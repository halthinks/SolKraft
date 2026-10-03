const { test } = require('node:test');
const assert = require('node:assert/strict');
const { paths, normalizeEndpoint, stepAt, commandFor } = require('../docs/assets/setup.js');

test('each setup path is complete and navigation stays bounded', () => {
  for (const id of ['render', 'api', 'plugin']) {
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
