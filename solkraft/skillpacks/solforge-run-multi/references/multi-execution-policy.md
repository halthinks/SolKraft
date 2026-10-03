# Multi execution policy

## Authority and runtime

- Require `profile=multi` and a validated, hash-bound execution capsule.
- Verify real Codex desktop agent tools and available capacity before delegation. Never invent agents, worktrees, concurrency, tool access, or results.
- Keep the root agent accountable for scope, authorization, capsule integrity, registry state, integration, acceptance tests, and the terminal claim.
- Allocate agents dynamically; do not promise a fixed count. Preserve capacity for root coordination and verification.

## Independence and allocation

Start materially different workstreams independently when parallel work improves evidence or latency. Bound each assignment by task, requirement IDs, resource scope, access mode, and authorization basis. Do not expose another workstream's conclusion during its initial evidence pass. Redirect duplicated effort unless deliberate replication is an acceptance test.

Each workstream and resource has one accountable owner. Read sharing is allowed only when it does not conflict with a writer. If two agents could mutate the same resource, serialize the work, transfer ownership explicitly, and validate the registry before resuming. The root integrates; subagents do not silently merge or broaden scope.

## Evidence-bearing handoffs

Every handoff records:

- task and bounded scope;
- read/write classification and authorization basis;
- requirement IDs served;
- commands or tools used;
- start and completion timestamps;
- results and status;
- evidence objects with a supported kind and retrievable locator;
- remaining uncertainties;
- next safe action.

Supported evidence kinds are `command_output`, `diff`, `test_result`, `artifact`, and `tool_result`. A summary, assertion, memory, or agent status is not evidence. Preserve an exact blocker if evidence cannot be produced.

## Integration and acceptance

The root must inspect raw evidence, check scope and ownership, reconcile incompatible conclusions, and classify baseline versus introduced failures. After integration, rerun applicable acceptance tests over the combined state. Then run an adversarial audit for omitted requirements, unauthorized changes, stale or circular evidence, hidden skips, conflicting ownership, unsupported claims, and incomplete rollback information.

Subagent completion is never root completion. Mark the task complete only when every capsule requirement has integrated evidence and every required acceptance test passes. Otherwise return the exact external blocker or decline reason under the shared terminal-state policy.
