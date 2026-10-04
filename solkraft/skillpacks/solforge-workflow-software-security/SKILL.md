---
name: solforge-workflow-software-security
description: "Review code for vulnerabilities, trust-boundary failures, unsafe input handling, and exploitable behavior; tie findings to concrete evidence."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Audit software for vulnerabilities

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the audited revision, the scope boundaries and exclusions, and the acceptance criteria — including what counts as a finding and whether live exploitation, dependency upgrades, or configuration changes are in scope. Enumerate the trust boundaries before reading code: where untrusted input enters (requests, files, environment, messages, deserialized data), where authority is checked, where secrets or credentials live, and which third-party dependencies are loaded with what privileges.

Follow data from entry points to sinks rather than scanning for patterns alone. At each crossing of a trust boundary, check for validation, escaping, and authorization: query and command construction, path and template handling, deserialization, redirect and server-side fetch targets, cryptographic use and key handling, session and token lifecycle, and error paths that leak internals. Check recent changes and configuration first when the audit follows an incident. Rank by exploitability and reachable impact, not by linter severity; verify each claimed mitigation actually exists in the code rather than assuming it.

Every reported finding names the file and location, the reachable input path, and a credible impact; a pattern match without a reachable sink is a hypothesis, not a vulnerability, and is reported as such. Do not inflate one root cause into many findings, do not claim demonstrated exploitation you did not perform, and do not report "no findings" without stating which surface and depth you actually covered — absence of findings is only as strong as the coverage behind it. When remediation is performed, verify with a check that exercises the original unsafe input path, not merely that the suspicious construct is gone.

Return the audit: confirmed findings with evidence and severity, hypotheses needing deeper access, remediation performed or proposed, and the uncovered surface or residual risk. Use [repository investigation](../solforge-codebase/SKILL.md) only when tracing a data flow to its sink requires deeper exploration.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
