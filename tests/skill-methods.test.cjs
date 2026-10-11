const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { methodSections, renderMethod, sourceLink } = require('../docs/assets/skill-methods.js');

test('actual testing and visualization methods remain distinct without shared integration', () => {
  const read = id => fs.readFileSync(path.join(__dirname, '../solkraft/skillpacks', id, 'SKILL.md'), 'utf8');
  const testing = read('solforge-workflow-software-test');
  const visual = read('solforge-workflow-data-visualize');
  const original = testing;
  const methods = methodSections(testing).join('\n');
  assert.match(methods, /reproduce the original failure/i);
  assert.match(methodSections(visual).join('\n'), /histograms or box plots/);
  assert.doesNotMatch(methods, /SolKraft integration|BEGIN SOLKRAFT|name: solforge|Use the \[native execution contract\]/);
  assert.notEqual(methods, methodSections(visual).join('\n'));
  assert.equal(testing, original);
});

test('source links resolve supporting files and reject executable protocols', () => {
  assert.equal(sourceLink('../solforge-result-validator/SKILL.md', 'solforge-build'), 'https://github.com/halthinks/SolKraft/blob/main/solkraft/skillpacks/solforge-result-validator/SKILL.md');
  assert.equal(sourceLink('javascript:alert(1)', 'solforge-build'), null);
  assert.equal(sourceLink('data:text/html,bad', 'solforge-build'), null);
});

test('empty instructions use supplied description and actual contract deliverables', () => {
  const oldDocument = global.document;
  global.document = { createElement: tag => ({ tag, children: [], append(...nodes) { this.children.push(...nodes); } }), createTextNode: text => ({ textContent: text }) };
  try {
    const section = renderMethod({ id: 'example', description: 'Inspect the supplied dataset.', contract: { inputs: [{ name: 'dataset', required: true }], outputs: [{ description: 'Validated rows and issue report' }] } });
    const text = section.children.flatMap(node => [node.textContent, ...node.children.map(child => child.textContent)]).join(' ');
    assert.match(text, /Inspect the supplied dataset/);
    assert.match(text, /dataset \(required\)/);
    assert.match(text, /Validated rows and issue report/);
    assert.equal(methodSections(undefined).length, 0);
  } finally { global.document = oldDocument; }
});
