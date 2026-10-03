# Ultra execution policy

Native Ultra is a capability, not a label. Execution is forbidden until the runtime capability and a user-authored authorization are both verified.

## Required hard ceilings

- `max_elapsed_seconds`
- `max_tool_calls`
- `max_rounds`
- `max_agents`
- `max_cost_usd`

Every ceiling must be finite and nonnegative; counts and elapsed time must be positive. The approved budget is hashed and bound to the execution capsule.

## Authorization

The authorization record must contain the capsule SHA-256, budget SHA-256, user-authored confirmation text, confirmation time, and `authorized_by: user`. The executing agent must not manufacture or infer authorization.

## Extensions

An extension must preserve the old budget hash, name the new budget hash, state the exact increases and reason, and contain new user-authored confirmation. Never silently roll unused capacity between capsules.

## Termination

Stop immediately on capability loss, user kill, any exceeded ceiling, unsafe scope change, missing confirmation, or invalid/stale evidence. Termination does not authorize cleanup mutations unless they were already explicitly included in the confirmed rollback plan.
