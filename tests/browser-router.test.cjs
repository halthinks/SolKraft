const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function adapter() {
  const workers = [];
  class Worker {
    constructor(url) { this.url = url; workers.push(this); }
    postMessage(data) { this.request = data; }
    terminate() { this.terminated = true; }
  }
  const window = { dispatchEvent() {} };
  const context = { URL, Worker, window, document: { currentScript: { src: 'https://example.test/assets/browser-router.js' } },
    CustomEvent: class {}, setTimeout, clearTimeout };
  vm.runInNewContext(fs.readFileSync('docs/assets/browser-router.js', 'utf8'), context);
  return { route: window.composeSolKraftBrowserRoute, workers };
}

test('returns production result and delivers startup progress', async () => {
  const { route, workers } = adapter();
  const progress = [];
  const request = route('Test the software', 10, message => progress.push(message));
  workers[0].onmessage({ data: { type: 'progress', message: 'Loading' } });
  workers[0].onmessage({ data: { id: workers[0].request.id, route: { selected: ['test'], execution_authorized: false } } });
  assert.equal((await request).execution_authorized, false);
  assert.deepEqual(progress, ['Loading']);
});

test('worker failure rejects pending request and a retry creates a new worker', async () => {
  const { route, workers } = adapter();
  const request = route('Test the software');
  workers[0].onerror();
  await assert.rejects(request, /could not load/);
  assert.equal(workers[0].terminated, true);
  const retry = route('Test the software');
  assert.equal(workers.length, 2);
  workers[1].onmessage({ data: { id: workers[1].request.id, route: { selected: [] } } });
  await retry;
});

test('empty objective rejects before loading runtime', async () => {
  const { route, workers } = adapter();
  await assert.rejects(route('  '), /Enter a request/);
  assert.equal(workers.length, 0);
});
