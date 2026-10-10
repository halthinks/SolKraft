/* Completed evidence and recorded production routes; no simulated CI. */
(() => {
  function validateReceipt(data) {
    const s = data?.summary;
    const required = ['complete_execution_counts', 'complete_shard_slice_topology', 'composition_coverage_rate', 'composition_order_rate', 'every_skill_rate', 'full_corpus_configuration', 'no_metadata_leakage', 'single_global_rate', 'single_holdout_rate', 'single_prompt_uniqueness', 'stability_rate'];
    if (!s?.proof_passed || !s.gates || !required.every(k => s.gates[k] === true)) throw new Error('The full proof has not passed.');
    if (s.execution_topology?.received_receipts !== s.execution_topology?.expected_receipts || !s.execution_topology?.expected_receipts) throw new Error('The receipt set is incomplete.');
    const expected = s.catalog?.skill_count * 1000 + 200000;
    if (s.single?.cases !== s.catalog?.skill_count * 1000 || s.composition?.cases !== 100000 || s.stability?.executions !== 100000 || s.corpus?.expected_total_executions !== expected) throw new Error('The full execution counts do not match.');
    if (!/^[a-f0-9]{64}$/.test(s.source?.inputs_sha256 || '')) throw new Error('Source identity is missing.');
    if (!Array.isArray(data.examples) || !data.examples.length || data.examples.some(x => x.route?.execution_authorized !== false)) throw new Error('Recorded examples are unavailable or invalid.');
    return s;
  }
  if (typeof module !== 'undefined') module.exports = { validateReceipt };
  if (typeof document === 'undefined') return;
  if (!document.querySelector('#validation-replay')) return;
  const $ = id => document.getElementById(id);
  const number = n => n.toLocaleString('en-US');
  const percent = n => (n * 100).toFixed(3) + '%';
  let recorded = null;
  function showExample(index) {
    const example = recorded.examples[index];
    $('proof-request').textContent = example.objective;
    $('proof-route').replaceChildren();
    example.route.selected.forEach((id, i) => {
      const row = document.createElement('li');
      const step = document.createElement('span'); step.className = 'proof-step'; step.textContent = String(i + 1).padStart(2, '0');
      const text = document.createElement('div');
      const name = document.createElement('strong'); name.textContent = example.names[id] || id;
      const code = document.createElement('small'); code.textContent = id;
      text.append(name, code); row.append(step, text); $('proof-route').append(row);
    });
    if (!example.route.selected.length) {
      const row = document.createElement('li'); row.textContent = 'No procedure selected: this work was explicitly excluded.'; $('proof-route').append(row);
    }
    $('proof-example-status').textContent = `${example.route.selected.length} selected · ${example.route.unselected_requested_stages?.length || 0} unresolved · execution_authorized: false`;
  }
  async function load() {
    $('proof-status').textContent = 'Loading completed receipt…'; $('proof-retry').hidden = true;
    try {
      const response = await fetch('assets/semantic-proof.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error('Receipt could not be loaded.');
      recorded = await response.json(); const s = validateReceipt(recorded);
      $('validation-count').textContent = number(s.corpus.expected_total_executions);
      $('proof-single').textContent = percent(s.single.rate);
      $('proof-coverage').textContent = percent(s.composition.coverage_rate);
      $('proof-order').textContent = percent(s.composition.order_rate);
      $('proof-stability').textContent = percent(s.stability.execution_stability_rate);
      $('proof-exact').textContent = percent(s.composition.exact_set_rate);
      $('proof-precision-note').textContent = `${number(s.composition.exact_target_set)} / ${number(s.composition.cases)} exact sets · ${number(s.composition.extra_selected_total)} extra selections · ${number(s.composition.no_unresolved)} requests with no unresolved stages.`;
      $('proof-status').textContent = `${s.execution_topology.received_receipts}/${s.execution_topology.expected_receipts} receipts · all gates passed · recorded local run`;
      $('proof-source').textContent = `Tested inputs SHA-256 ${s.source.inputs_sha256}`;
      $('proof-examples').replaceChildren();
      recorded.examples.forEach((example, index) => {
        const option = document.createElement('option'); option.value = index; option.textContent = example.label; $('proof-examples').append(option);
      });
      $('proof-examples').disabled = false; $('proof-open-route').disabled = false; showExample(0);
    } catch (error) {
      recorded = null;
      ['validation-count', 'proof-single', 'proof-coverage', 'proof-order', 'proof-stability', 'proof-exact'].forEach(id => $(id).textContent = '—');
      $('proof-status').textContent = `Evidence unavailable: ${error.message}`;
      $('proof-retry').hidden = false; $('proof-examples').disabled = true; $('proof-open-route').disabled = true;
      $('proof-route').replaceChildren(); $('proof-example-status').textContent = 'No routing example loaded.';
      $('proof-request').textContent = 'No recorded request available.';
      $('proof-precision-note').textContent = 'Exact sets, extra selections, and unresolved work require a completed receipt.';
      $('proof-source').textContent = 'No verified source identity loaded.';
    }
  }
  $('proof-examples').addEventListener('change', event => { if (recorded) showExample(Number(event.target.value)); });
  $('proof-retry').addEventListener('click', load);
  $('proof-open-route').addEventListener('click', () => {
    if (!recorded) return;
    document.querySelector('.tab[data-panel="route-panel"]').click();
    $('route-input').value = recorded.examples[Number($('proof-examples').value)].objective;
    document.querySelector('#explore').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    $('route-input').focus({ preventScroll: true });
  });
  load();
})();
