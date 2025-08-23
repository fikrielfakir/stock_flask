// StockCéramique Service Worker
// Advanced PWA functionality with offline support and smart caching

const CACHE_NAME = 'stockceramique-v2.0.0';
const STATIC_CACHE = 'stockceramique-static-v2.0.0';
const DATA_CACHE = 'stockceramique-data-v2.0.0';

// Resources to cache on install
const STATIC_RESOURCES = [
  '/',
  '/enhanced-dashboard',
  '/dashboard',
  '/articles',
  '/suppliers',
  '/requestors',
  '/purchase-requests',
  '/reception',
  '/outbound',
  '/reports',
  '/analytics',
  '/settings',
  '/src/index.css',
  '/src/main.tsx',
];

// API endpoints to cache
const API_ENDPOINTS = [
  '/api/articles',
  '/api/suppliers',
  '/api/requestors',
  '/api/purchase-requests',
  '/api/dashboard/stats',
  '/api/dashboard/stock-evolution',
  '/api/dashboard/category-distribution',
  '/api/dashboard/recent-movements',
];

// Install Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static resources
      caches.open(STATIC_CACHE).then((cache) => {
        console.log('Service Worker: Caching static resources');
        return cache.addAll(STATIC_RESOURCES);
      }),
      
      // Skip waiting to activate immediately
      self.skipWaiting()
    ])
  );
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    Promise.all([
      // Clear old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && 
                cacheName !== STATIC_CACHE && 
                cacheName !== DATA_CACHE) {
              console.log('Service Worker: Deleting old cache', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      
      // Take control of all clients
      self.clients.claim()
    ])
  );
});

// Fetch event - Smart caching strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static resources
  if (request.destination === 'document' || 
      request.destination === 'script' || 
      request.destination === 'style') {
    event.respondWith(handleStaticRequest(request));
    return;
  }

  // Default: try network first, fallback to cache
  event.respondWith(
    fetch(request)
      .then((response) => {
        // Cache successful responses
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(request);
      })
  );
});

// API Request Handler - Network first with fallback
async function handleApiRequest(request) {
  try {
    // Try network first
    const response = await fetch(request);
    
    if (response.status === 200) {
      // Cache successful API responses
      const cache = await caches.open(DATA_CACHE);
      const responseClone = response.clone();
      
      // Don't cache POST/PUT/DELETE requests
      if (request.method === 'GET') {
        cache.put(request, responseClone);
      }
    }
    
    return response;
  } catch (error) {
    // Network failed, try cache
    console.log('Service Worker: Network failed, trying cache for', request.url);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      // Add offline indicator header
      const response = cachedResponse.clone();
      response.headers.set('X-Served-By', 'ServiceWorker');
      response.headers.set('X-Cache-Status', 'offline');
      return response;
    }
    
    // Return offline fallback for API requests
    return new Response(
      JSON.stringify({
        error: 'Offline - Service temporairement indisponible',
        offline: true,
        timestamp: new Date().toISOString()
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'application/json',
          'X-Cache-Status': 'offline-fallback'
        }
      }
    );
  }
}

// Static Request Handler - Cache first
async function handleStaticRequest(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Return cached version and update in background
    updateCacheInBackground(request);
    return cachedResponse;
  }
  
  // Not in cache, fetch from network
  try {
    const response = await fetch(request);
    
    if (response.status === 200) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('Service Worker: Failed to fetch static resource', request.url);
    
    // Return offline page for documents
    if (request.destination === 'document') {
      return new Response(
        `<!DOCTYPE html>
        <html>
        <head>
          <title>StockCéramique - Hors ligne</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 50px; }
            .offline { color: #666; }
            .retry { margin-top: 20px; }
            button { padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; }
          </style>
        </head>
        <body>
          <h1>🔌 Mode hors ligne</h1>
          <p class="offline">StockCéramique fonctionne en mode hors ligne. Certaines fonctionnalités peuvent être limitées.</p>
          <div class="retry">
            <button onclick="window.location.reload()">Réessayer</button>
            <button onclick="window.location.href='/'">Accueil</button>
          </div>
          <script>
            // Check connection status
            window.addEventListener('online', () => {
              window.location.reload();
            });
          </script>
        </body>
        </html>`,
        {
          status: 200,
          headers: {
            'Content-Type': 'text/html',
            'X-Cache-Status': 'offline-fallback'
          }
        }
      );
    }
    
    throw error;
  }
}

// Background cache update
async function updateCacheInBackground(request) {
  try {
    const response = await fetch(request);
    
    if (response.status === 200) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response);
    }
  } catch (error) {
    // Silently fail background updates
    console.log('Service Worker: Background update failed for', request.url);
  }
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('Service Worker: Background sync triggered', event.tag);
  
  if (event.tag === 'stockceramique-sync') {
    event.waitUntil(syncOfflineActions());
  }
});

// Sync offline actions when back online
async function syncOfflineActions() {
  try {
    // Get offline actions from IndexedDB or cache
    const offlineActions = await getOfflineActions();
    
    for (const action of offlineActions) {
      try {
        await fetch(action.url, {
          method: action.method,
          headers: action.headers,
          body: action.body
        });
        
        // Remove successful action
        await removeOfflineAction(action.id);
        
        // Notify client of success
        await notifyClients({
          type: 'SYNC_SUCCESS',
          action: action.type,
          message: `${action.type} synchronisée avec succès`
        });
        
      } catch (error) {
        console.log('Service Worker: Failed to sync action', action, error);
      }
    }
  } catch (error) {
    console.log('Service Worker: Sync process failed', error);
  }
}

// Push notifications
self.addEventListener('push', (event) => {
  console.log('Service Worker: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification StockCéramique',
    icon: '/icon-192x192.png',
    badge: '/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      url: '/'
    },
    actions: [
      {
        action: 'open',
        title: 'Ouvrir',
        icon: '/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'Fermer'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('StockCéramique', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then((clientList) => {
        // Focus existing window if available
        for (const client of clientList) {
          if (client.url === event.notification.data.url && 'focus' in client) {
            return client.focus();
          }
        }
        
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow(event.notification.data.url);
        }
      })
    );
  }
});

// Utility functions
async function getOfflineActions() {
  // In a real implementation, this would read from IndexedDB
  return [];
}

async function removeOfflineAction(id) {
  // In a real implementation, this would remove from IndexedDB
  console.log('Service Worker: Removing offline action', id);
}

async function notifyClients(message) {
  const clients = await self.clients.matchAll();
  
  clients.forEach((client) => {
    client.postMessage(message);
  });
}

// Performance monitoring
self.addEventListener('message', (event) => {
  if (event.data.type === 'PERFORMANCE_MARK') {
    console.log('Service Worker: Performance mark', event.data);
  }
});

console.log('Service Worker: StockCéramique SW loaded successfully');