# Validation evidence

The current local release gate passed **75 Python regression tests**, three Node setup behavior tests, and a separate real MCP integration test against the built wheel and packaged plugin. Earlier validation evidence below records previous revisions and test counts.

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

The earlier console revision was exercised in a browser for disconnected catalog browsing, pagination through the final five-item page, page-size changes, empty search, lazy skill retrieval, resource inspection, request copying, and the three-stage worked example. That revision used Mermaid and a pause control; both were subsequently replaced by vertical HTML cards. Earlier GitHub verification runs passed. Current builds and tests run locally; Pages only uploads generated static files. A hosted API requires an operator deployment and key; successful local MCP tests do not establish external availability.


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

That implementation revision's complete suite passed **74 tests**. The integration environment reused installed dependencies; a clean dependency download was not part of that local wheel check. Its GitHub verification run independently installed declared dependencies on Linux. Current automatic GitHub test runs are disabled.

Browser checks confirmed large vertical cards (29px headings on desktop), sequential delays from 0 to 9 seconds, connector pulses preceding the next card, and no pause button or Mermaid renderer. The walkthrough is an illustration, not execution telemetry. Reduced-motion settings reveal the complete static flow. The static catalog and precomputed example remain available without a server.

Remote GitHub marketplace installation also succeeded with `--sparse .agents/plugins --sparse plugins/solkraft`. An initial full checkout failed on Windows path lengths in the nested test profile; the documented sparse install avoids that failure. The remote installed copy passed the same real stdio test. Browser-to-local-API connection and live three-stage routing passed; the 390px layout had 25px headings without horizontal overflow. GitHub verification and Pages deployment passed for the implementation commit.

## Interactive setup and local gate

The connection walkthrough has three paths: Render (five steps), API/MCP (five), and local plugin (four). Step navigation is bounded; platform selection changes installation and REST commands; endpoint validation rejects insecure remote URLs, credential/query-bearing URLs, endpoint paths, and shell metacharacters in hostnames. Behavior tests were written before implementation and observed failing, then passing. A separate red/green test establishes that the local gate records a nonzero build step and raises rather than proceeding as success.

Executed `python -m scripts.local_ci` on Windows with Python 3.11.9: 75 Python/router tests, three Node behavior tests, compilation and JavaScript syntax checks, static generation, plugin packaging, wheel construction, isolated wheel installation, outside-checkout catalog inspection, and one real packaged-plugin MCP integration test all passed. The gate writes an ignored machine receipt at `build/local-ci.json`. Artifact environments reuse installed dependencies; this does not prove fresh dependency resolution. No WSL or Omarchy execution is claimed.

Browser checks exercised all three setup paths, Windows/Linux instruction switching, copy feedback, automatic sequence completion at step five, manual step selection, keyboard arrow selection, endpoint handoff to the real console, authenticated local API connection, and real three-stage routing. The 390px mobile layout exposed an initial grid overflow; the repaired layout measured 375px document width and 275px scene width, with 28px scene titles and no horizontal page overflow. Browser error/warning logs were empty. No Render deployment was performed; hosted setup steps are based on the repository Blueprint and current Render documentation.
