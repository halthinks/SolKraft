---
name: inforge-run-multi
description: Execute a validated InForge Multi execution capsule with real Codex desktop agents, bounded ownership, evidence-bearing handoffs, root integration, and adversarial acceptance. Use when a user explicitly requests multi-agent execution of an InForge capsule or a complex authorized task needs independent parallel workstreams in the Codex desktop runtime.
---

# InForge Run Multi

Execute only a capsule whose profile is `multi`. Never simulate agents or describe sequential reasoning as multi-agent execution.

## Required workflow

1. Read [multi-execution-policy.md](references/multi-execution-policy.md) completely. Run `python scripts/verify_bundle.py`; stop if bundle integrity fails.
2. Read [execution-policy.md](references/execution-policy.md). Run `python scripts/validate_capsule.py <capsule.json> --check-sources`; reject stale, altered, mismatched, or authority-expanding input. Initialize `scripts/execution_state.py init <capsule.json> <state.json>`.
3. Verify that real Codex desktop agent tools and capacity are available. Record runtime evidence; stop with an exact capability blocker otherwise.
4. Retain root ownership of the capsule, scope, agent registry, mutation authorization, integration, verification, and terminal result.
5. Allocate independent workstreams dynamically within current runtime limits. Give each agent only its bounded task, requirement IDs, resources, permissions, and evidence obligations.
6. Record agents, workstreams, resource ownership, and handoffs using [agent-registry.schema.json](references/agent-registry.schema.json). Run:

   `python scripts/validate_multi_registry.py <registry.json> --capsule <capsule.json>`

7. Preserve early independence. Do not reveal other agents' conclusions until each assigned approach has produced evidence or an exact blocker.
8. Assign one owner to each resource or workstream. Serialize mutations whenever ownership or write scope could conflict.
9. Accept handoffs only when they contain task, scope, read/write classification, authorization basis, commands or tools, timestamps, results, supported evidence, uncertainties, and next safe action. Treat summaries as orientation, never evidence.
10. Integrate centrally. The root agent must inspect evidence, reconcile conflicts, record requirement evidence through `execution_state.py evidence`, rerun integrated verification, and conduct the final adversarial acceptance audit.
11. Run `python scripts/acceptance_audit.py <capsule.json> <state.json> --complete`. Return `complete`, `blocked`, or `declined` only under the shared execution contract. Never convert partial agent success into root completion.

## Hard stops

- Stop if the profile is not `multi`.
- Stop if real agent capability cannot be verified.
- Stop before an unconfirmed high-consequence action.
- Stop a workstream that exceeds its assigned scope or authority.
- Reject duplicate or conflicting ownership, unknown requirement IDs, unsupported statuses, and evidence-free handoffs.
- Never accept an agent's assertion, status message, or prose summary as proof of completion.

Run `python scripts/selftest_multi.py` after changing this profile.
