const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateReceipt } = require('../docs/assets/validation.js');
function receipt() {
  return { summary: { proof_passed: true, gates: { complete_execution_counts: true, complete_shard_slice_topology: true, composition_coverage_rate: true, composition_order_rate: true, every_skill_rate: true, full_corpus_configuration: true, no_metadata_leakage: true, single_global_rate: true, single_holdout_rate: true, single_prompt_uniqueness: true, stability_rate: true }, execution_topology: { received_receipts: 32, expected_receipts: 32 }, catalog: { skill_count: 173 }, source: { inputs_sha256: 'a'.repeat(64) }, single: { cases: 173000 }, composition: { cases: 100000 }, stability: { executions: 100000 }, corpus: { expected_total_executions: 373000 } }, examples: [{ route: { execution_authorized: false } }] };
}
function exactReceipt() {
  const data = receipt();
  Object.assign(data.summary.gates, { composition_exact_rate: true, composition_no_extra_selections: true, composition_no_unresolved: true, original_diagnostic_complete: true });
  data.summary.corpus.expected_total_executions = 473000;
  Object.assign(data.summary.single, { rate: 1, holdout_rate: 1, min_per_skill_rate: 1 });
  Object.assign(data.summary.composition, { coverage_rate: 1, order_rate: 1 });
  data.summary.stability.execution_stability_rate = 1;
  data.summary.original_composition_diagnostic = { cases: 100000 };
  Object.assign(data.summary.composition, { exact_set_rate: 1, extra_selected_total: 0, no_unresolved: 100000 });
  return data;
}
test('only a complete exact-match receipt can be displayed as passed', () => {
  assert.equal(validateReceipt(exactReceipt()).composition.exact_set_rate, 1);
  assert.throws(() => validateReceipt(receipt()));
  for (const mutate of [d => d.summary.composition.exact_set_rate = 0.27697, d => d.summary.composition.extra_selected_total = 1, d => d.summary.composition.no_unresolved = 99999]) {
    const data = exactReceipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});
test('failed and partial receipts cannot be displayed as completed proof', () => {
  for (const mutate of [d => d.summary.proof_passed = false, d => d.summary.gates = {}, d => d.summary.gates.single_global_rate = false, d => d.summary.execution_topology.received_receipts = 31, d => d.summary.single.cases = 173, d => d.summary.stability.executions = 100, d => d.summary.corpus.expected_total_executions = 100000]) {
    const data = exactReceipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});
test('missing source identity or unsafe recorded example fails closed', () => {
  for (const mutate of [d => delete d.summary.source, d => d.examples = [], d => d.examples[0].route.execution_authorized = true]) {
    const data = exactReceipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});

test('claimed passing gates cannot conceal rates below 100%', () => {
  for (const mutate of [d => d.summary.single.rate = .999, d => d.summary.single.holdout_rate = .999, d => d.summary.single.min_per_skill_rate = .999, d => d.summary.composition.coverage_rate = .999, d => d.summary.composition.order_rate = .999, d => d.summary.stability.execution_stability_rate = .999, d => d.summary.original_composition_diagnostic.cases = 99999]) {
    const data = exactReceipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});
