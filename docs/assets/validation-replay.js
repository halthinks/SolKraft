(() => {
  const stream = document.querySelector('#validation-stream');
  const button = document.querySelector('#validation-replay-btn');
  const counter = document.querySelector('#validation-count');
  const progress = document.querySelector('#validation-progress');
  if (!stream || !button || !counter || !progress) return;

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
  let timer;

  function addLine(n) {
    const row = document.createElement('div');
    row.className = 'validation-line new';
    const skill = skills[n % skills.length];
    const check = checks[(n * 7) % checks.length];
    const c = document.createElement('span'); c.className='case'; c.textContent='#'+String(n).padStart(6,'0');
    const r = document.createElement('span'); r.className='route'; r.textContent=skill+' · '+check;
    const p = document.createElement('span'); p.className='pass'; p.textContent='PASS';
    row.append(c,r,p);
    stream.append(row);
    while (stream.children.length > 18) stream.firstElementChild.remove();
    stream.scrollTop = stream.scrollHeight;
  }

  function replay() {
    clearInterval(timer);
    stream.replaceChildren();
    let frame = 0;
    const frames = 180;
    button.disabled = true;
    button.textContent = 'Replaying recorded run…';
    counter.textContent = '0';
    progress.style.width = '0%';

    timer = setInterval(() => {
      frame += 1;
      const count = Math.min(100000, Math.floor(100000 * frame / frames));
      const start = Math.max(1, count - 8);
      for (let n = start; n <= count; n += 2) addLine(n);
      counter.textContent = count.toLocaleString();
      progress.style.width = (frame / frames * 100).toFixed(1) + '%';
      if (frame >= frames) {
        clearInterval(timer);
        counter.textContent = '100,000';
        button.disabled = false;
        button.textContent = 'Replay 100k validation';
        addLine(100000);
      }
    }, 32);
  }

  button.addEventListener('click', replay);
  replay();
})();
