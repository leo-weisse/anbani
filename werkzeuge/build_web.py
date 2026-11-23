"""Baut aus anbani.html die eigenständige Web-App im Ordner docs/ (für GitHub Pages).

Aufruf:  python werkzeuge/build_web.py
"""
import hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "anbani.html")
OUT = os.path.join(ROOT, "docs")

src = open(SRC, encoding="utf-8").read()
# Artifact-spezifische Zeilen entfernen (Titel kommt in den neuen Kopf, Icon wird durch PNG ersetzt)
src = re.sub(r'<title>.*?</title>\s*', "", src, count=1)
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", src, count=1)
src = re.sub(r'<link rel="icon"[^>]*>\s*', "", src, count=1)
head_part, body_part = src.split("</style>", 1)
head_part += "</style>"

HEAD = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Anbani</title>
<meta name="description" content="Georgisch lernen: das Alphabet und erste Wörter, Schritt für Schritt.">
<meta name="theme-color" content="#8C1D3B">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Anbani">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" href="icons/favicon-64.png">
<style>
/* Grundgerüst, das sonst der Artifact-Rahmen liefert */
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
"""
SW_REG = """
<script>
if ("serviceWorker" in navigator) {
  addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
</script>
</body>
</html>
"""
html = HEAD + head_part + "\n</head>\n<body>\n" + body_part.strip() + "\n" + SW_REG
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)

manifest = {
    "name": "Anbani – Georgisch lernen",
    "short_name": "Anbani",
    "description": "Georgisch lernen: das Alphabet und erste Wörter, Schritt für Schritt.",
    "lang": "de",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#24141A",
    "theme_color": "#8C1D3B",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8", newline="\n").write(json.dumps(manifest, ensure_ascii=False, indent=2))

version = hashlib.sha1(html.encode("utf-8")).hexdigest()[:10]
SW = """// Offline-Modus für Anbani. Die Versionsnummer ändert sich bei jedem Build,
// dadurch holt sich die App beim nächsten Start mit Internet die neue Fassung.
const CACHE = "anbani-%s";
const CORE = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png",
              "icons/apple-touch-icon.png", "icons/favicon-64.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith("anbani-") && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Schriften von Google: einmal laden, danach aus dem Speicher
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
    })));
    return;
  }
  if (url.origin !== location.origin) return;
  // Eigene Dateien: erst Internet (für Updates), sonst gespeicherte Fassung
  e.respondWith(fetch(req).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
    return res;
  }).catch(() => caches.match(req).then(hit => hit || caches.match("index.html"))));
});
""" % version
open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8", newline="\n").write(SW)
print("docs/ gebaut, Version", version)
