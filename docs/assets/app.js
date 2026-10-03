(() => {
  const $ = (selector) => document.querySelector(selector);
  const endpointInput = $('#api-url');
  const keyInput = $('#api-key');
  const connection = $('#connection');
  const results = $('#results');
  const countPill = $('#catalog-count');
  const toast = $('#toast');
  let apiBase = '';
  let apiKey = '';
  let toastTimer;
  let offlineSkills = [];

  function notify(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2600);
  }
  function endpoint(path) { return `${apiBase}${path}`; }
  async function request(path, options = {}) {
    if (!apiBase || !apiKey) throw new Error('Connect to your API first.');
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 90000);
    try {
      const response = await fetch(endpoint(path), {
        ...options,
        signal: controller.signal,
        headers: { Authorization: `Bearer ${apiKey}`, ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(options.headers || {}) }
      });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Server returned ${response.status}. Check the API key and CORS settings.`);
      }
      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('The server took too long to respond. A free server may be waking from sleep; try again in a moment.');
      if (error instanceof TypeError) throw new Error('Could not reach the API. Check the URL, server status, and allowed CORS origin.');
      throw error;
    } finally { clearTimeout(timer); }
  }
  function setConnected(online, message) {
    connection.classList.toggle('online', online);
    connection.innerHTML = `<i></i>${message}`;
    countPill.textContent = online ? 'API connected' : 'Connect to load catalog';
  }
  function setLoading(node, message) {
    node.replaceChildren();
    const p = document.createElement('p');
    p.className = 'muted';
    p.textContent = message;
    node.append(p);
  }
  function renderSkills(rows) {
    results.replaceChildren();
    if (!rows.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      const title = document.createElement('strong');
      title.textContent = 'No matching skills found.';
      const hint = document.createElement('p');
      hint.textContent = 'Try describing the outcome in different words, or broaden your search.';
      empty.append(title, hint);
      results.append(empty);
      return;
    }
    for (const skill of rows) {
      const row = document.createElement('article');
      row.className = 'skill-row';
      const info = document.createElement('div');
      const title = document.createElement('h3');
      title.textContent = skill.name || skill.id;
      const description = document.createElement('p');
      description.textContent = skill.description || '';
      info.append(title, description);
      const meta = document.createElement('div');
      meta.className = 'skill-meta';
      const id = document.createElement('span');
      id.className = 'skill-id';
      id.textContent = skill.id;
      const button = document.createElement('button');
      button.className = 'inspect-btn';
      button.type = 'button';
      button.textContent = 'Inspect →';
      button.addEventListener('click', () => inspectSkill(skill.id));
      meta.append(id, button);
      row.append(info, meta);
      results.append(row);
    }
  }
  async function inspectSkill(id) {
    const dialog = $('#skill-dialog');
    const detail = $('#skill-detail');
    detail.replaceChildren();
    const loading = document.createElement('p');
    loading.className = 'muted';
    loading.textContent = 'Loading skill…';
    detail.append(loading);
    dialog.showModal();
    try {
      const skill = apiBase ? await request(`/v1/skills/${encodeURIComponent(id)}`) : await fetch(`assets/skills/${encodeURIComponent(id)}.json`, { cache: 'no-store' }).then(response => response.json());
      detail.replaceChildren();
      const label = document.createElement('div');
      label.className = 'eyebrow';
      label.textContent = 'SELECTED SKILL';
      const title = document.createElement('h2');
      title.textContent = skill.name || skill.id;
      const description = document.createElement('p');
      description.className = 'skill-description';
      description.textContent = skill.description || '';
      const body = document.createElement('pre');
      body.className = 'skill-content';
      body.textContent = skill.content || '';
      detail.append(label, title, description, body);
    } catch (error) {
      detail.replaceChildren();
      const message = document.createElement('p');
      message.className = 'error';
      message.textContent = error.message;
      detail.append(message);
    }
  }
  async function searchSkills(query = '') {
    if (!apiBase) {
      const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
      const rows = offlineSkills.filter(skill => terms.every(term => `${skill.name} ${skill.description}`.toLowerCase().includes(term)));
      renderSkills(rows.slice(0, query ? 50 : 12));
      countPill.textContent = `${offlineSkills.length} bundled skills`;
      return;
    }
    const label = $('#result-label');
    label.textContent = query ? 'MATCHING SKILLS' : 'AVAILABLE SKILLS';
    setLoading(results, 'Searching the catalog…');
    try {
      const data = await request(`/v1/skills?${query ? `q=${encodeURIComponent(query)}&` : ''}limit=${query ? 30 : 12}`);
      renderSkills(data.items || []);
      countPill.textContent = query ? `${data.count} matches` : 'Catalog live';
    } catch (error) {
      setLoading(results, error.message);
      const p = results.querySelector('p');
      if (p) p.classList.add('error');
      notify(error.message);
    }
  }
  async function connect() {
    const raw = endpointInput.value.trim().replace(/\/+$/, '');
    const key = keyInput.value.trim();
    if (!raw || !key) return notify('Enter both the API URL and your bearer key.');
    try {
      const parsed = new URL(raw);
      if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('Use an HTTP or HTTPS API URL.');
      apiBase = raw;
      apiKey = key;
      setConnected(false, 'Connecting…');
      $('#connect-btn').disabled = true;
      const health = await fetch(endpoint('/healthz'), { signal: AbortSignal.timeout(90000) });
      if (!health.ok) throw new Error(`Health check returned ${health.status}.`);
      await request('/v1/skills?limit=1');
      setConnected(true, 'API online');
      notify('Connected. Your key is held in this tab only.');
      await searchSkills('');
    } catch (error) {
      apiBase = '';
      apiKey = '';
      setConnected(false, 'Not connected');
      notify(error.message || 'Could not connect. Check the URL, key, and CORS configuration.');
    } finally { $('#connect-btn').disabled = false; }
  }
  async function buildRoute() {
    const objective = $('#route-input').value.trim();
    const output = $('#route-results');
    if (!objective) return notify('Describe the work you want to complete.');
    output.replaceChildren();
    setLoading(output, 'Composing an advisory route…');
    try {
      const data = await request('/v1/route', { method: 'POST', body: JSON.stringify({ objective, max_skills: Number($('#max-skills').value) }) });
      output.replaceChildren();
      const notice = document.createElement('div');
      notice.className = 'route-warning';
      notice.textContent = 'Suggested workflow only · SolKraft does not execute skills or authorize actions.';
      output.append(notice);
      for (const stage of data.stages || []) {
        const card = document.createElement('article');
        card.className = 'route-card';
        const head = document.createElement('div');
        head.className = 'route-card-head';
        const number = document.createElement('span');
        number.className = 'stage-number';
        number.textContent = String(stage.stage);
        const title = document.createElement('h4');
        title.textContent = (stage.selected || []).join(' · ') || 'No confident skill match';
        head.append(number, title);
        const description = document.createElement('p');
        description.textContent = `${stage.text || ''} — ${stage.reason || ''}`;
        card.append(head, description);
        output.append(card);
      }
      for (const stage of data.unselected_requested_stages || []) {
        const p = document.createElement('p');
        p.className = 'muted';
        p.textContent = `Unresolved: ${stage.text} — ${stage.reason}`;
        output.append(p);
      }
      if (!data.stages || !data.stages.length) {
        const p = document.createElement('p');
        p.className = 'muted';
        p.textContent = 'No confident skill match. Try a more specific outcome.';
        output.append(p);
      }
    } catch (error) {
      output.replaceChildren();
      const p = document.createElement('p');
      p.className = 'error';
      p.textContent = error.message;
      output.append(p);
    }
  }

  fetch('assets/catalog.json', { cache: 'no-store' }).then(response => response.json()).then(skills => {
    offlineSkills = skills;
    if (!apiBase) searchSkills('');
  }).catch(() => notify('Catalog unavailable. Connect an API to browse skills.'));

  let discoveryGraph;
  function renderGraph(query = '') {
    if (!discoveryGraph) return;
    const edges = discoveryGraph.edges.filter(edge => JSON.stringify(edge).toLowerCase().includes(query.toLowerCase()));
    $('#graph-summary').textContent = `${Object.keys(discoveryGraph.nodes).length} skills · ${discoveryGraph.edges.length} conditional relationships · ${discoveryGraph.semantic_core_count} semantic workflows`;
    const container = $('#graph-results');
    container.replaceChildren();
    for (const edge of edges.slice(0, 60)) {
      const row = document.createElement('article'); row.className = 'skill-row';
      const info = document.createElement('div');
      const title = document.createElement('h3'); title.textContent = `${edge.from} → ${edge.to}`;
      const condition = document.createElement('p'); condition.textContent = `${edge.type}: ${edge.condition}`;
      info.append(title, condition); row.append(info); container.append(row);
    }
    if (!edges.length) container.textContent = 'No matching relationships. Catalog-only skills remain available through discovery and explicit selection.';
  }
  fetch('assets/graph.json', { cache: 'no-store' }).then(r => r.json()).then(graph => { discoveryGraph = graph; renderGraph(); }).catch(() => { $('#graph-summary').textContent = 'Graph unavailable. Reload to retry.'; });
  $('#graph-search').addEventListener('input', event => renderGraph(event.currentTarget.value));

  $('#connect-btn').addEventListener('click', connect);
  $('#api-key').addEventListener('keydown', (event) => { if (event.key === 'Enter') connect(); });
  $('#search-input').addEventListener('keydown', (event) => { if (event.key === 'Enter') searchSkills(event.currentTarget.value.trim()); });
  $('#route-btn').addEventListener('click', buildRoute);
  document.querySelectorAll('.tab').forEach((tab) => tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach((item) => { item.classList.toggle('active', item === tab); item.setAttribute('aria-selected', String(item === tab)); });
    document.querySelectorAll('.panel').forEach((panel) => { const active = panel.id === tab.dataset.panel; panel.hidden = !active; panel.classList.toggle('active', active); });
  }));
})();
