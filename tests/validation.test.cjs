const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateReceipt } = require('../docs/assets/validation.js');
function receipt() {
  return { summary: { proof_passed: true, gates: { complete_execution_counts: true, complete_shard_slice_topology: true, composition_coverage_rate: true, composition_order_rate: true, every_skill_rate: true, full_corpus_configuration: true, no_metadata_leakage: true, single_global_rate: true, single_holdout_rate: true, single_prompt_uniqueness: true, stability_rate: true }, execution_topology: { received_receipts: 32, expected_receipts: 32 }, catalog: { skill_count: 173 }, source: { inputs_sha256: 'a'.repeat(64) }, single: { cases: 173000 }, composition: { cases: 100000 }, stability: { executions: 100000 }, corpus: { expected_total_executions: 373000 } }, examples: [{ route: { execution_authorized: false } }] };
}
test('a complete receipt can be displayed without conflating gate acceptance with precision', () => {
  const data = receipt(); data.summary.composition.exact_set_rate = 0.27697;
  assert.equal(validateReceipt(data).composition.exact_set_rate, 0.27697);
});
test('failed and partial receipts cannot be displayed as completed proof', () => {
  for (const mutate of [d => d.summary.proof_passed = false, d => d.summary.gates = {}, d => d.summary.gates.single_global_rate = false, d => d.summary.execution_topology.received_receipts = 31, d => d.summary.single.cases = 173, d => d.summary.stability.executions = 100, d => d.summary.corpus.expected_total_executions = 100000]) {
    const data = receipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});
test('missing source identity or unsafe recorded example fails closed', () => {
  for (const mutate of [d => delete d.summary.source, d => d.examples = [], d => d.examples[0].route.execution_authorized = true]) {
    const data = receipt(); mutate(data); assert.throws(() => validateReceipt(data));
  }
});
