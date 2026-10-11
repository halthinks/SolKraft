/* Lazy browser adapter for the public production router. */
(() => {
  const assetURL = new URL('.', document.currentScript.src);
  let worker;
  let sequence = 0;
  const pending = new Map();
  function reset(error) {
    if (worker) worker.terminate();
    worker = undefined;
    for (const request of pending.values()) {
      clearTimeout(request.timer);
      request.reject(error);
    }
    pending.clear();
  }
  window.composeSolKraftBrowserRoute = (objective, maxSkills = 10, onProgress) => {
    if (typeof objective !== 'string' || !objective.trim()) return Promise.reject(new Error('Enter a request to compose a route.'));
    if (!Number.isInteger(maxSkills) || maxSkills < 1 || maxSkills > 50) return Promise.reject(new Error('Choose between 1 and 50 skills.'));
    if (!worker) {
      worker = new Worker(new URL('router-worker.js', assetURL));
      worker.onmessage = ({ data }) => {
        if (data.type === 'progress') {
          window.dispatchEvent(new CustomEvent('solkraft-router-progress', { detail: data.message }));
          for (const request of pending.values()) {
            if (typeof request.onProgress === 'function') request.onProgress(data.message);
          }
          return;
        }
        const request = pending.get(data.id);
        if (!request) return;
        clearTimeout(request.timer);
        pending.delete(data.id);
        if (data.error) request.reject(new Error(data.error)); else request.resolve(data.route);
      };
      worker.onerror = () => reset(new Error('The browser routing engine could not load. Check your internet connection and retry.'));
    }
    return new Promise((resolve, reject) => {
      const id = ++sequence;
      const timer = setTimeout(() => reset(new Error('The browser routing engine timed out. Check your connection and retry.')), 120000);
      pending.set(id, { resolve, reject, timer, onProgress });
      worker.postMessage({ id, objective, max_skills: maxSkills });
    });
  };
})();
