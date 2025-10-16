
# Unearthed

Eine kleine Python-Codebasis mit Hilfs-Skripten und Tests.

Dieses Repository enthält mehrere Skripte wie `run.py`, `blocks.py`, `schieben.py` und eine einfache Testdatei `tests.py`.

## Inhalt

- `run.py` – Hauptskript zum Ausführen (siehe Beschreibung im Code).
- `blocks.py` – Hilfsfunktionen / Module für Block-Operationen.
- `schieben.py` – Zusatzskript (bewegt/verschiebt Dinge — siehe Code).
- `tests.py` – Einfache Tests / Test-Sammlung.

> Hinweis: Lies die Kommentare in den einzelnen Dateien für Details zur Benutzung und zu Abhängigkeiten.

## Voraussetzungen

- Python 3.8+ (empfohlen)
- Git (zum Klonen des Repositories)

Optional:
- `pytest` zum Ausführen der Tests (`pip install pytest`).

## Repository klonen

Öffne ein Terminal (z. B. PowerShell) und führe aus:

```powershell
git clone https://github.com/FFLish/Unearthed.git
cd Unearthed
```

Wenn du das Repository in VS Code klonen willst, öffne die Quellverwaltung (Source Control) in VS Code und nutze die Schaltfläche "Repository klonen". Du kannst auch das gleiche `git clone` in der integrierten Konsole ausführen.

Wichtig: Falls das Repository privat ist, stelle sicher, dass du bei GitHub angemeldet bist und ggf. SSH- oder HTTPS-Zugang konfiguriert hast.

## Projekt starten

Die genaue Nutzung hängt vom jeweiligen Skript ab. Ein allgemeiner Startbefehl ist:

```powershell
python run.py
```

Wenn dein System mehrere Python-Versionen hat, benutze ggf. `py -3 run.py` oder `python3 run.py`.

## Tests

Falls `tests.py` eine ausführbare Testdatei ist, kannst du sie direkt starten:

```powershell
python tests.py
```

Alternativ, falls du `pytest` verwendest:

```powershell
pytest -q
```

## Beiträge

Wenn du beitragen möchtest:

1. Forke das Repository.
2. Erstelle einen neuen Branch: `git checkout -b feature/mein-feature`.
3. Committe deine Änderungen und pushe sie: `git push origin feature/mein-feature`.
4. Erstelle einen Pull Request auf GitHub.

## Kontakt

Bei Fragen oder Problemen öffne bitte ein Issue im Repository oder kontaktiere den Maintainer über das GitHub-Profil `FFLish`.

## Lizenz

Standardmäßig keine Lizenz angegeben. Falls du eine Lizenz hinzufügen möchtest, lege eine `LICENSE`-Datei an (z. B. MIT, Apache-2.0).

---

Wenn du möchtest, kann ich die README weiter anpassen (z. B. konkrete Beispiele für `run.py`, Anforderungen in `requirements.txt` erstellen oder Tests mit `pytest` einrichten). Sag mir einfach, welche Details du ergänzt haben willst.
