# Transposition contract — SolForge Prompt Single

Preserve the source prompt's section order and rhetorical form while translating its task-specific language into the user's domain.

## Required semantic roles

1. `Current task statement` opening.
2. Precise domain definitions needed to remove ambiguity.
3. Direct statement of the complete requested outcome.
4. Edge cases, permitted variants, and boundary conditions.
5. Exact acceptance target, including assumptions the user explicitly supplied.
6. A paragraph explaining what partial progress does not count, with task-specific examples.
7. A genuinely diverse portfolio of task-relevant approaches.
8. Early independence among single-agent reasoning branches or passes.
9. An explicit registry of approach families.
10. A warning against elegant reductions that merely defer the core difficulty.
11. A blocked-route rule requiring a materially new mechanism before reopening.
12. Several incompatible routes kept alive through multiple rounds.
13. A task-specific adversarial checklist derived from the user's definitions, edge cases, failure modes, and likely false positives.
14. Concrete-output requirements: artifacts, lemmas, diffs, tests, equations, sources, constructions, or counterexamples as appropriate.
15. Repeated synthesis, challenge, redirection, and fresh rounds by the single primary agent.
16. Persistence language preventing return merely because early approaches fail.
17. A terminal condition requiring the complete outcome to survive adversarial audit, with truthful external-blocker handling.
18. A prohibition on substituting reductions, partial results, isolated gaps, or difficulty explanations unless the user requested them.
19. Gap-driven continuation rather than a fabricated wall-clock promise.
20. A task-appropriate public-search rule consistent with the user's scope and current source requirements.

## Fidelity rules

- Preserve sentence patterns and force from `source-prompt.md` wherever they remain truthful.
- Replace CDC nouns, definitions, special cases, insufficiency examples, audit checks, and search restrictions with user-task analogues throughout the document.
- Do not merely paste a normalized intent above a generic orchestration tail.
- Do not leave graph-specific language unless the user's task is actually about graphs.
- Do not add scope, permissions, facts, or success criteria unsupported by the user.
- Keep higher-priority instructions, safety boundaries, and real tool limits controlling.
- Replace agent nouns with `reasoning branch`, `approach pass`, or `audit pass`; explicitly prohibit imaginary subagents.
