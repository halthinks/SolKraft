// Run after npm install --prefix build/browser-router-check --no-save pyodide@0.29.3.
// Tests production Python in WebAssembly without controlling a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { loadPyodide } = require('../build/browser-router-check/node_modules/pyodide');
(async () => {
  const messages = [];
  const context = {
    URL, Promise, JSON, console,
    self: { location: { href: 'https://example.test/assets/router-worker.js' }, postMessage: value => messages.push(value) },
    importScripts: () => {},
    // Node uses its installed runtime directory; browsers use the pinned CDN.
    loadPyodide: () => loadPyodide(),
    fetch: async () => ({ ok: true, arrayBuffer: async () => Uint8Array.from(fs.readFileSync('docs/assets/router-runtime.zip')).buffer }),
  };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync('docs/assets/router-worker.js', 'utf8'), context);
  context.self.onmessage({ data: { id: 1, objective: 'Inspect the codebase, diagnose the crash, build the fix and test it', max_skills: 10 } });
  await vm.runInContext('queue', context);
  const result = messages.find(value => value.id === 1);
  assert.equal(result.error, undefined);
  assert.equal(result.route.execution_authorized, false);
  assert(result.route.selected.includes('solforge-workflow-software-diagnose'));
  assert(result.route.selected.includes('solforge-workflow-software-test'));
  context.self.onmessage({ data: { id: 2, objective: '', max_skills: 10 } });
  await vm.runInContext('queue', context);
  assert.match(messages.find(value => value.id === 2).error, /non-empty/);
  context.self.onmessage({ data: { id: 3, objective: 'Run software tests', max_skills: 10 } });
  await vm.runInContext('queue', context);
  assert.equal(messages.find(value => value.id === 3).route.execution_authorized, false);
  console.log(JSON.stringify({ runtime: 'Pyodide 0.29.3', selected: result.route.selected, invalidRequest: 'rejected', subsequentRequest: 'passed' }));
})().catch(error => { console.error(error); process.exitCode = 1; });
