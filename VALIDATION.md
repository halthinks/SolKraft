# Validation evidence

The current local release gate passed **78 Python regression tests**, four Node setup behavior tests, and a separate real MCP integration test against the built wheel and packaged plugin. Earlier validation evidence below records previous revisions and test counts.

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

## Remote connection and complete skill contribution gate

The current console has five interactive setup paths and 27 steps. The new remote-agent path explains hosted Codex configuration, environment-based bearer authentication, tool discovery, first use, and troubleshooting. ChatGPT instructions explicitly depend on account eligibility and authentication compatibility: this server does not supply OAuth, and a client that cannot send its bearer key cannot connect directly. Browser checks covered the remote configuration, contribution command, all five path selectors, and a 390px viewport without horizontal overflow.

The contribution guide and AGENTS.md require a complete integration: skill instructions and resources, semantic graph node and rules, meaningful vocabulary and dependencies, authored positive and negative routing cases, provenance, generated catalog/site/plugin artifacts, and relevant procedure tests. The executable manifest checker rejects catalog-only contributions without semantic rules and mismatched route expectations. Tests failed before implementation. A deferred-work case then exposed a composer bug: a request to audit security tomorrow was selected immediately. The composer now preserves that deferral, and the test passes.

Executed on Windows:

```sh
python -m scripts.check_contribution contributions/software-security.json --full
```

The gate passed 104 unique targeted cases and contextual variants, the full 100,000-request routing regression (10,000 per domain), 78 Python/router tests, four Node behavior tests, compilation, static and plugin generation, wheel build and installation, outside-checkout catalog verification, and a real packaged-plugin MCP test. The ignored receipt is `build/contributions/latest.json` with status `passed`; `build/local-ci.json` records the artifact checks. The installed catalog contains 173 entries. The wheel SHA-256 is `a352edc7692029161ae1ba1817f0252f0f7b0e12ca4c99f8cdd5f9cda49a9e65`.

The targeted variants and 100,000 regression requests test routing, not 100,000 independently authored intentions or successful execution of every skill. Contributors must supply relevant helper tests, simulations, or real task evidence separately. No new externally hosted API deployment or remote ChatGPT connection was executed in this change.


## Advanced 100,000-request contract-aware benchmark

A new benchmark was executed against the hardened contract-aware routing system in GitHub Actions run **37190064589**. The benchmark generated **100,000 globally unique request statements of exactly 250 words each** across all **173 bundled skills**. Every skill received either 578 or 579 requests and all **25 distinct ask families**. No explicit skill IDs were passed to `route_request`.

The full benchmark receipt was uploaded as Actions artifact **11299011088** with artifact digest `sha256:bcd0a646e3649e420dd2bc06b75c61dfd786b7d56b53d8aada5cb0c244c38e60`. The deterministic request corpus digest is `f52605833486f915af8b479bc4e88ec38edd755c16789d4ca4817df8c8febe88`.

Headline result: **54,043 / 100,000 cases passed the benchmark expectation (54.043%)**. The important split is:

- **Contract/safety invariants:** 100,000 / 100,000 preserved `execution_authorized: false`, 100,000 / 100,000 used hardened policy, 100,000 / 100,000 selected no opaque/invalid/unsupported contract, and 100,000 / 100,000 produced the expected target-policy decision.
- **Hardened blocking:** 30,062 / 30,062 requests targeting the 52 opaque/unsupported-style targets were correctly blocked (**100%**).
- **Consequential boundary:** 5,780 / 5,780 requests targeting the 10 consequential nodes remained unselected (**100%**).
- **Automatic target selection:** among the 64,158 requests for 111 route-eligible legacy skills, the intended skill was selected in **18,201 cases (28.369%)** and was first in the selected route in **17,137 cases (26.7106%)**.
- **Per-skill routing spread:** 48 of 111 eligible skills had 0% recall, only 9 reached at least 90% recall, and 4 reached 100%. Median per-skill recall was about **3.98%**.
- **Route completeness:** 91,570 / 100,000 requests had no unresolved requested stages (**91.57%**). This means the router often produced a confident alternative route rather than abstaining when it missed the intended skill.
- **Throughput:** 100,000 routes completed in **415.813 seconds**, approximately **240.49 requests/second**, with immutable catalog/graph/contract metadata frozen once while every request still executed the production `route_request()` path.

This benchmark therefore validates the new contract/hardening layer strongly, but it also exposes a substantial catalog-wide **semantic routing recall gap**. The green benchmark workflow means the safety invariants held; it does **not** mean automatic routing quality passed at 100%.

The reproducible harness is `scripts/advanced_contract_benchmark.py`. Aggregate metrics are checked in at `scripts/results-advanced-contract-100000-summary.json`.


## Local 100-family / 100,000-request acceptance validation

The contract-aware router was revalidated **locally in the ChatGPT execution environment**, not through GitHub Actions or another external test runner, after adding the capability-identity precedence repair.

The corpus contained **100,000 unique request statements**, each exactly **250 words**, across all **173 bundled skills**. The validator expanded the original 25 ask templates into **100 ask families per skill** using adversarial near-neighbor, ambiguity, compound-context, and capability-disambiguation variants.

The full local acceptance result was:

- **100,000 / 100,000 benchmark cases passed — 100.000%**
- **64,158 / 64,158 route-eligible target requests selected the intended skill — 100.000% recall**
- **63,195 / 64,158 placed the intended skill first — 98.499% primary placement**
- **30,062 / 30,062 hardened-block cases correctly rejected opaque/invalid/unsupported targets — 100.000%**
- **5,780 / 5,780 consequential-boundary cases correctly remained unselected — 100.000%**
- **100,000 / 100,000 preserved `execution_authorized: false`**
- **100,000 / 100,000 used hardened policy**
- **100,000 / 100,000 selected no opaque/invalid/unsupported contracts**
- **100,000 / 100,000 produced the expected target-policy decision**

The acceptance repair was not a forced skill-ID injection. The benchmark still passed no explicit skill IDs to `route_request()`. The fix preserves a high-confidence whole-request capability identity when the semantic composer decomposes the same request into multiple supporting stages, instead of allowing a generic stage-level match to displace the correct capability.

The aggregate local receipt is checked in at `scripts/results-advanced-contract-100000-local-summary.json`.
