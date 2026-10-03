// Public bundled data only. Authenticated API responses never enter this cache.
((root) => {
  function createStaticLoader(fetchData) {
    const pending = new Map();
    return function load(path) {
      if (!pending.has(path)) {
        const request = Promise.resolve().then(() => fetchData(path, { cache: 'no-cache' }))
          .then(response => {
            if (!response.ok) throw new Error('Could not load the bundled data. Please try again.');
            return response.json();
          }).catch(error => { pending.delete(path); throw error; });
        pending.set(path, request);
      }
      return pending.get(path);
    };
  }
  if (typeof module === 'object' && module.exports) module.exports = { createStaticLoader };
  else root.loadSolKraftStatic = createStaticLoader(root.fetch.bind(root));
})(typeof window === 'object' ? window : globalThis);
