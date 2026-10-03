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
  let skillStructure = {};
  let currentQuery = '';
  let currentPage = 0;
  let pageSize = 12;
  let totalMatches = 0;
  let searchGeneration = 0;

  function updatePagination() {
    const pages = Math.max(1, Math.ceil(totalMatches / pageSize));
    $('#page-status').textContent = totalMatches ? `Page ${currentPage + 1} of ${pages} · ${currentPage * pageSize + 1}–${Math.min((currentPage + 1) * pageSize, totalMatches)} of ${totalMatches} skills` : '0 matching skills';
    $('#page-prev').disabled = currentPage === 0;
    $('#page-next').disabled = (currentPage + 1) * pageSize >= totalMatches;
  }
  async function copyText(value) {
    try { await navigator.clipboard.writeText(value); notify('Copied. Paste into your agent or editor.'); }
    catch { notify('Clipboard unavailable. Select the instructions and copy them manually.'); }
  }
  function activatePanel(id) {
    document.querySelectorAll('.tab').forEach(tab => { const active = tab.dataset.panel === id; tab.classList.toggle('active', active); tab.setAttribute('aria-selected', String(active)); });
    document.querySelectorAll('.panel').forEach(panel => { const active = panel.id === id; panel.hidden = !active; panel.classList.toggle('active', active); });
  }

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
      const skill = apiBase ? await request(`/v1/skills/${encodeURIComponent(id)}`) : await window.loadSolKraftStatic(`assets/skills/${encodeURIComponent(id)}.json`);
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
      const copy = document.createElement('button');
      copy.className = 'button primary'; copy.textContent = 'Copy skill instructions';
      copy.addEventListener('click', () => copyText(skill.content || ''));
      const usage = document.createElement('p'); usage.className = 'muted';
      usage.textContent = 'Give this procedure to your agent with your task. Referenced files remain part of the skill; install the pack or retrieve them through REST/MCP when needed.';
      detail.append(label, title, description, copy, usage);
      const structure = skillStructure[id];
      if (structure) {
        const files = document.createElement('details'); files.className = 'parser-explanation';
        const summary = document.createElement('summary'); summary.textContent = `${structure.python_files.length} Python files · ${structure.references.length} supporting references`;
        const listing = document.createElement('pre'); listing.className = 'skill-content';
        const paths = [...structure.python_files, ...structure.references];
        for (const path of paths) {
          const link = document.createElement('a'); link.textContent = path;
          link.href = `https://github.com/halthinks/SolKraft/blob/main/solkraft/skillpacks/${encodeURIComponent(id)}/${path.split('/').map(encodeURIComponent).join('/')}`;
          link.target = '_blank'; link.rel = 'noreferrer'; listing.append(link, '\n');
        }
        if (!paths.length) listing.textContent = 'This skill is instruction-based; no Python runtime is bundled in its folder.';
        files.append(summary, listing); detail.append(files);
      }
      detail.append(body);
    } catch (error) {
      detail.replaceChildren();
      const message = document.createElement('p');
      message.className = 'error';
      message.textContent = error.message;
      detail.append(message);
    }
  }
  async function searchSkills(query = '', reset = true) {
    if (reset) currentPage = 0;
    currentQuery = query;
    const generation = ++searchGeneration;
    const offset = currentPage * pageSize;
    $('#page-prev').disabled = $('#page-next').disabled = true;
    try {
      let rows;
      if (!apiBase) {
        const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
        const matching = offlineSkills.filter(skill => terms.every(term => `${skill.name} ${skill.description}`.toLowerCase().includes(term)));
        totalMatches = matching.length; rows = matching.slice(offset, offset + pageSize);
        countPill.textContent = `${offlineSkills.length} bundled skills`;
      } else {
        setLoading(results, 'Searching the catalog…');
        const data = await request(`/v1/skills?q=${encodeURIComponent(query)}&limit=${pageSize}&offset=${offset}`);
        if (generation !== searchGeneration) return;
        rows = data.items || []; totalMatches = data.total ?? data.count;
        countPill.textContent = `${totalMatches} ${query ? 'matches' : 'available skills'}`;
      }
      renderSkills(rows); updatePagination();
      $('#result-label').textContent = query ? `${totalMatches} MATCHING SKILLS` : `${totalMatches} AVAILABLE SKILLS`;
    } catch (error) {
      if (generation !== searchGeneration) return;
      setLoading(results, error.message); notify(error.message);
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
    if (!apiBase) return notify('Connect an API for custom routing, or use the worked example above.');
    output.replaceChildren();
    setLoading(output, 'Composing an advisory route…');
    try {
      const data = await request('/v1/route', { method: 'POST', body: JSON.stringify({ objective, max_skills: Number($('#max-skills').value) }) });
      $('#route-mode').textContent = 'Live parser response from your connected API.';
      renderRoute(data);
    } catch (error) {
      output.replaceChildren();
      const p = document.createElement('p');
      p.className = 'error';
      p.textContent = error.message;
      output.append(p);
    }
  }

  function renderRoute(data) {
    const output = $('#route-results');
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
        for (const id of stage.selected || []) {
          const inspect = document.createElement('button'); inspect.className = 'inspect-btn';
          inspect.textContent = `Read ${id} →`; inspect.addEventListener('click', () => inspectSkill(id)); card.append(inspect);
        }
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
    const trace = document.createElement('details'); trace.className = 'parser-explanation';
    const summary = document.createElement('summary'); summary.textContent = 'Inspect the parser output, exclusions, and selection trace';
    const raw = document.createElement('pre'); raw.className = 'skill-content'; raw.textContent = JSON.stringify(data, null, 2);
    trace.append(summary, raw); output.append(trace);
  }
  $('#example-btn').addEventListener('click', async () => {
    try {
      const example = await window.loadSolKraftStatic('assets/example-route.json');
      activatePanel('route-panel'); $('#route-input').value = example.objective;
      $('#route-mode').textContent = 'Worked example · actual bundled parser output generated when this site was built. This is not a live server request.';
      renderRoute(example.route); $('#explore').scrollIntoView({behavior: 'smooth'});
    } catch (error) { notify(error.message); }
  });
  $('#page-prev').addEventListener('click', () => { if (currentPage > 0) { currentPage--; searchSkills(currentQuery, false); } });
  $('#page-next').addEventListener('click', () => { if ((currentPage + 1) * pageSize < totalMatches) { currentPage++; searchSkills(currentQuery, false); } });
  $('#page-size').addEventListener('change', event => { pageSize = Number(event.currentTarget.value); searchSkills(currentQuery); });
  $('#search-input').addEventListener('input', event => searchSkills(event.currentTarget.value.trim()));
  document.querySelectorAll('[data-inspect-skill]').forEach(button => button.addEventListener('click', () => inspectSkill(button.dataset.inspectSkill)));
  $('#copy-task').addEventListener('click', () => copyText($('#route-input').value));

  window.loadSolKraftStatic('assets/skill-structure.json').then(data => { skillStructure = data; }).catch(() => {});
  window.loadSolKraftStatic('assets/catalog.json').then(skills => {
    offlineSkills = skills;
    if (!apiBase) searchSkills('');
  }).catch(() => notify('Catalog unavailable. Connect an API to browse skills.'));

  let discoveryGraph;
  function renderGraph(query = '') {
    if (!discoveryGraph) return;
    const edges = discoveryGraph.edges.filter(edge => JSON.stringify(edge).toLowerCase().includes(query.toLowerCase()));
    $('#graph-summary').textContent = `${Object.keys(discoveryGraph.nodes).length} skills · ${discoveryGraph.edges.length} conditional relationships · ${discoveryGraph.semantic_core_count} semantic workflows · showing ${Math.min(edges.length, 60)} of ${edges.length} ${query ? 'matching' : ''} relationships`;
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
  window.loadSolKraftStatic('assets/graph.json').then(graph => { discoveryGraph = graph; renderGraph(); }).catch(() => { $('#graph-summary').textContent = 'Graph unavailable. Reload to retry.'; });
  $('#graph-search').addEventListener('input', event => renderGraph(event.currentTarget.value));

  $('#connect-btn').addEventListener('click', connect);
  $('#api-key').addEventListener('keydown', (event) => { if (event.key === 'Enter') connect(); });
  $('#search-input').addEventListener('keydown', (event) => { if (event.key === 'Enter') searchSkills(event.currentTarget.value.trim()); });
  $('#route-btn').addEventListener('click', buildRoute);
  document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => activatePanel(tab.dataset.panel)));
})();
