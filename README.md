# S&P 500 Analyzer
1. Repo auf GitHub anlegen, alle Dateien hochladen.
2. Settings → Pages → Branch `main`, Ordner `/ (root)`.
3. Actions → "Daten aktualisieren" → Run workflow (einmalig, dauert ca. 10–20 Min.). Danach läuft es werktags automatisch.
4. Lokal testen: `python scripts/fetch_data.py 10` (nur 10 Aktien), dann `python -m http.server`.
Ohne data/ zeigt die Seite Demo-Daten.
Hinweis: Scores sind eigene, vereinfachte Formeln. Keine Anlageberatung.
