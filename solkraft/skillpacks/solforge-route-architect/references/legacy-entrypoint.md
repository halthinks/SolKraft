---
name: solforge-route-architect
description: "Construct and rank executable, runtime-neutral routes from the complete live capability graph. Use directly for complex composition, dependency ordering, parallel waves, and route comparison."
---

# SolForge Route Architect

Construct and rank executable, runtime-neutral routes from the complete live capability graph. Use directly for complex composition, dependency ordering, parallel waves, and route comparison.

## Native execution

1. Preserve the user's objective, requested scope, supplied inputs, and current workspace state.
2. Inspect the real sources, files, tools, and runtime evidence needed for this capability.
3. Combine this skill with any number of compatible skills or workflows when that improves coverage or speed.
4. Perform the requested work directly with the active host's native tools. Recommendations never hide or disable other capabilities.
5. Verify the actual result in proportion to risk. A plan, queued job, preview, or partial check is not completion evidence.
6. Report concrete outputs, checks, remaining uncertainty, and any genuine external dependency.

## Open graph composition

- When the complete catalog would help, call `solforge_get_open_capability_graph`.
- To assemble a route, call `solforge_compose_open_capability_route` with an objective, any explicit skill or workflow IDs, or the include-all options.
- Treat ranked capabilities and dependency waves as useful suggestions. Add, remove, reorder, or combine capabilities whenever the objective benefits.
- Execute the selected native skills directly; graph composition creates no separate planning gate.

## Composition behavior

- Capability tags: `solforge`, `native`, `composable`, `orchestration`.
- There is no SolForge fan-out limit. Use one, several, or all useful capabilities.
- Dependencies guide ordering only; they do not make a capability unavailable.
- Independent work may run in parallel when ownership and integration are clear.
- Apply direct user Pause, Resume, and Stop instructions immediately.
- For external or destructive effects, require that the current user request names the exact effect and target, then follow ordinary host safeguards at effect time.
