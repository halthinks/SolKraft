---
name: hardware-product-pipeline
description: >-
  Run the six finished hardware skills as one product pipeline, from new-part
  selection through a preserved register, build-closure matrix, CAD-bound
  realization, and honest evidence claims. Use when starting or auditing a
  0-to-1 hardware product. Do not treat pcb-generation as a finished release
  factory. Never substitute parts to close a gap.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Hardware Product Pipeline

One product root. Six skills. Existing validators. No invented readiness.

This is the operating loop. It does not replace the six skills. It sequences
them and refuses a claim the current artifacts cannot support.

`pcb-generation` is an unfinished board hook, not a seventh gate. A pcb-toolchain
preview, a generated board, or this skill existing is not fabrication evidence.

## The six skills

| Stage | Skill | Artifact the next stage consumes |
|---|---|---|
| 0 Authority | `evidence-bound-product-pipeline` | classified sources, decision log, open conflicts |
| 1 Select | `select-and-validate-hardware-parts` | one `decision.json` per new part |
| 2 Preserve | `preserve-engineering-selections` | `selection-register.json` |
| 3 Build matrix | `build-selected-hardware-product` | `build-closure-matrix.json` |
| 4 Realize | `realize-hardware-product` | `product-realization-manifest.json` plus analysis/acceptance files |
| 5 CAD bind | `realize-cad-bound-product` | master assembly, render lineage, same product root |

Run the named skill at that stage. This skill only checks handoffs.

## Product root

```text
<product-root>/
  # optional product metadata file; not created or required by this skill
  authority/decision-log.json
  authority/evidence-index.json
  requirements.json
  decisions/<selection_id>.json
  selection-register.json
  build-closure-matrix.json
  product-realization-manifest.json
  geometry/
  analysis/
  acceptance/
  presentation/
  pipeline-status.json
```

Product identity, profile, revision, claimed stage, and claimed closure are inputs to the pipeline runner and resulting status artifacts. Do not require an undeclared `pipeline.json`; if a host/project supplies equivalent metadata, treat it as input rather than proof.

## Stage rules

0. Classify every inherited file before adopting it. Historical CAD, renders,
   and BOMs stay `HISTORICAL` or `CANDIDATE` until exact revision, hash, and
   gate are recorded. Do not global-replace old product names.

1. New parts start at select. Requirements and electronic budgets first. At
   least two real MPNs. Hard gates before scores. `SELECTED` is illegal while
   any validation gate is not `PASS`. Run
   `select-and-validate-hardware-parts/scripts/validate_part_decision.py`.

2. Feed passing decisions into the register. Never silently substitute, rename,
   merge, or delete a row. Missing schematic/PCB/firmware/CAD means implement
   that layer, not reopen the part. Run
   `preserve-engineering-selections/scripts/validate_selection_register.py`.

3. Expand the register with
   `build-selected-hardware-product/scripts/build_closure_matrix.py`. Keep every
   selection ID. Do not drop an open row to improve the score.

4. Realize the locked rows as one electrical/mechanical/thermal package. Use
   `realize-hardware-product` closure levels only:
   `CONCEPT`, `SOURCE_BOUND`, `DIGITAL_CLOSED`, `FIRST_ARTICLE_READY`,
   `PHYSICALLY_VERIFIED`. Run
   `realize-hardware-product/scripts/validate_realization.py MANIFEST --root ROOT`.

5. Bind CAD as geometry authority. Envelopes and keep-outs before the shell.
   Renders come from released meshes. Run
   `realize-cad-bound-product/scripts/validate_realization.py ROOT`.
   Do not say fabrication-ready, measured, or production-ready unless the
   physical records exist.

## Claim ceiling

The supported claim is the highest stage whose validators passed and whose
open gates do not contradict the claim. A lower-stage pass never lifts a
higher-stage label.

Build readiness words (`DESIGN_COMPLETE` … `RELEASE_READY`) and realize
closure words are not interchangeable. Report both. Never use a matrix cell,
a datasheet, a host test, a render, or a plan as physical proof.

## Commands

From this skill folder, or any copy of `scripts/run_pipeline.py`:

```text
python scripts/run_pipeline.py init <product-root> --product NAME --profile PROFILE --revision REV
python scripts/run_pipeline.py check <product-root>
python scripts/run_pipeline.py status <product-root>
```

`init` writes empty honest templates. It does not select parts.
`check` runs every existing sibling validator against present artifacts and
writes `pipeline-status.json`.
`status` reprints the last check.

`--skills-root` defaults to this skill's parent folder
(`<configured-path>` when installed there).

## Stop conditions

Pause promotion, not safe digital work, when:

- a required artifact for the claimed stage is missing
- a validator returns FAIL
- a selected part has no exact MPN, order path, or dimensional evidence
- a `SELECTED` row has an unresolved gate
- PCB work is being treated as released through unfinished `pcb-generation`
- a render, calculation, or host test is being used as physical evidence

Record the blocked gate, the work that can continue, and the exact evidence
needed to resume promotion.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
