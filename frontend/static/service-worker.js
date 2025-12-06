// Service Worker para modo offline
const CACHE_NAME = 'pampeano-web-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/htmx.min.js',
  '/static/js/alpine.min.js',
  '/static/js/main.js',
  '/static/icons/organizacion.svg',
  '/static/icons/proyecto.svg'
];

// Instalación
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// Activación
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
    .then(() => self.clients.claim())
  );
});

// Fetch con estrategia cache-first
self.addEventListener('fetch', event => {
  // Solo cachear GET requests
  if (event.request.method !== 'GET') return;
  
  // Ignorar APIs y recursos externos
  if (event.request.url.includes('/api/') || 
      event.request.url.includes('/auth/') ||
      !event.request.url.includes(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Cache miss - fetch from network
        return fetch(event.request.clone())
          .then(fetchResponse => {
            // Verificar respuesta válida
            if (!fetchResponse || fetchResponse.status !== 200 || 
                fetchResponse.type !== 'basic') {
              return fetchResponse;
            }
            
            // Clonar respuesta para cachear
            const responseToCache = fetchResponse.clone();
            
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return fetchResponse;
          })
          .catch(() => {
            // Modo offline: devolver página offline
            if (event.request.url.endsWith('.html') || 
                event.request.url === self.location.origin + '/') {
              return caches.match('/static/offline.html');
            }
          });
      })
  );
});

// Sync para datos pendientes (offline)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncPendingData());
  }
});

async function syncPendingData() {
  // Implementar sincronización de datos pendientes cuando haya conexión
  // Esto requeriría almacenar operaciones en IndexedDB
  console.log('Sincronizando datos pendientes...');
}
