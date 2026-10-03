# Validation evidence

The service and bundled parser have 73 passing regression tests. These cover intentional abstention, release-gate context, explicit skill selection, catalog-wide graph visibility, supporting resource containment, authentication, and real mounted MCP initialization and routing.

Run the same suite:

```sh
python -m pip install -e ".[dev]"
SOLFORGE_TEST_ROOT=solkraft/skillpacks python -m pytest -q tests solkraft/skillpacks/solforge/tests -p no:cacheprovider
node --check docs/assets/app.js
node --check docs/assets/flow.js
python -m compileall -q solkraft
```

On PowerShell, set `$env:SOLFORGE_TEST_ROOT = 'solkraft/skillpacks'` before pytest.

The reproducible routing battery runs through the public Python routing interface:

```sh
python -m scripts.routing_battery
```

Its checked-in receipt is `scripts/results-routing-100000.json`: 100,000 passing requests across ten domains, 10,000 per domain. Every prompt contains at least 200 words. Each domain checks prompt uniqueness, expected ordered skills, retained effect exclusions, absence of unresolved requested stages, and advisory authority.

These are systematically generated combinations of stage phrases and context variants. They provide regression coverage, not a statistically representative sample of unrestricted human requests, proof of universal understanding, or a measured twofold improvement. The suite does not establish correctness of every engineering procedure or completion of work performed by a host agent.

The console was exercised in a browser for disconnected catalog browsing, pagination through the final five-item page, page-size changes, empty search, lazy skill retrieval, resource inspection, request copying, and the three-stage worked example. The Mermaid SVG rendered with seven animated edges, readable labels, and a functioning pause control. These checks validate the static walkthrough; they do not establish availability of an external API. GitHub Actions runs the regression suite and deploys the static console. A hosted API requires an operator deployment and key; successful local MCP tests do not establish external availability.
