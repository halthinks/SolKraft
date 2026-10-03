# Contributing to SolKraft

Thanks for contributing. Keep changes focused and add tests for behavior changes.

## Skill contribution provenance

A skill contribution must include:

- the author or upstream project and a stable source URL when available;
- the applicable license and confirmation that redistribution is allowed;
- attribution and notices required by that license;
- a concise purpose-oriented description in frontmatter;
- tests or examples showing when routing should and should not select it.

First-party skill contributions must be submitted under the repository license. Do not copy plugin cache content into the repository based only on local availability. Keep contributions within the repository's published scope and follow its agent and engineering contracts.

## Development checks

```powershell
pip install -e ".[dev]"
python -m pytest -q
```

The REST API and MCP server may return skill instructions as text. They must never execute them. New tools must preserve that read-only boundary and must not expose absolute server paths.
