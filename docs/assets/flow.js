(async () => {
const diagram = document.querySelector('#workflow-diagram');
const toggle = document.querySelector('#motion-toggle');
let paused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function setMotion() {
  diagram.classList.toggle('motion-paused', paused);
  toggle.setAttribute('aria-pressed', String(paused));
  toggle.textContent = paused ? 'Play animation' : 'Pause animation';
}
toggle.addEventListener('click', () => { paused = !paused; setMotion(); });
setMotion();
try {
  await new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'assets/vendor/mermaid.min.js';
    script.onload = resolve;
    script.onerror = reject;
    document.head.append(script);
  });
  const mermaid = window.mermaid;
  mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'dark', htmlLabels: false,
    themeVariables: { primaryColor: '#172322', primaryTextColor: '#eef4f6', primaryBorderColor: '#75e3a0', lineColor: '#b3f77c', fontFamily: 'Manrope, sans-serif' },
    flowchart: { htmlLabels: false, curve: 'basis', useMaxWidth: true } });
  const source = `flowchart LR
    A[Your request] e1@--> B[SolForge parser]
    G[Selection graph] e2@--> B
    B e3@--> C[Ordered skills]
    C e4@--> D[Skill instructions]
    D e5@--> E[Your host agent]
    P[Capability-preserving execution] e6@--> E
    E e7@--> F[Verified result]
    F -. failed check .-> E
    e1@{ animation: slow }
    e2@{ animation: slow }
    e3@{ animation: slow }
    e4@{ animation: slow }
    e5@{ animation: slow }
    e6@{ animation: slow }
    e7@{ animation: slow }`;
  const { svg } = await mermaid.render('solkraft-workflow', source);
  diagram.innerHTML = svg;
} catch (error) {
  // The readable HTML flow remains useful if the optional renderer cannot load.
  toggle.hidden = true;
  console.warn('Workflow diagram could not render:', error.message);
}
})();
