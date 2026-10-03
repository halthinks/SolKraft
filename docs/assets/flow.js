// Reveal once when visible; this illustrates information flow, not a live job.
(() => {
  const tracks = document.querySelectorAll('.flow-track');
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    tracks.forEach(track => track.classList.add('is-visible'));
    return;
  }
  tracks.forEach(track => track.classList.add('motion-ready'));
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }
  }, { threshold: 0.08 });
  tracks.forEach(track => observer.observe(track));
})();
