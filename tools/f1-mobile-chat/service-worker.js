/**
 * F1 Designer Mobile Chat - Service Worker
 * Enables offline caching and PWA installation
 */

const CACHE_NAME = 'f1-designer-chat-v1';
const ASSETS = [
    './',
    './index.html',
    './app.js',
    './styles.css',
    './manifest.json'
];

// Install - cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS))
            .then(() => self.skipWaiting())
    );
});

// Activate - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(
                keys.filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            ))
            .then(() => self.clients.claim())
    );
});

// Fetch - serve from cache, fall back to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Only cache same-origin requests (not API calls)
    if (url.origin !== location.origin) {
        return;
    }
    
    // Don't cache API requests
    if (url.pathname.includes('/session') || 
        url.pathname.includes('/event') ||
        url.pathname.includes('/global')) {
        return;
    }
    
    event.respondWith(
        caches.match(request)
            .then((cached) => {
                if (cached) {
                    // Return cached version, but update cache in background
                    event.waitUntil(
                        fetch(request)
                            .then((response) => {
                                if (response.ok) {
                                    caches.open(CACHE_NAME)
                                        .then((cache) => cache.put(request, response));
                                }
                            })
                            .catch(() => {})
                    );
                    return cached;
                }
                
                return fetch(request)
                    .then((response) => {
                        if (response.ok) {
                            const clone = response.clone();
                            caches.open(CACHE_NAME)
                                .then((cache) => cache.put(request, clone));
                        }
                        return response;
                    });
            })
    );
});
