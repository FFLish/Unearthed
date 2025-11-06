
# Unearthed

Das Proramm für unser Roboter für die Unearthed season. Programiert in Python mit PyBricks.

## Inhalt

- `run.py` – Hauptskript zum Ausführen.
- `blocks.py` – Blöcke für main.
- `schieben.py` – Programm womit man den Roboter auf den Spielfeld schieben kann um den Code zu bekommen.
- `tests.py` – Dokument für temporäre tests. (Wird in der Git repository nicht gespeichert)

## Repository klonen

### Schritt 1: Erstelle dir einen GitHub Konto

### Schritt 2: Git installieren
- Lade dir hier den Installer herunter und führe ihn aus: https://git-scm.com/downloads
- Alternativ Installation über die Kommandozeile

### Schritt 3: VSCode installieren
- Googlen hilft :-)

### Schritt 4: Einrichten von VSCode
- Öffne VSCode
- Links auf der Taskleiste findest `Source Control` drücke drauf
- Wähle `Clone Git Repository` aus
- Füge den Link aus diesem Browserfenster ein
- Gib ggf. deine Anmeldedaten für Git ein bzw. gewähre VSCode Zugriff auf dein Konto
- Wähle einen Ordner aus, in dem das Repository lokal gespeichert werden soll

## Branches
Zu viele Köche verderben den Brei ;-) Zumindest, wenn alle gleichzeitig an unterschiedlichen Dingen arbeiten. Dafür gibt es in Git das Konzept der "Branches". Ein Branch geht immer vom "Stamm", dem main-Branch, aus. Auf dem Branch kann ein Entwickler Änderungen vornehmen, Features ergänzen etc. Sobald der Branch fertig ist, wird ein "Pull Request" erstellt, eine Anfrage an den Administrator, die Änderungen in den main-Branch zu übernehmen. Dazu, wie Branches und Pull Requests funktionieren, gibt es ganz viel Material im Internet, daher gehen wir hier nicht näher darauf ein.

In unserem Repository gibt es insbesondere 3 wichtige Branches: "main" ist der hauptprogramm den fertigen Programm deployed. In "optimize" werden die runs verbessert erstellt. "develop" dient der Weiterentwicklung 

## Projekt starten
Wenn du Änderungen gemacht hast kannst du in Terminal oben mit "New Terminal" dieses Comand eingeben: `py -3 -m pipx run pybricksdev run ble test.py` und auf den Roboter starten (Roboter muss Bluethout anhaben)


## Beiträge

Wenn du beitragen möchtest:
1. Gehe wieder auf Source control
2. Erstelle einen neuen Branch.
2. Committe deine Änderungen und pushe sie.
4. Erstelle einen Pull Request auf GitHub.
