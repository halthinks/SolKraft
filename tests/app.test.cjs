const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

// Exercise the page's actual event handlers without a browser or an API server.
class Element {
  constructor(tag = 'div') {
    this.tagName = tag.toUpperCase(); this.children = []; this.listeners = {};
    this.attributes = {}; this.dataset = {}; this.value = ''; this.disabled = false;
    this._text = ''; this.className = '';
    this.classList = { add() {}, remove() {}, toggle() {} };
  }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(child => typeof child === 'string' ? child : child.textContent).join(''); }
  set innerHTML(value) { this.textContent = value; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this._text = ''; this.children = children; }
  addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
  async dispatch(type) { await Promise.all((this.listeners[type] || []).map(listener => listener({ currentTarget: this }))); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  showModal() { this.open = true; }
  scrollIntoView() {}
}
function descendants(node, predicate) {
  return node.children.flatMap(child => typeof child === 'string' ? [] : [ ...(predicate(child) ? [child] : []), ...descendants(child, predicate) ]);
}
async function harness(compose) {
  const nodes = new Map();
  const get = selector => {
    if (!nodes.has(selector)) nodes.set(selector, new Element());
    return nodes.get(selector);
  };
  const skills = {
    alpha: { id: 'alpha', name: 'Alpha', content: '# Alpha\n\nInspect failure traces and reproduce the crash.\n\n<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->\nShared integration guidance.' },
    beta: { id: 'beta', name: 'Beta', content: '# Beta\n\nCompare market segments and calculate demand.\n\n<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->\nShared integration guidance.' },
  };
  const copies = []; let fetches = 0;
  const context = vm.createContext({
    document: { querySelector: get, querySelectorAll: () => [], createElement: tag => new Element(tag), createTextNode: text => { const node = new Element('#text'); node.textContent = text; return node; } },
    navigator: { clipboard: { writeText: async text => copies.push(text) } },
    URL, AbortController, AbortSignal, console,
    setTimeout: () => 1, clearTimeout() {},
    fetch: async () => { fetches++; throw new Error('Unexpected API request'); },
  });
  context.window = context;
  context.composeSolKraftBrowserRoute = compose;
  context.loadSolKraftStatic = async asset => {
    if (asset === 'assets/catalog.json') return Object.values(skills);
    if (asset === 'assets/skill-structure.json') return {};
    if (asset === 'assets/graph.json') return { nodes: {}, edges: [], semantic_core_count: 0 };
    const id = asset.match(/assets\/skills\/(.+)\.json/)[1];
    return skills[id];
  };
  for (const asset of ['skill-methods.js', 'app.js']) {
    vm.runInContext(fs.readFileSync(path.join(__dirname, '../docs/assets', asset), 'utf8'), context, { filename: asset });
  }
  await new Promise(resolve => setImmediate(resolve));
  return { get, skills, copies, fetches: () => fetches };
}
const route = { stages: [{ stage: 1, selected: ['alpha'], text: 'Diagnose the crash', reason: 'software diagnosis' }], unselected_requested_stages: [] };

test('Build my route calls the browser router with the user request and renders its stages without an API', async () => {
  let finish; const calls = [];
  const page = await harness((objective, maxSkills, progress) => {
    calls.push({ objective, maxSkills }); progress('Loading the production router');
    return new Promise(resolve => { finish = resolve; });
  });
  page.get('#route-input').value = '  Diagnose the crash  '; page.get('#max-skills').value = '7';
  const pending = page.get('#route-btn').dispatch('click');
  assert.equal(page.get('#route-btn').disabled, true);
  assert.equal(page.get('#route-btn').attributes['aria-busy'], 'true');
  assert.match(page.get('#route-results').textContent, /Loading the production router/);
  await page.get('#route-btn').dispatch('click');
  assert.equal(calls.length, 1, 'busy clicks must not create duplicate requests');
  finish(route); await pending;
  assert.deepEqual(calls, [{ objective: 'Diagnose the crash', maxSkills: 7 }]);
  assert.match(page.get('#route-results').textContent, /alpha/);
  assert.match(page.get('#route-results').textContent, /Diagnose the crash/);
  assert.match(page.get('#route-mode').textContent, /bundled production router/);
  assert.equal(page.get('#route-btn').disabled, false);
  assert.equal(page.get('#route-btn').attributes['aria-busy'], undefined);
  assert.equal(page.fetches(), 0);
});

test('router failure is visible and the same button can retry successfully', async () => {
  let attempts = 0;
  const page = await harness(async () => { if (++attempts === 1) throw new Error('Router download failed'); return route; });
  page.get('#route-input').value = 'Diagnose the crash'; page.get('#max-skills').value = '5';
  await page.get('#route-btn').dispatch('click');
  assert.match(page.get('#route-results').textContent, /Router download failed/);
  assert.equal(page.get('#route-btn').disabled, false);
  assert.equal(page.get('#route-btn').attributes['aria-busy'], undefined);
  await page.get('#route-btn').dispatch('click');
  assert.equal(attempts, 2);
  assert.match(page.get('#route-results').textContent, /alpha/);
  assert.doesNotMatch(page.get('#route-results').textContent, /Router download failed/);
});

test('skill inspection shows each original method and preserves the complete copy payload', async () => {
  const page = await harness(async () => route);
  const buttons = descendants(page.get('#results'), node => node.className === 'inspect-btn');
  assert.equal(buttons.length, 2);
  const methods = [];
  for (let index = 0; index < buttons.length; index++) {
    await buttons[index].dispatch('click');
    const detail = page.get('#skill-detail');
    const method = descendants(detail, node => node.className === 'skill-method')[0];
    methods.push(method.textContent);
    assert.doesNotMatch(method.textContent, /Shared integration guidance/);
    assert.match(detail.textContent, /Shared integration guidance/);
    const copy = descendants(detail, node => node.textContent === 'Copy skill instructions')[0];
    await copy.dispatch('click');
  }
  assert.match(methods[0], /failure traces/);
  assert.match(methods[1], /market segments/);
  assert.notEqual(methods[0], methods[1]);
  assert.deepEqual(page.copies, [page.skills.alpha.content, page.skills.beta.content]);
});
