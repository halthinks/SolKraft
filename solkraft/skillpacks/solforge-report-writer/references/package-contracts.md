<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Report package contracts

## Package selection

| ID | Package | Mandatory sections |
|---|---|---|
| RR-O01 | Academic research paper | Abstract, introduction, methods, results, discussion, limitations, references, appendices |
| RR-O02 | Technical whitepaper | Executive summary, problem, architecture or method, evidence, findings, risks, recommendations |
| RR-O03 | Literature review | Search protocol, inclusion and exclusion, evidence table, synthesis, disagreements, gaps |
| RR-O04 | Due-diligence report | Scope, source quality, claims, red flags, counterevidence, uncertainties, decision implications |
| RR-O05 | Evidence brief | Question, key findings, strongest evidence, contradictions, uncertainty, sources |
| RR-O06 | Executive report | Decision, findings, implications, options, risks, actions, technical appendix |
| RR-O07 | Methods appendix | Data, transformations, prompt and contract references, tools, assumptions, tests, limitations |
| RR-O08 | Reproducibility package | Source manifest, hashes, search log, event receipt, claim graph, methods, exports |

## Universal acceptance record

Record:

- report ID, package ID, schema version, report version, capsule hash, and claim-graph hash;
- section completion and section owner;
- citation style and per-citation metadata result;
- unsupported-claim, contrary-evidence, uncertainty, and limitation findings;
- reviewer identity, decision, decision time, and receipt hash;
- requested exports and semantic parity results.

Block acceptance for a missing mandatory section, nonexistent citation, unsupported material claim, omitted material counterevidence, hidden material uncertainty, stale capsule, absent reviewer receipt, or export mismatch.

## Production standards

The package determines document structure. The production standard determines depth, interaction, review, visuals, and exports. Both are mandatory and independently hash-bound.

| Standard | Reader promise | Interaction | Review | Minimum visuals | Required exports |
|---|---|---|---|---|---|
| Concise | Decision-ready evidence without unnecessary ceremony | No extra dialog | Evidence audit | None unless evidence needs one | Markdown |
| Professional Handoff | Transfer ownership with architecture, measured gains, maintenance rules, production boundaries, and next actions | Clarify material gaps | Handoff acceptance | 1 chart and 1 visual aid | Markdown, PDF, DOCX |
| Collegiate | Formal, citation-disciplined argument suitable for advanced coursework or institutional review | Clarify, then section review | Editorial acceptance | 1 chart and 2 visual aids | Markdown, PDF, DOCX |
| Scientific | Methods-first, reproducible research with formal figures, limitations, contrary evidence, and review | Method, evidence, and acceptance gates | Scientific reviewer acceptance | 2 charts and 2 visual aids | Markdown, PDF, DOCX, hosted |

Never silently promote or demote a standard. A production-standard change requires a new widget selection and configuration hash.
