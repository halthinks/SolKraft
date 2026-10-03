#!/usr/bin/env node
import { createHash } from "node:crypto";
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { platformPlanCompletionHash } from "../../../server/platform-delivery.mjs";
import { strategySha256 } from "../../../server/strategy-policy.mjs";
import { readState } from "../../../server/state-store.mjs";

const [manifestFile, outputDirectory, planContractFile, routeReceiptFile] =
  process.argv.slice(2);
const HASH = /^[a-f0-9]{64}$/u;
if (!manifestFile || !outputDirectory || !planContractFile || !routeReceiptFile) {
  console.error(
    "Usage: render-installers.mjs <manifest.json> <new-output-directory> <plan-contract.json> <route-receipt.json>",
  );
  process.exit(64);
}
const manifestText = await readFile(resolve(manifestFile), "utf8");
const manifestSha256 = sha(manifestText);
const manifest = JSON.parse(manifestText);
const routeReceipt = JSON.parse(
  await readFile(resolve(routeReceiptFile), "utf8"),
);
const allowedReceiptKeys = [
  "schemaVersion",
  "kind",
  "decision",
  "canonicalSkillId",
  "routeHash",
  "targets",
  "strategySelections",
  "strategySelectionsSha256",
  "completionMode",
  "objectiveSha256",
  "actionDirectiveSha256",
  "repositoryProfileSha256",
  "authority",
  "receiptSha256",
  "deliveryManifestSha256",
];
const unsignedRouteReceipt = { ...routeReceipt };
delete unsignedRouteReceipt.receiptSha256;
if (
  Object.keys(routeReceipt).some((key) => !allowedReceiptKeys.includes(key)) ||
  routeReceipt.schemaVersion !== "1.0" ||
  routeReceipt.kind !== "solforge-launcher-route-acceptance" ||
  routeReceipt.decision !== "accepted" ||
  routeReceipt.canonicalSkillId !== "solforge-launcher" ||
  !HASH.test(routeReceipt.routeHash ?? "") ||
  !Array.isArray(routeReceipt.targets) ||
  routeReceipt.targets.length === 0 ||
  strategySha256(routeReceipt.strategySelections) !==
    routeReceipt.strategySelectionsSha256 ||
  !["audit", "execution"].includes(routeReceipt.completionMode) ||
  !HASH.test(routeReceipt.objectiveSha256 ?? "") ||
  !HASH.test(routeReceipt.actionDirectiveSha256 ?? "") ||
  !HASH.test(routeReceipt.repositoryProfileSha256 ?? "") ||
  routeReceipt.authority?.permissionExpansionAuthorized !== false ||
  JSON.stringify(routeReceipt.authority?.externalEffects) !== "[]" ||
  strategySha256(unsignedRouteReceipt) !== routeReceipt.receiptSha256
)
  throw new Error("accepted Launcher route receipt is invalid");
const state = await readState();
if (
  JSON.stringify(state.platformRouteReceipts?.[routeReceipt.receiptSha256]) !==
  JSON.stringify(routeReceipt)
)
  throw new Error(
    "Launcher route receipt was not issued by the acceptance boundary",
  );
const { routeHash, receiptSha256: routeReceiptSha256 } = routeReceipt;
const planContract = JSON.parse(
  await readFile(resolve(planContractFile), "utf8"),
);
const { requestId, planCompletionHash, acceptedActionDirective } = planContract;
if (
  routeReceipt.deliveryManifestSha256 !== manifestSha256 ||
  strategySha256(acceptedActionDirective) !==
    routeReceipt.actionDirectiveSha256 ||
  platformPlanCompletionHash({
    requestId,
    routeReceipt,
    acceptedActionDirective,
  }) !== planCompletionHash
)
  throw new Error(
    "plan contract does not bind the Launcher manifest and accepted route receipt",
  );
