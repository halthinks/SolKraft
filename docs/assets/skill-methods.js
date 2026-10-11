/* Source-derived method presentation. Full instructions remain available to copy. */
(() => {
  function methodSections(content) {
    const body = String(content || '')
      .replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '')
      .split('<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->')[0]
      .replace(/<!--[\s\S]*?-->/g, '');
    return body.split(/\n\s*\n/).map(text => text.trim()).filter(text => text &&
      !/^#\s/.test(text) &&
      !/^Use the \[native execution contract\]/.test(text) &&
      !/^Apply this procedure directly within the current task\./.test(text));
  }
  function sourceLink(path, id) {
    try {
      const url = new URL(path, `https://github.com/halthinks/SolKraft/blob/main/solkraft/skillpacks/${encodeURIComponent(id || '')}/`);
      return ['https:', 'http:'].includes(url.protocol) ? url.href : null;
    } catch { return null; }
  }
  function appendText(node, text, id) {
    // Markdown links stay usable; all source prose is inserted as text, never HTML.
    const pattern = /\[([^\]]+)\]\(([^)]+)\)/g;
    let start = 0, match;
    while ((match = pattern.exec(text))) {
      node.append(document.createTextNode(text.slice(start, match.index)));
      const href = sourceLink(match[2], id);
      const label = document.createElement(href ? 'a' : 'span');
      label.textContent = match[1];
      label.title = match[2];
      if (href) { label.href = href; label.target = '_blank'; label.rel = 'noreferrer'; }
      node.append(label);
      start = pattern.lastIndex;
    }
    node.append(document.createTextNode(text.slice(start)));
  }
  function renderMethod(skill) {
    const section = document.createElement('section');
    section.className = 'skill-method';
    const heading = document.createElement('h3');
    heading.textContent = 'What this skill does';
    section.append(heading);
    const paragraphs = methodSections(skill.content);
    for (const text of paragraphs) {
      const paragraph = document.createElement('p');
      paragraph.className = 'skill-method-paragraph';
      appendText(paragraph, text, skill.id);
      section.append(paragraph);
    }
    if (!paragraphs.length) {
      const paragraph = document.createElement('p');
      paragraph.textContent = skill.description || 'Inspect the full instructions and supporting files below.';
      section.append(paragraph);
    }
    for (const [key, title] of [['inputs', 'Needs'], ['outputs', 'Produces']]) {
      const records = skill.contract?.[key];
      if (!Array.isArray(records) || !records.length) continue;
      const heading = document.createElement('h4'); heading.textContent = title;
      const list = document.createElement('ul');
      for (const record of records) {
        const item = document.createElement('li');
        item.textContent = record.description || record.name || '';
        if (key === 'inputs' && record.required) item.textContent += ' (required)';
        list.append(item);
      }
      section.append(heading, list);
    }
    return section;
  }
  const api = { methodSections, renderMethod, sourceLink };
  if (typeof window !== 'undefined') window.SolKraftSkillMethods = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
