// LIFE RPG service worker — makes the app installable and offline-capable.
// Bump CACHE when you change cached assets to force an update.
const CACHE = 'liferpg-v5';
// 계급 일러스트(art/*.webp)는 런타임 fetch 캐싱으로 저장됨 — 파일이 아직 없을 수 있어
// ASSETS(addAll)에는 넣지 않는다 (없는 파일이 있으면 설치가 통째로 실패하므로).
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './vendor/tailwind.js', './vendor/orbitron.woff2',
  './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const { request } = e;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  const isHTML = request.mode === 'navigate' ||
    (url.origin === location.origin && /\.html$/.test(url.pathname));

  // HTML(앱 화면)은 네트워크 우선 — 배포한 새 버전이 항상 바로 뜨도록.
  // (오프라인이면 캐시된 화면으로 폴백)
  if (isHTML) {
    e.respondWith(
      fetch(request).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put('./index.html', copy)); }
        return res;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }

  // 그 외 정적 파일(스크립트·폰트·이미지)은 캐시 우선 — 빠르고 오프라인 가능.
  e.respondWith(
    caches.match(request).then(cached => {
      if (cached) return cached;
      return fetch(request).then(res => {
        const cacheable = res.ok && (
          url.origin === location.origin ||
          /(tailwindcss\.com|googleapis\.com|gstatic\.com)/.test(url.host)
        );
        if (cacheable) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(request, copy)); }
        return res;
      });
    })
  );
});
