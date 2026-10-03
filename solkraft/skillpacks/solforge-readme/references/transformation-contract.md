# Whitepaper-to-README transformation contract

## Reading layers

| Layer | Reader question | Required content |
|---|---|---|
| Thirty seconds | What is this, who is it for, and why should I care? | Product identity, primary user, problem, differentiator, status. |
| Five minutes | Can I use it, and how does it work? | Quick start, capability map, architecture, example workflows, requirements, trust boundary. |
| Deep | Can I verify, operate, extend, or govern it? | Linked architecture, capability, security, evidence, limitations, and source material. |

## Irreducible identity

Extract and source-bind:

1. product category;
2. primary reader or user;
3. core problem;
4. unique mechanism; and
5. evidence-backed differentiator.

If the source does not support one of these, label the gap. Do not fill it with marketing language.

## Root README hierarchy

Prefer this order unless the repository type materially requires another:

1. hero and one-sentence identity;
2. overview and value;
3. quick start with verified commands;
4. capability map;
5. how it works;
6. one or two representative workflows;
7. trust, security, authority, availability, and limitations;
8. documentation map;
9. contribution and license when source-supported; and
10. source or release provenance.

## Compression rules

- Preserve material distinctions and exact availability.
- Remove repeated argumentation and duplicated evidence exposition.
- Convert repeated mappings into tables.
- Use one useful architecture visual when relationships are otherwise difficult to scan.
- Move mechanisms, evidence tables, policy detail, and long limitations into linked documents.
- Keep the root statement that tells the reader why each boundary matters.
- Never turn a limitation into a benefit claim, an internal module into a public product, or an authorized effect into a completed effect.

## Mandatory package

- `README.md`
- `docs/architecture.md`
- `docs/capabilities.md`
- `docs/security-and-authority.md`
- `docs/readme-claim-manifest.json`
- `docs/readme-compression-report.md`
- the embedded source document at its declared repository-relative path
- `readme-package.json`
- `readme-result-receipt.json`

The claim manifest stores and hashes each material README paragraph and its exact indexed source excerpt so validation can recompute both sides. The compression report gives every source section one unambiguous treatment and destination. The package and result receipts bind the accepted route, plan-completion hash, source, outputs, and exact effect-plan authority. Goal state is not part of the contract. Local package creation never implies an external effect, while an explicitly displayed and accepted commit, push, publication, deployment, hosting, or disclosure step remains executable without duplicate approval so long as its provider, account, target, permission, and revision have not changed.

## Acceptance gates

Block acceptance for any of these conditions:

- missing required output;
- nonexistent or broken relative link;
- absent, placeholder, destructive, or unsupported quick-start command;
- capability name that does not exist on the live public registry surface;
- material claim without a source binding;
- omitted source security, authority, privacy, risk, or limitation boundary;
- claimed availability unsupported by live evidence;
- proprietary-only rendering required to understand the README;
- missing accessible explanation for a material visual; or
- changed source hash after compilation.
