# DayQ build-first contract

## Objective

Maximize playable DayQ progress. Target roughly 80 percent implementation and play, 10 percent focused smoke testing and repair, and 10 percent planning and reporting.

## Work selection

Always prefer the smallest change that extends a real player route. Build in dependency order, but satisfy dependencies at prototype quality until the route proves they deserve production depth.

Before implementation, select every applicable named route from `dayq/data/DAYQ_SKILL_REGISTRY.json` with `python dayq/scripts/dayq_skill_registry.py plan --route <name>`. The returned ordered skill set is mandatory for that milestone. The orchestrator coordinates those skills; it never replaces them.

## Severity queue

| Priority | Meaning | Action |
|---|---|---|
| P0 | build failure, crash, data loss, security or severe authority exploit | fix now |
| P1 | current playable route is broken | fix now |
| P2 | nonblocking defect or incomplete secondary path | defer and continue |
| P3 | polish, exhaustive evidence, documentation, or speculative hardening | backlog |

## Validation tiers

### Routine change

- compile the affected target;
- run one focused PIE smoke route;
- capture only the command and result.

### Subsystem milestone

- run directly relevant focused automation;
- run one representative PIE route;
- retain at most one representative screenshot or log plus a short result.

### Integration milestone

- perform the subsystem milestone checks;
- add a two-client authority route only when networking or ownership changed;
- add save/restart only when persistent state changed;
- run a short adjacent-system regression, not the entire project suite.

### Release candidate

- run the complete validation contract;
- include performance, fault injection, cohort playtests, and release evidence as applicable.

## Asset policy

Grayboxes, primitives, labels, starter materials, and temporary audio are valid gameplay prototypes. They do not require an immutable asset-factory job. Create the governed production job when the mechanic is stable enough to define the asset contract, the geometry itself is mechanic-critical, or the asset is being promoted for release. Imported third-party sources still require provenance and license review before use.

## Truth and stopping

Never claim an unrun check passed. `Deferred` is a valid status for noncritical work. Stop only for a real authority boundary, unavailable required external capability, or a blocker with no safe local workaround. A missing optional proof artifact is not a blocker.
