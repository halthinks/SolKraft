# Launcher platform contract

| State | Required evidence | Permitted claim |
|---|---|---|
| `native_verified` | Built artifact plus successful clean real-target install, launch, update/uninstall where applicable | Works natively on the exact OS and architecture tested |
| `packaged_runtime` | Reproducible artifact build and clean packaged-runtime launch | Runs with the bundled or declared runtime |
| `containerized` | Reproducible OCI build, digest, SBOM, and runtime smoke | Runs in the tested container environment |
| `experimental` | Plausible route with explicit missing gates | Experimental target; not supported for production use |
| `unsupported` | Documented blocker | Not currently supported |

Every target needs an acquisition path, integrity check, prerequisites, install, launch, update, uninstall, troubleshooting, and verification story. Prefer native ecosystem conventions. A `curl` command must download over HTTPS, verify a pinned checksum or signature, avoid secret-bearing arguments, and have a download-and-inspect alternative. Never make piping remote code the only path.

Mobile artifacts require an existing verified mobile target with a viable native build and test path. Signing identity, notarization, store review, registry namespaces, and release publication are external effects, not packaging assumptions.

## Executable bindings

Compilation requires the complete verified plan-completion contract, not a caller-invented hash, plus the complete accepted route receipt whose payload recomputes to `routeReceiptSha256`. Each target stores the accepted `selectedStrategyId`; result validation rejects any other strategy. `topChoices` contains three manageable options and `allChoices` retains every ranked Advanced option. Goal state is never consulted.

Acceptance requires every target artifact kind, checksum-addressed artifact IDs, install/launch/update/uninstall/rollback evidence, the release manifest, SBOM, provenance, CI reproduction, and documentation matrix. `experimental` is visible but cannot be accepted as a completed Launcher result.
