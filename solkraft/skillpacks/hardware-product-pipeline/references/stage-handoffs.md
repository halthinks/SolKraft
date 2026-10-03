# Stage handoffs

These are the only machine handoffs this pipeline recognizes.

1. `decisions/<selection_id>.json` must pass `validate_part_decision.py`.
2. `selection-register.json` must pass `validate_selection_register.py` and contain rows.
3. `build-closure-matrix.json` is generated from the register by `build_closure_matrix.py`. Every selection ID is retained.
4. `product-realization-manifest.json` must pass `realize-hardware-product` `validate_realization.py`.
5. The same product root must pass `realize-cad-bound-product` `validate_realization.py`.

`pcb-generation` is not a handoff. It cannot satisfy fabrication, manufacturer, first-article, or production claims.
