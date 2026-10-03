const { test } = require('node:test');
const assert = require('node:assert/strict');
const { paths, normalizeEndpoint, stepAt, commandFor } = require('../docs/assets/setup.js');
const { createStaticLoader } = require('../docs/assets/static-data.js');

test('browser loads the bundled-data loader before its consumer', () => {
  const html = require('node:fs').readFileSync(require('node:path').join(__dirname, '../docs/index.html'), 'utf8');
  const loader = html.indexOf('src="assets/static-data.js');
  assert.ok(loader > 0 && loader < html.indexOf('src="assets/app.js'));
});

test('bundled data shares concurrent requests and reuses successful results', async () => {
  let calls = 0;
  const load = createStaticLoader(async (path, options) => {
    calls++;
    assert.equal(options.cache, 'no-cache');
    return { ok: true, json: async () => ({ path }) };
  });
  const [first, second] = await Promise.all([load('catalog.json'), load('catalog.json')]);
  assert.equal(first, second);
  assert.equal(await load('catalog.json'), first);
  assert.equal(calls, 1);
  await load('graph.json');
  assert.equal(calls, 2);
});

test('failed bundled requests can be retried, including malformed JSON', async () => {
  for (const failure of ['http', 'json', 'network']) {
    let calls = 0;
    const load = createStaticLoader(async () => {
      if (++calls === 1) {
        if (failure === 'network') throw new Error('offline');
        return { ok: failure !== 'http', json: async () => { throw new Error('invalid JSON'); } };
      }
      return { ok: true, json: async () => ['recovered'] };
    });
    await assert.rejects(load('catalog.json'));
    assert.deepEqual(await load('catalog.json'), ['recovered']);
    assert.equal(calls, 2);
  }
});

test('each setup path is complete and navigation stays bounded', () => {
  for (const id of ['render', 'api', 'plugin', 'remote', 'contribute']) {
    assert.ok(paths[id].steps.length >= 4);
    assert.equal(stepAt(id, -1), 0);
    assert.equal(stepAt(id, 999), paths[id].steps.length - 1);
    for (const step of paths[id].steps) assert.ok(step.title && step.body && step.result);
  }
  assert.throws(() => stepAt('unknown', 0));
});
test('endpoint builder rejects credentials, query secrets and insecure remote URLs', () => {
  assert.equal(normalizeEndpoint('https://example.onrender.com/'), 'https://example.onrender.com');
  assert.equal(normalizeEndpoint('http://127.0.0.1:8765'), 'http://127.0.0.1:8765');
  for (const value of ['javascript:alert(1)', 'https://user:key@example.com', 'http://example.com', 'https://example.com?key=secret', 'https://example.com/mcp/', "https://evil'host.com", 'https://evil$host.com']) {
    assert.throws(() => normalizeEndpoint(value));
  }
});
test('platform commands use the correct environment and never embed a real key', () => {
  assert.match(commandFor('plugin', 0, 'windows', ''), /Scripts/);
  assert.match(commandFor('plugin', 0, 'linux', ''), /bin\/activate/);
  assert.match(commandFor('api', 1, 'linux', 'https://example.onrender.com'), /https:\/\/example.onrender.com\/v1\/skills/);
  assert.match(commandFor('render', 1, 'linux', ''), /token_urlsafe/);
});

test('remote setup connects to the supplied host and references a key variable', () => {
  const config = commandFor('remote', 2, 'windows', 'https://my-library.onrender.com/');
  assert.match(config, /url = "https:\/\/my-library\.onrender\.com\/mcp\/"/);
  assert.match(config, /bearer_token_env_var = "SOLKRAFT_API_KEY"/);
  assert.match(commandFor('remote', 3, 'windows', ''), /\$env:SOLKRAFT_API_KEY/);
  assert.match(commandFor('remote', 3, 'linux', ''), /export SOLKRAFT_API_KEY/);
  assert.match(commandFor('contribute', 4, 'linux', ''), /check_contribution.*--full/);
});
