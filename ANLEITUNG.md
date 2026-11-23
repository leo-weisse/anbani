# Anbani – Georgisch lernen

## Was liegt wo?

| Datei / Ordner | Wofür |
|---|---|
| `anbani.html` | Die App selbst. Hier werden Lektionen, Design und Logik geändert. |
| `docs/` | Die fertige Web-App fürs Handy. Wird aus `anbani.html` erzeugt, nicht von Hand ändern. |
| `logo/` | Das Logo als App-Icon und als Schriftzug (hell und dunkel). |
| `werkzeuge/build_web.py` | Erzeugt `docs/` neu. |

## Nach einer Änderung an der App

1. In diesem Ordner ausführen:

   ```powershell
   python werkzeuge/build_web.py
   ```

2. Den Ordner `docs/` wieder zu GitHub hochladen.

Beim nächsten Öffnen mit Internet holt sich die App auf dem Handy die neue Version von selbst.

## App auf den Home-Bildschirm legen

**iPhone:** Die Adresse der App in **Safari** öffnen → Teilen-Symbol (Quadrat mit Pfeil) → **„Zum Home-Bildschirm“** → „Hinzufügen“.

**Android:** Die Adresse in **Chrome** öffnen → Menü **⋮** → **„App installieren“** oder **„Zum Startbildschirm hinzufügen“**.

Danach startet Anbani im Vollbild mit eigenem Symbol. Nach dem ersten Öffnen funktioniert die App auch ohne Internet.

## Gut zu wissen

- Der Lernfortschritt wird auf dem jeweiligen Gerät gespeichert. Handy und PC haben also einen eigenen Stand.
- Beim allerersten Start braucht die App Internet, um Dateien und Schriften zu laden. Danach ist alles auf dem Gerät gespeichert.
