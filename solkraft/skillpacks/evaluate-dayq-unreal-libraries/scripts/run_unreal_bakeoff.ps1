[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$UnrealRoot,

    [Parameter(Mandatory = $true)]
    [string]$Project,

    [Parameter(Mandatory = $true)]
    [string]$ReportDirectory,

    [string]$TestFilter = 'DayQ.Ballistics',
    [string]$Configuration = 'Development'
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $UnrealRoot).Path
$resolvedProject = (Resolve-Path -LiteralPath $Project).Path
$report = [System.IO.Path]::GetFullPath($ReportDirectory)
New-Item -ItemType Directory -Path $report -Force | Out-Null

$projectName = [System.IO.Path]::GetFileNameWithoutExtension($resolvedProject)
$build = Join-Path $resolvedRoot 'Engine\Build\BatchFiles\Build.bat'
$editor = Join-Path $resolvedRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'

if (-not (Test-Path -LiteralPath $build)) { throw "Missing Unreal Build.bat: $build" }
if (-not (Test-Path -LiteralPath $editor)) { throw "Missing UnrealEditor-Cmd.exe: $editor" }

function Invoke-Captured {
    param([string]$Name, [scriptblock]$Command)
    $log = Join-Path $report "$Name.log"
    $started = Get-Date
    & $Command 2>&1 | Tee-Object -FilePath $log | Out-Host
    $code = $LASTEXITCODE
    [pscustomobject]@{
        name = $Name
        exit_code = $code
        started_at = $started.ToUniversalTime().ToString('o')
        finished_at = (Get-Date).ToUniversalTime().ToString('o')
        log = $log
        sha256 = (Get-FileHash -LiteralPath $log -Algorithm SHA256).Hash
    }
}

$results = @()
$results += Invoke-Captured 'editor-build' {
    & $build "${projectName}Editor" Win64 $Configuration "-Project=$resolvedProject" -WaitMutex -NoHotReloadFromIDE -NoXGE
}

if ($results[-1].exit_code -eq 0) {
    $results += Invoke-Captured 'server-build' {
        & $build "${projectName}Server" Win64 $Configuration "-Project=$resolvedProject" -WaitMutex -NoXGE
    }
    $automationReport = Join-Path $report 'automation'
    $results += Invoke-Captured 'automation' {
        & $editor $resolvedProject -Unattended -NoSplash -NullRHI -NoSound -NoP4 "-ExecCmds=Automation RunTests $TestFilter;Quit" "-ReportExportPath=$automationReport" -TestExit='Automation Test Queue Empty'
    }
}

$summary = [ordered]@{
    schema = 1
    created_at = (Get-Date).ToUniversalTime().ToString('o')
    unreal_root = $resolvedRoot
    project = $resolvedProject
    project_sha256 = (Get-FileHash -LiteralPath $resolvedProject -Algorithm SHA256).Hash
    test_filter = $TestFilter
    results = $results
}
$summary | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $report 'run-summary.json') -Encoding utf8
$summary | ConvertTo-Json -Depth 8

if (@($results | Where-Object { $_.exit_code -ne 0 }).Count -gt 0) { exit 1 }
