[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][ValidatePattern('^[a-z0-9-]+$')][string]$SkillId,
  [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string[]]$OwnedPaths,
  [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$CommitMessage,
  [string]$EvidenceManifestPath,
  [string[]]$PreserveMasteryProgramId,
  [switch]$ValidateEvidenceManifestOnly
)

$ErrorActionPreference='Stop'

function Get-Sha256([string]$Path){
  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-TextSha256([string]$Text){
  $algorithm=[System.Security.Cryptography.SHA256]::Create()
  try{
    $bytes=[System.Text.UTF8Encoding]::new($false).GetBytes($Text)
    return ([System.BitConverter]::ToString($algorithm.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()
  }finally{$algorithm.Dispose()}
}

function Get-NormalizedTextFileSha256([string]$Path){
  $text=[System.IO.File]::ReadAllText($Path).Replace("`r`n","`n").Replace("`r","`n")
  return Get-TextSha256 $text
}

function Get-GitBlobSha256([string]$Root,[string]$Commit,[string]$RelativePath){
  $nodeScript="const{spawnSync}=require('node:child_process');const{createHash}=require('node:crypto');const r=spawnSync('git',['-C',process.argv[1],'show',process.argv[2]],{encoding:null,maxBuffer:1024*1024*1024});if(r.status!==0){process.stderr.write(r.stderr||'git show failed');process.exit(r.status??1)}process.stdout.write(createHash('sha256').update(r.stdout).digest('hex'));"
  $hash=(& node -e $nodeScript $Root "${Commit}:$RelativePath").Trim()
  if($LASTEXITCODE -ne 0 -or $hash -notmatch '^[a-f0-9]{64}$'){throw "Unable to hash source-commit evidence blob: $RelativePath"}
  return $hash
}

function Set-EnrichedReceiptAtomically([string]$ReceiptPath,[string]$Json,[scriptblock]$Verify){
  if(-not (Test-Path -LiteralPath $ReceiptPath -PathType Leaf)){throw 'The official release receipt is missing before enrichment.'}
  $receiptDirectory=Split-Path -Parent $ReceiptPath
  $receiptName=Split-Path -Leaf $ReceiptPath
  $nonce=[guid]::NewGuid().ToString('n')
  $temporaryReceipt=Join-Path $receiptDirectory ".$receiptName.$nonce.enriched.tmp"
  $backupReceipt=Join-Path $receiptDirectory ".$receiptName.$nonce.pre-enrichment.backup"
  $failedReceipt=Join-Path $receiptDirectory ".$receiptName.$nonce.failed-enrichment.tmp"
  $replaced=$false
  [System.IO.File]::WriteAllText($temporaryReceipt,$Json,[System.Text.UTF8Encoding]::new($false))
  try{
    [System.IO.File]::Replace($temporaryReceipt,$ReceiptPath,$backupReceipt,$true)
    $replaced=$true
    $verified=& $Verify $ReceiptPath
    Remove-Item -LiteralPath $backupReceipt -Force
    return $verified
  }catch{
    $enrichmentFailure=$_
    if($replaced -and (Test-Path -LiteralPath $backupReceipt -PathType Leaf)){
      try{
        [System.IO.File]::Replace($backupReceipt,$ReceiptPath,$failedReceipt,$true)
        if(Test-Path -LiteralPath $failedReceipt){Remove-Item -LiteralPath $failedReceipt -Force}
      }catch{
        throw "Official receipt enrichment failed and the prior receipt could not be restored. Enrichment failure: $($enrichmentFailure.Exception.Message). Restore failure: $($_.Exception.Message)"
      }
    }
    throw $enrichmentFailure
  }finally{
    if(Test-Path -LiteralPath $temporaryReceipt){Remove-Item -LiteralPath $temporaryReceipt -Force}
  }
}

function Resolve-RepositoryFile([string]$Root,[string]$Path,[string]$Label){
  if([string]::IsNullOrWhiteSpace($Path)){throw "$Label path is required."}
  $candidate=if([System.IO.Path]::IsPathRooted($Path)){$Path}else{Join-Path $Root $Path}
  $absolute=[System.IO.Path]::GetFullPath($candidate)
  if(-not (Test-Path -LiteralPath $absolute -PathType Leaf)){throw "$Label is missing or is not a file: $Path"}
  $item=Get-Item -LiteralPath $absolute -Force
  if(($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0){throw "$Label may not be a reparse point: $Path"}
  $resolved=(Resolve-Path -LiteralPath $absolute).Path
  $rootBoundary=$Root.TrimEnd([char[]]'\/')+[System.IO.Path]::DirectorySeparatorChar
  if(-not $resolved.StartsWith($rootBoundary,[System.StringComparison]::OrdinalIgnoreCase)){throw "$Label escapes repository root ${Root}: $Path"}
  $ancestor=Split-Path -Parent $resolved
  while($ancestor -and -not $ancestor.Equals($Root,[System.StringComparison]::OrdinalIgnoreCase)){
    $ancestorItem=Get-Item -LiteralPath $ancestor -Force
    if(($ancestorItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0){throw "$Label may not traverse a reparse point: $Path"}
    $parent=Split-Path -Parent $ancestor
    if($parent -eq $ancestor){break}
    $ancestor=$parent
  }
  return [pscustomobject]@{
    Absolute=$resolved
    Relative=$resolved.Substring($rootBoundary.Length).Replace('\','/')
  }
}

function Test-OwnedPathCoverage([string]$Relative,[string[]]$NormalizedOwned){
  foreach($owned in $NormalizedOwned){
    if($Relative.Equals($owned,[System.StringComparison]::OrdinalIgnoreCase) -or $Relative.StartsWith("$owned/",[System.StringComparison]::OrdinalIgnoreCase)){return $true}
  }
  return $false
}

function Resolve-ReleaseEvidenceManifest([string]$Root,[string]$Path,[string]$ExpectedSkillId,[string[]]$NormalizedOwned){
  $manifestFile=Resolve-RepositoryFile $Root $Path 'Release evidence manifest'
  if(-not ($NormalizedOwned -contains $manifestFile.Relative)){throw "EvidenceManifestPath must be explicitly included in OwnedPaths: $($manifestFile.Relative)"}
  try{$manifest=Get-Content -LiteralPath $manifestFile.Absolute -Raw | ConvertFrom-Json}catch{throw "Release evidence manifest is not valid JSON: $($_.Exception.Message)"}
  $topLevel=@($manifest.psobject.Properties.Name)
  $unsupportedTop=@($topLevel | Where-Object {$_ -notin @('schemaVersion','kind','skillId','evidence')})
  if($unsupportedTop.Count){throw "Release evidence manifest contains unsupported fields: $($unsupportedTop -join ', ')"}
  if($manifest.schemaVersion -ne '1.0'){throw 'Release evidence manifest schemaVersion must be 1.0.'}
  if($manifest.kind -ne 'solforge-official-release-evidence'){throw 'Release evidence manifest kind is invalid.'}
  if($manifest.skillId -ne $ExpectedSkillId){throw "Release evidence manifest skillId mismatch: expected $ExpectedSkillId."}
  if(-not $manifest.evidence){throw 'Release evidence manifest evidence object is required.'}
  $categories=@('visual','recovery','benchmark')
  $unsupportedCategories=@($manifest.evidence.psobject.Properties.Name | Where-Object {$_ -notin $categories})
  if($unsupportedCategories.Count){throw "Release evidence manifest contains unsupported evidence categories: $($unsupportedCategories -join ', ')"}
  $seenIds=@{}
  $seenPaths=@{}
  $normalizedEvidence=[ordered]@{}
  foreach($category in $categories){
    $entries=@($manifest.evidence.$category)
    if(-not $entries.Count){throw "Release evidence manifest requires at least one $category evidence entry."}
    $normalized=@()
    foreach($entry in $entries){
      $unsupportedFields=@($entry.psobject.Properties.Name | Where-Object {$_ -notin @('id','path','sha256')})
      if($unsupportedFields.Count){throw "Release evidence entry contains unsupported fields: $($unsupportedFields -join ', ')"}
      if($entry.id -notmatch '^[a-z0-9][a-z0-9._-]*$'){throw "Release evidence id is invalid: $($entry.id)"}
      $idKey="$category/$($entry.id)"
      if($seenIds.ContainsKey($idKey)){throw "Duplicate release evidence id: $idKey"}
      $seenIds[$idKey]=$true
      if([System.IO.Path]::IsPathRooted([string]$entry.path)){throw "Release evidence paths must be repository-relative: $($entry.path)"}
      $evidenceFile=Resolve-RepositoryFile $Root ([string]$entry.path) "$category evidence"
      if($seenPaths.ContainsKey($evidenceFile.Relative.ToLowerInvariant())){throw "Duplicate release evidence path: $($evidenceFile.Relative)"}
      $seenPaths[$evidenceFile.Relative.ToLowerInvariant()]=$true
      if(-not (Test-OwnedPathCoverage $evidenceFile.Relative $NormalizedOwned)){throw "Release evidence path is not covered by OwnedPaths: $($evidenceFile.Relative)"}
      $expected=([string]$entry.sha256).ToLowerInvariant()
      if($expected -notmatch '^[a-f0-9]{64}$'){throw "Release evidence SHA-256 is invalid: $idKey"}
      $actual=Get-Sha256 $evidenceFile.Absolute
      if($actual -ne $expected){throw "Release evidence SHA-256 mismatch for ${idKey}: expected $expected, got $actual"}
      $normalized+=[ordered]@{id=[string]$entry.id;path=$evidenceFile.Relative;sha256=$actual}
    }
    $normalizedEvidence[$category]=$normalized
  }
  return [pscustomobject]@{
    Manifest=[ordered]@{
      schemaVersion='1.0'
      kind='solforge-official-release-evidence'
      skillId=$ExpectedSkillId
      path=$manifestFile.Relative
      sha256=(Get-Sha256 $manifestFile.Absolute)
    }
    Evidence=$normalizedEvidence
  }
}

function Invoke-ProtectedBundleVerifier([string]$PluginDirectory,[string]$Profile,[string]$Scope){
  $profileRoot=Join-Path $PluginDirectory "skills\$Profile"
  $verifier=Join-Path $profileRoot 'scripts\verify_bundle.py'
  $bundleManifest=Join-Path $profileRoot 'references\manifest.json'
  if(-not (Test-Path -LiteralPath $verifier -PathType Leaf) -or -not (Test-Path -LiteralPath $bundleManifest -PathType Leaf)){throw "Protected profile bundle verifier inputs are missing: $Profile ($Scope)"}
  Push-Location $profileRoot
  try{
    & python 'scripts/verify_bundle.py' | Out-Host
    $verifierExit=$LASTEXITCODE
  }finally{Pop-Location}
  if($verifierExit -ne 0){throw "Protected profile bundle verification failed: $Profile ($Scope)"}
  return [ordered]@{
    profileId=$Profile
    scope=$Scope
    result='passed'
    verifierPath="skills/$Profile/scripts/verify_bundle.py"
    verifierSha256=(Get-NormalizedTextFileSha256 $verifier)
    manifestPath="skills/$Profile/references/manifest.json"
    manifestSha256=(Get-NormalizedTextFileSha256 $bundleManifest)
  }
}

function Invoke-InstalledMcpDiscovery([string]$InstalledPluginRoot){
  $discoveryScript=Join-Path $InstalledPluginRoot 'scripts\mcp-discovery-smoke.mjs'
  if(-not (Test-Path -LiteralPath $discoveryScript -PathType Leaf)){throw 'Installed MCP discovery script is missing.'}
  Push-Location $InstalledPluginRoot
  try{
    $discoveryOutput=@(& node $discoveryScript 2>&1)
    $discoveryExit=$LASTEXITCODE
  }finally{Pop-Location}
  $discoveryOutput | ForEach-Object {Write-Host ([string]$_)}
  if($discoveryExit -ne 0){throw 'Installed MCP discovery failed.'}
  $summary=($discoveryOutput | ForEach-Object {[string]$_}) -join "`n"
  if($summary -notmatch 'SolForge Codex discovery smoke passed \((\d+) tools / (\d+) app-only via ([^)]+)\)'){throw 'Installed MCP discovery output did not contain verifiable registered and app-only tool counts.'}
  $toolCount=[int]$Matches[1]
  $appOnlyToolCount=[int]$Matches[2]
  $serverName=$Matches[3]
  if($serverName -ne 'solforge'){throw "Installed MCP discovery used an unexpected server: $serverName"}
  if($toolCount -lt 1){throw 'Installed MCP discovery did not expose any tools.'}
  if($appOnlyToolCount -lt 1 -or $appOnlyToolCount -ge $toolCount){throw 'Installed MCP discovery did not preserve both model-callable and app-only authority surfaces.'}
  return [ordered]@{
    result='passed'
    serverName=$serverName
    toolCount=$toolCount
    appOnlyToolCount=$appOnlyToolCount
    verifiedToolCount=$toolCount
    verifiedAppOnlyToolCount=$appOnlyToolCount
    scriptPath='scripts/mcp-discovery-smoke.mjs'
    scriptSha256=(Get-Sha256 $discoveryScript)
  }
}
$skillScriptRoot=$PSScriptRoot
$repositoryRoot=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $skillScriptRoot)))
$repositoryRoot=(Resolve-Path -LiteralPath $repositoryRoot).Path
$pluginRoot=Join-Path $repositoryRoot 'plugin'
$skillRoot=Join-Path $pluginRoot "skills\$SkillId"
$manifestPath=Join-Path $pluginRoot '.codex-plugin\plugin.json'
$releaseScript=Join-Path $repositoryRoot 'scripts\release-solforge-plugin.ps1'
$validator=Join-Path $HOME '.codex\skills\.system\skill-creator\scripts\quick_validate.py'

if(-not (Test-Path -LiteralPath (Join-Path $skillRoot 'SKILL.md'))){throw "SolForge skill source is missing: $skillRoot"}
if(-not (Test-Path -LiteralPath (Join-Path $skillRoot 'agents\openai.yaml'))){throw 'Native agents/openai.yaml metadata is required.'}
if(-not (Test-Path -LiteralPath $releaseScript)){throw 'The official SolForge release script is missing.'}
if(-not (Test-Path -LiteralPath $validator)){throw 'The system skill validator is missing.'}

$normalizedOwned=@()
foreach($path in $OwnedPaths){
  $absolute=if([System.IO.Path]::IsPathRooted($path)){[System.IO.Path]::GetFullPath($path)}else{[System.IO.Path]::GetFullPath((Join-Path $repositoryRoot $path))}
  $rootBoundary=$repositoryRoot.TrimEnd([char[]]'\/')+[System.IO.Path]::DirectorySeparatorChar
  if(-not $absolute.StartsWith($rootBoundary,[System.StringComparison]::OrdinalIgnoreCase)){throw "Owned path escapes repository root ${repositoryRoot}: $path"}
  $relative=$absolute.Substring($rootBoundary.Length).Replace('\','/')
  $normalizedOwned+=$relative
}
$skillRelative="plugin/skills/$SkillId"
if(-not ($normalizedOwned | Where-Object {$_ -eq $skillRelative -or $_.StartsWith("$skillRelative/")})){throw "OwnedPaths must include $skillRelative"}
$releaseEvidence=$null
if(-not [string]::IsNullOrWhiteSpace($EvidenceManifestPath)){
  $releaseEvidence=Resolve-ReleaseEvidenceManifest $repositoryRoot $EvidenceManifestPath $SkillId $normalizedOwned
}
if($ValidateEvidenceManifestOnly){
  if(-not $releaseEvidence){throw 'ValidateEvidenceManifestOnly requires EvidenceManifestPath.'}
  $atomicTestRoot=Join-Path ([System.IO.Path]::GetTempPath()) ("solforge-receipt-replace-"+[guid]::NewGuid().ToString('n'))
  New-Item -ItemType Directory -Path $atomicTestRoot | Out-Null
  try{
    $atomicTestReceipt=Join-Path $atomicTestRoot 'receipt.json'
    [System.IO.File]::WriteAllText($atomicTestReceipt,'{"state":"prior"}',[System.Text.UTF8Encoding]::new($false))
    $rollbackObserved=$false
    try{
      Set-EnrichedReceiptAtomically $atomicTestReceipt '{"state":"candidate"}' {param($Path) throw 'intentional post-replace verification failure'} | Out-Null
    }catch{
      if($_.Exception.Message -match 'intentional post-replace verification failure'){$rollbackObserved=$true}else{throw}
    }
    if(-not $rollbackObserved -or (Get-Content -LiteralPath $atomicTestReceipt -Raw) -ne '{"state":"prior"}'){throw 'Atomic receipt replacement did not restore the prior receipt after verification failure.'}
    $accepted=Set-EnrichedReceiptAtomically $atomicTestReceipt '{"state":"accepted"}' {param($Path) if((Get-Content -LiteralPath $Path -Raw) -ne '{"state":"accepted"}'){throw 'replacement content mismatch'};return $true}
    if(-not $accepted -or @(Get-ChildItem -LiteralPath $atomicTestRoot -File).Count -ne 1){throw 'Atomic receipt replacement did not remove its backup after successful verification.'}
    [pscustomobject]@{Valid=$true;AtomicReceiptReplacementVerified=$true;Manifest=$releaseEvidence.Manifest;Evidence=$releaseEvidence.Evidence} | ConvertTo-Json -Depth 16
  }finally{Remove-Item -LiteralPath $atomicTestRoot -Recurse -Force}
  return
}

$statePath=Join-Path $HOME '.solforge\state-v1.json'
if(Test-Path -LiteralPath $statePath){
  $state=Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
  $unsafe=@($state.runs.psobject.Properties | Where-Object {$_.Value.lease.state -eq 'active' -or $_.Value.state -in @('running','pausing','prompt_run_pending')})
  if($unsafe.Count){$summary=($unsafe | ForEach-Object {"$($_.Name) [$($_.Value.state), lease=$($_.Value.lease.state)]"}) -join '; ';throw "Active SolForge work prevents skill release: $summary. Safe Pause or complete it first."}
  $unsafeResearch=@()
  if($state.masteryPrograms){$unsafeResearch+=@($state.masteryPrograms.psobject.Properties | Where-Object {$_.Value.activeClosureExecutionLease})}
  if($unsafeResearch.Count){$summary=($unsafeResearch | ForEach-Object {"$($_.Name) [closure execution lease active]"}) -join '; ';throw "Active Code Research execution prevents skill release: $summary. Finish or safely stop the exact mutation lease first."}
}

$env:PYTHONUTF8='1'
& node (Join-Path $pluginRoot 'scripts\product-contract-preflight.mjs')
if($LASTEXITCODE -ne 0){throw 'SolForge product contract preflight failed.'}
& python $validator $skillRoot
if($LASTEXITCODE -ne 0){throw 'Source skill validation failed.'}
$protectedBundleProfiles=@('solforge-prompt-single','solforge-prompt-multi','solforge-prompt-ultra','solforge-run-single','solforge-run-multi','solforge-run-ultra')
$sourceProtectedVerifierResults=@()
foreach($profile in $protectedBundleProfiles){
  $sourceProtectedVerifierResults+=Invoke-ProtectedBundleVerifier $pluginRoot $profile 'source'
}
& npm --prefix $repositoryRoot run test:plugin
if($LASTEXITCODE -ne 0){throw 'SolForge plugin tests failed.'}

$manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$currentBuild=0L
if($manifest.version -match '^([^+]+)\+codex\.(\d+)$'){$baseVersion=$Matches[1];$currentBuild=[int64]$Matches[2]}else{$baseVersion=($manifest.version -split '\+',2)[0]}
$clockBuild=[int64](Get-Date -Format 'yyyyMMddHHmmss')
$nextBuild=[Math]::Max($clockBuild,$currentBuild+1)
$manifest.version="$baseVersion+codex.$nextBuild"
$manifestJson=$manifest | ConvertTo-Json -Depth 32
[System.IO.File]::WriteAllText($manifestPath,"$manifestJson`n",[System.Text.UTF8Encoding]::new($false))

$pathsToStage=@($normalizedOwned+'plugin/.codex-plugin/plugin.json' | Select-Object -Unique)
& git -C $repositoryRoot add -- @pathsToStage
if($LASTEXITCODE -ne 0){throw 'Unable to stage owned SolForge paths.'}
& git -C $repositoryRoot diff --cached --check
if($LASTEXITCODE -ne 0){throw 'Staged SolForge changes failed git diff --check.'}
$staged=@(& git -C $repositoryRoot diff --cached --name-only)
$skillContractIndexPath="$skillRelative/SKILL.md"
& git -C $repositoryRoot cat-file -e ":$skillContractIndexPath" 2>$null
if($LASTEXITCODE -ne 0){throw 'The staged release does not contain the skill contract.'}
if($releaseEvidence){
  $evidenceManifestIndexPath=$releaseEvidence.Manifest.path
  & git -C $repositoryRoot cat-file -e ":$evidenceManifestIndexPath" 2>$null
  if($LASTEXITCODE -ne 0){throw "The staged release does not contain the evidence manifest: $evidenceManifestIndexPath"}
}
$unstagedTracked=@(& git -C $repositoryRoot diff --name-only)
if($unstagedTracked.Count){throw "Unstaged tracked changes prevent a deterministic release: $($unstagedTracked -join ', ')"}

$trackedOutside=@(& git -C $repositoryRoot status --porcelain --untracked-files=no | ForEach-Object {$_.Substring(3).Replace('\','/')} | Where-Object {$_ -notin $staged})
if($trackedOutside.Count){throw "Unrelated tracked changes prevent a safe release: $($trackedOutside -join ', ')"}
$untrackedOutside=@(& git -C $repositoryRoot ls-files --others --exclude-standard)
if($untrackedOutside.Count){throw "Untracked files prevent a source-commit-bound release: $($untrackedOutside -join ', ')"}

& git -C $repositoryRoot commit -m $CommitMessage
if($LASTEXITCODE -ne 0){throw 'Unable to commit the complete SolForge skill release.'}
$sourceCommit=(& git -C $repositoryRoot rev-parse HEAD).Trim()
if($releaseEvidence){
  $postCommitEvidence=Resolve-ReleaseEvidenceManifest $repositoryRoot $EvidenceManifestPath $SkillId $normalizedOwned
  if($postCommitEvidence.Manifest.sha256 -ne $releaseEvidence.Manifest.sha256){throw 'Release evidence manifest changed after validation.'}
  $releaseEvidence=$postCommitEvidence
  $commitBoundEvidence=@([pscustomobject]@{path=$releaseEvidence.Manifest.path;sha256=$releaseEvidence.Manifest.sha256})
  foreach($category in @('visual','recovery','benchmark')){foreach($entry in @($releaseEvidence.Evidence[$category])){$commitBoundEvidence+=[pscustomobject]@{path=$entry.path;sha256=$entry.sha256}}}
  foreach($binding in $commitBoundEvidence){
    $boundPath=$binding.path
    $trackedAtCommit=@(& git -C $repositoryRoot ls-tree -r --name-only $sourceCommit -- $boundPath)
    if($LASTEXITCODE -ne 0 -or -not ($trackedAtCommit | Where-Object {$_.Replace('\','/') -eq $boundPath})){throw "Release evidence is not bound to source commit ${sourceCommit}: $boundPath"}
    $committedSha256=Get-GitBlobSha256 $repositoryRoot $sourceCommit $boundPath
    if($committedSha256 -ne $binding.sha256){throw "Source-commit evidence SHA-256 mismatch for ${boundPath}: expected $($binding.sha256), got $committedSha256"}
  }
}

$releaseArguments = @{
  RepositoryRoot = $repositoryRoot
}
if (@($PreserveMasteryProgramId).Count) {
  $releaseArguments.PreserveMasteryProgramId = $PreserveMasteryProgramId
}
& $releaseScript @releaseArguments
if($LASTEXITCODE -ne 0){throw 'Official SolForge installation failed.'}

$receiptPath=Join-Path $HOME '.codex\plugins\solforge-release-current.json'
$receipt=Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if($receipt.sourceCommit -ne $sourceCommit){throw 'Release receipt source commit mismatch.'}
$sourcePluginTree=(& git -C $repositoryRoot rev-parse "${sourceCommit}:plugin").Trim()
if($LASTEXITCODE -ne 0 -or $receipt.sourcePluginTree -ne $sourcePluginTree){throw 'Release receipt committed plugin tree mismatch.'}
if($receipt.bundleInputMode -ne 'git-archive-committed-plugin-tree'){throw 'Release receipt bundle input mode is not commit-derived.'}
if([System.IO.Path]::GetFullPath($receipt.sourceRepositoryRoot) -ne [System.IO.Path]::GetFullPath($repositoryRoot)){throw 'Release receipt source repository mismatch.'}
if($receipt.commitBundleSha256 -ne $receipt.bundleSha256){throw 'Release receipt committed bundle hash mismatch.'}
if(-not (Test-Path -LiteralPath (Join-Path $receipt.installedPath "skills\$SkillId\SKILL.md"))){throw 'Installed plugin does not contain the new SolForge skill.'}
& node (Join-Path $receipt.installedPath 'scripts\verify-release-state.mjs') --verify $receipt.installedPath $receipt.resolverSourcePath $receiptPath
if($LASTEXITCODE -ne 0){throw 'Installed runtime freshness verification failed.'}
$env:PYTHONUTF8='1'
& python $validator (Join-Path $receipt.installedPath "skills\$SkillId")
if($LASTEXITCODE -ne 0){throw 'Installed skill validation failed.'}
$installedProtectedVerifierResults=@()
foreach($profile in $protectedBundleProfiles){
  $installedProtectedVerifierResults+=Invoke-ProtectedBundleVerifier $receipt.installedPath $profile 'installed'
}
$installedMcpDiscovery=Invoke-InstalledMcpDiscovery $receipt.installedPath

$releaseEvidenceSha256=$null
$receiptFileSha256=$null
if($releaseEvidence){
  foreach($profile in $protectedBundleProfiles){
    $sourceResult=$sourceProtectedVerifierResults | Where-Object {$_.profileId -eq $profile}
    $installedResult=$installedProtectedVerifierResults | Where-Object {$_.profileId -eq $profile}
    if(-not $sourceResult -or -not $installedResult -or $sourceResult.verifierSha256 -ne $installedResult.verifierSha256 -or $sourceResult.manifestSha256 -ne $installedResult.manifestSha256){throw "Installed protected verifier evidence differs from source: $profile"}
  }
  $receiptEnrichment=[ordered]@{
    schemaVersion='1.0'
    evidenceManifest=$releaseEvidence.Manifest
    evidence=$releaseEvidence.Evidence
    protectedVerifierResults=[ordered]@{
      source=@($sourceProtectedVerifierResults)
      installed=@($installedProtectedVerifierResults)
    }
    installedMcpDiscovery=$installedMcpDiscovery
  }
  $receiptEnrichmentJson=$receiptEnrichment | ConvertTo-Json -Compress -Depth 32
  $releaseEvidenceSha256=Get-TextSha256 $receiptEnrichmentJson
  $receipt.schemaVersion='1.1'
  $receipt | Add-Member -NotePropertyName releaseEvidence -NotePropertyValue $receiptEnrichment -Force
  $receipt | Add-Member -NotePropertyName releaseEvidenceSha256 -NotePropertyValue $releaseEvidenceSha256 -Force
  $enrichedReceiptJson=$receipt | ConvertTo-Json -Depth 32
  $writtenReceipt=Set-EnrichedReceiptAtomically $receiptPath $enrichedReceiptJson {
    param($CandidateReceiptPath)
    $candidateReceipt=Get-Content -LiteralPath $CandidateReceiptPath -Raw | ConvertFrom-Json
    $writtenEnrichmentJson=$candidateReceipt.releaseEvidence | ConvertTo-Json -Compress -Depth 32
    if((Get-TextSha256 $writtenEnrichmentJson) -ne $candidateReceipt.releaseEvidenceSha256){throw 'Enriched official release receipt hash mismatch.'}
    if($candidateReceipt.releaseEvidence.evidenceManifest.sha256 -ne $releaseEvidence.Manifest.sha256){throw 'Enriched official release receipt evidence manifest mismatch.'}
    & node (Join-Path $candidateReceipt.installedPath 'scripts\verify-release-state.mjs') --verify $candidateReceipt.installedPath $candidateReceipt.resolverSourcePath $CandidateReceiptPath | Out-Host
    if($LASTEXITCODE -ne 0){throw 'Installed runtime freshness verification failed after official receipt enrichment.'}
    return $candidateReceipt
  }
  $receipt=$writtenReceipt
  $receiptFileSha256=Get-Sha256 $receiptPath
}

[pscustomobject]@{
  SkillId=$SkillId
  InstalledVersion=$receipt.installedVersion
  SourceCommit=$sourceCommit
  BundleSha256=$receipt.bundleSha256
  ResolverSourcePath=$receipt.resolverSourcePath
  InstalledPath=$receipt.installedPath
  ReceiptPath=$receiptPath
  VersionReceiptPath=(Join-Path $HOME ".codex\plugins\solforge-releases\$($receipt.installedVersion).json")
  PreservedProcessIds=@($receipt.preservedProcessIds)
  ReceiptFileSha256=$receiptFileSha256
  EvidenceManifestSha256=if($releaseEvidence){$releaseEvidence.Manifest.sha256}else{$null}
  ReleaseEvidenceSha256=$releaseEvidenceSha256
  NativeMcpRegistered=$true
  InstalledMcpToolCount=$installedMcpDiscovery.toolCount
  NewTaskRequired=$false
  RuntimeRestartRequired=$false
}
