/* Execute production Python in a worker; no surrogate browser matcher. */
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/';
let runtimePromise;

function runtime() {
  if (!runtimePromise) runtimePromise = (async () => {
    self.postMessage({ type: 'progress', message: 'Loading the Python routing engine…' });
    importScripts(`${PYODIDE_URL}pyodide.js`);
    const python = await loadPyodide({ indexURL: PYODIDE_URL });
    await python.loadPackage('pyyaml');
    const response = await fetch(new URL('router-runtime.zip', self.location.href), { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Routing package download failed (${response.status})`);
    python.unpackArchive(await response.arrayBuffer(), 'zip', { extractDir: '/solkraft-runtime' });
    python.runPython(`
import sys, json
sys.path.insert(0, '/solkraft-runtime')
from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request
_browser_catalog = SkillCatalog([BUNDLE_ROOT])
def _browser_route(request_json):
    request = json.loads(request_json)
    return json.dumps(route_request(_browser_catalog, request['objective'], request['max_skills'], policy={'contract_mode': 'hardened'}))
`);
    return python;
  })().catch(error => { runtimePromise = undefined; throw error; });
  return runtimePromise;
}

// A queue prevents overlapping requests from sharing Python request state.
let queue = Promise.resolve();
self.onmessage = (event) => {
  const { id, objective, max_skills } = event.data;
  queue = queue.then(async () => {
    try {
      const python = await runtime();
      const routeFunction = python.globals.get('_browser_route');
      try {
        const route = JSON.parse(routeFunction(JSON.stringify({ objective, max_skills })));
        self.postMessage({ id, route });
      } finally { routeFunction.destroy(); }
    } catch (error) {
      self.postMessage({ id, error: error.message || String(error) });
    }
  });
};
