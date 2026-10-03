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


## Plugin and vertical walkthrough verification

For this change, the new stdio test was written first and failed because the plugin was absent. After packaging, it exposed a missing runtime in the subprocess environment; the plugin now launches the installed `solkraft` console command. A wheel was built and installed into an isolated environment, and the Codex CLI installed `solkraft@solkraft` from the repository marketplace into an isolated profile.

The installed plugin configuration was then exercised with a real MCP client outside the checkout. Initialize, list tools, search, repository-release-gate routing, selected-skill retrieval, supporting-resource retrieval, and catalog graph retrieval all passed. The subprocess imported the installed wheel and returned 173 catalog entries. This proves transport and artifact integration, not universal model selection or public API availability.

Executed commands:

```sh
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
python -m venv --system-site-packages build/plugin-env
# Install the wheel in that environment; dependencies reused from the host.
python -m pip install --no-deps --force-reinstall dist/solkraft-0.1.0-py3-none-any.whl
codex plugin marketplace add . --json
codex plugin add solkraft@solkraft --json
# With the installed runtime on PATH, installed plugin root selected,
# and SOLFORGE_TEST_ROOT=solkraft/skillpacks:
python -m pytest -q tests solkraft/skillpacks/solforge/tests -p no:cacheprovider
python -m compileall -q solkraft
node --check docs/assets/app.js
node --check docs/assets/flow.js
python -m scripts.build_console
python scripts/package_plugin.py
```

The complete suite passed **74 tests**. The integration environment reused installed dependencies; a clean dependency download was not part of that local wheel check. GitHub CI independently installs declared dependencies on Linux.

Browser checks confirmed large vertical cards (29px headings on desktop), sequential delays from 0 to 9 seconds, connector pulses preceding the next card, and no pause button or Mermaid renderer. The walkthrough is an illustration, not execution telemetry. Reduced-motion settings reveal the complete static flow. The static catalog and precomputed example remain available without a server.
