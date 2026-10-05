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
  const loopHoldMs = 1800;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  let timer = null;
  let restartTimer = null;
  let activated = false;
  let running = false;

  function clearTimers() {
    if (timer) clearInterval(timer);
    if (restartTimer) clearTimeout(restartTimer);
    timer = null;
    restartTimer = null;
    running = false;
  }

  function addLine(n, animate = true) {
    const row = document.createElement('div');
    row.className = animate ? 'validation-line new' : 'validation-line';

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

  function showReducedMotionState() {
    clearTimers();
    stream.replaceChildren();

    const sampleCases = [
      99988, 99990, 99992, 99994, 99996, 99998, 100000
    ];
    sampleCases.forEach((n) => addLine(n, false));

    counter.textContent = '100,000';
    progress.style.width = '100%';
  }

  function runLoop() {
    if (!activated || reducedMotion.matches || running) return;

    running = true;
    stream.replaceChildren();
    counter.textContent = '0';
    progress.style.width = '0%';

    let frame = 0;

    timer = setInterval(() => {
      frame += 1;

      const count = Math.min(
        100000,
        Math.floor(100000 * frame / frames)
      );
      const start = Math.max(1, count - 8);

      for (let n = start; n <= count; n += 2) addLine(n);

      counter.textContent = count.toLocaleString();
      progress.style.width =
        (frame / frames * 100).toFixed(1) + '%';

      if (frame >= frames) {
        clearInterval(timer);
        timer = null;
        running = false;

        counter.textContent = '100,000';
        progress.style.width = '100%';
        addLine(100000);

        restartTimer = setTimeout(() => {
          restartTimer = null;
          runLoop();
        }, loopHoldMs);
      }
    }, frameMs);
  }

  function activate() {
    if (activated) return;
    activated = true;

    if (reducedMotion.matches) {
      showReducedMotionState();
    } else {
      runLoop();
    }
  }

  function handleMotionPreferenceChange() {
    if (!activated) return;

    if (reducedMotion.matches) {
      showReducedMotionState();
    } else {
      clearTimers();
      runLoop();
    }
  }

  if (typeof reducedMotion.addEventListener === 'function') {
    reducedMotion.addEventListener('change', handleMotionPreferenceChange);
  } else if (typeof reducedMotion.addListener === 'function') {
    reducedMotion.addListener(handleMotionPreferenceChange);
  }

  counter.textContent = '0';
  progress.style.width = '0%';

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        observer.disconnect();
        activate();
      }
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px -5% 0px'
    });

    observer.observe(section);
  } else {
    activate();
  }
})();