const action = acceptedActionDirective;
if (
  !/^(?:write|create|generate|build|render|produce)\b.*\b(?:launcher|installer|installation package)\b/iu.test(
    action,
  ) ||
  /\b(?:do not|don't|never)\b/iu.test(action)
)
  throw new Error(
    "accepted action directive must positively direct the launcher or installer write",
  );
if (!/^https:\/\//iu.test(manifest.artifactUrl ?? ""))
  throw new Error("artifactUrl must use HTTPS");
if (!HASH.test(manifest.artifactSha256 ?? ""))
  throw new Error("artifactSha256 is required");
if (!manifest.projectName) throw new Error("projectName is required");
for (const platform of ["shell", "powershell"])
  for (const action of [
    "install",
    "launch",
    "update",
    "uninstall",
    "rollback",
  ]) {
    const command = manifest.journeys?.[platform]?.[action];
    if (
      typeof command !== "string" ||
      !command.trim() ||
      /[\r\n\0]/u.test(command)
    )
      throw new Error(
        `journeys.${platform}.${action} must be a non-empty single-line command`,
      );
    if (
      ["launch", "uninstall", "rollback"].includes(action) &&
      command.includes("{{artifact}}")
    )
      throw new Error(
        `journeys.${platform}.${action} cannot depend on a fresh download`,
      );
  }
const output = resolve(outputDirectory);
const files = {
  "install.sh": shell(manifest),
  "install.ps1": powershell(manifest),
  "release-manifest.json":
    JSON.stringify(
      {
        ...manifest,
        manifestSha256,
        planCompletionHash,
        routeHash,
        routeReceiptSha256,
      },
      null,
      2,
    ) + "\n",
};
for (const name of Object.keys(files)) {
  const target = resolve(output, name);
  try {
    await access(target);
    throw new Error(
      `refusing to overwrite existing launcher artifact: ${target}`,
    );
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}
await mkdir(output, { recursive: true });
for (const [name, text] of Object.entries(files))
  await writeFile(resolve(output, name), text, "utf8");
console.log(
  JSON.stringify(
    {
      accepted: true,
      planCompletionHash,
      routeHash,
      files: Object.fromEntries(
        Object.entries(files).map(([name, text]) => [name, sha(text)]),
      ),
    },
    null,
    2,
  ),
);

function shell(m) {
  const j = m.journeys.shell,
    cmd = (action) => j[action].replaceAll("{{artifact}}", '"$tmp"');
  return `#!/bin/sh\nset -eu\nurl='${safe(m.artifactUrl)}'\nexpected='${m.artifactSha256}'\ntmp="\${TMPDIR:-/tmp}/${safe(m.projectName)}.$$"\ntrap 'rm -f "$tmp"' EXIT INT TERM\ndownload_verified() { curl --fail --location --proto '=https' --tlsv1.2 "$url" --output "$tmp"; if command -v sha256sum >/dev/null 2>&1; then actual=$(sha256sum "$tmp" | awk '{print $1}'); elif command -v shasum >/dev/null 2>&1; then actual=$(shasum -a 256 "$tmp" | awk '{print $1}'); else printf 'No SHA-256 verifier found.\\n' >&2; exit 1; fi; [ "$actual" = "$expected" ] || { printf 'Artifact SHA-256 mismatch.\\n' >&2; exit 1; }; }\ncase "\${1:-install}" in\n  install) download_verified; ${cmd("install")} ;;\n  launch) ${cmd("launch")} ;;\n  update) download_verified; ${cmd("update")} ;;\n  uninstall) ${cmd("uninstall")} ;;\n  rollback) ${cmd("rollback")} ;;\n  *) printf 'Usage: %s [install|launch|update|uninstall|rollback]\\n' "$0" >&2; exit 64 ;;\nesac\n`;
}
function powershell(m) {
  const j = m.journeys.powershell,
    cmd = (action) => j[action].replaceAll("{{artifact}}", "$tmp");
  return `param([ValidateSet('install','launch','update','uninstall','rollback')][string]$Action = 'install')\n$ErrorActionPreference = 'Stop'\n$url = '${safe(m.artifactUrl)}'\n$expected = '${m.artifactSha256}'\n$tmp = Join-Path ([System.IO.Path]::GetTempPath()) '${safe(m.projectName)}-download'\nfunction Get-VerifiedArtifact { Invoke-WebRequest -Uri $url -OutFile $tmp -UseBasicParsing; $actual = (Get-FileHash -LiteralPath $tmp -Algorithm SHA256).Hash.ToLowerInvariant(); if ($actual -ne $expected) { Remove-Item -LiteralPath $tmp -Force; throw 'Artifact SHA-256 mismatch' } }\nswitch ($Action) {\n  'install' { Get-VerifiedArtifact; ${cmd("install")} }\n  'launch' { ${cmd("launch")} }\n  'update' { Get-VerifiedArtifact; ${cmd("update")} }\n  'uninstall' { ${cmd("uninstall")} }\n  'rollback' { ${cmd("rollback")} }\n}\n`;
}
function safe(value) {
  return String(value).replace(/[^a-zA-Z0-9._:\/-]/gu, "-");
}
function sha(value) {
  return createHash("sha256").update(String(value)).digest("hex");
}
