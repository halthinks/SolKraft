(() => {
  const section = document.querySelector('#validation-replay');
  const stream = document.querySelector('#validation-stream');
  const counter = document.querySelector('#validation-count');
  const progress = document.querySelector('#validation-progress');
  if (!section || !stream || !counter || !progress) return;

  const skills = [
    'solforge-workflow-codebase','solforge-package-build','solforge-now',
    'solforge-workflow-software-security','solforge-workflow-data-validate',
    'solforge-run-refactor','solforge-plugin-development','deep-research',
    'audit-git-worktrees','solforge-workflow-math-verify',
    'solforge-result-validator','build-selected-hardware-product'
  ];
  const checks = [
    'capability identity → target selected',
    'hardened policy → admissible',
    'contract state → valid',
    'typed dataflow → resolved',
    'execution_authorized → false',
    'near-neighbor rejected',
    'whole-request identity preserved',
    'consequential boundary preserved'
  ];

  const frames = 180;
  const frameMs = 32 * 30; // 30× slower than the original replay.
  let timer = null;
  let started = false;

  function addLine(n) {
    const row = document.createElement('div');
    row.className = 'validation-line new';
    const skill = skills[n % skills.length];
    const check = checks[(n * 7) % checks.length];

    const c = document.createElement('span');
    c.className = 'case';
    c.textContent = '#' + String(n).padStart(6, '0');

    const r = document.createElement('span');
    r.className = 'route';
    r.textContent = skill + ' · ' + check;

    const p = document.createElement('span');
    p.className = 'pass';
    p.textContent = 'PASS';

    row.append(c, r, p);
    stream.append(row);

    while (stream.children.length > 18) stream.firstElementChild.remove();
    stream.scrollTop = stream.scrollHeight;
  }

  function replay() {
    if (started) return;
    started = true;

    stream.replaceChildren();
    counter.textContent = '0';
    progress.style.width = '0%';

    let frame = 0;
    timer = setInterval(() => {
      frame += 1;
      const count = Math.min(100000, Math.floor(100000 * frame / frames));
      const start = Math.max(1, count - 8);

      for (let n = start; n <= count; n += 2) addLine(n);

      counter.textContent = count.toLocaleString();
      progress.style.width = (frame / frames * 100).toFixed(1) + '%';

      if (frame >= frames) {
        clearInterval(timer);
        timer = null;
        counter.textContent = '100,000';
        progress.style.width = '100%';
        addLine(100000);
      }
    }, frameMs);
  }

  counter.textContent = '0';
  progress.style.width = '0%';

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        observer.disconnect();
        replay();
      }
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px -5% 0px'
    });

    observer.observe(section);
  } else {
    replay();
  }
})();
