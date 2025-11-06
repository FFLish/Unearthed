# Unearthed

Dieses Repository enthält das Programm für unseren Roboter in der **Unearthed Season** der *FIRST LEGO League (FLL)*.  
Der Code ist in **Python** mit **PyBricks** programmiert und steuert unseren LEGO Spike/EV3-Roboter während der Missionen auf dem Spielfeld.

---

## Was ist **GitHub**?

**GitHub** ist eine Plattform, auf der man Code speichern, teilen und gemeinsam bearbeiten kann.  
Man kann sich das wie **Google Drive – aber für Programmierer** vorstellen.  

GitHub nutzt das System **Git**, um Versionen von Dateien zu speichern – also wer was geändert hat und wann.

---

## Warum ist das nützlich?

- Wenn man ein Programm schreibt, kann man sehen, welche Änderungen gemacht wurden.  
- Mehrere Personen können gleichzeitig am selben Projekt arbeiten.  
- Man kann ältere Versionen wiederherstellen, falls etwas schiefgeht.  

---

## Was sind **Branches**?

Ein **Branch** (auf Deutsch: *Zweig*) ist wie eine Kopie des Projekts, in der man neue Dinge ausprobieren kann, ohne das Original zu verändern.

Zum Beispiel:  
- Der **main-Branch** ist das Hauptprojekt.  
- Du erstellst einen neuen Branch, z. B. `neue-idee`, und arbeitest dort an etwas Neuem.  
- Wenn alles gut funktioniert, fügst du den Branch wieder mit dem main-Branch zusammen – das nennt man **merge**.  

> So können mehrere Teammitglieder gleichzeitig am Projekt arbeiten, ohne sich gegenseitig in die Quere zu kommen.

---

## Was ist ein **Commit**?

Ein **Commit** ist wie ein Speicherpunkt.  
Wenn du zum Beispiel eine Datei bearbeitest, schreibst du:
> "Ich habe den Fehler im Code behoben."

Dann machst du einen **Commit** – also eine Art „Speichern mit Nachricht“.  
So sieht man später genau:
- Was geändert wurde  
- Wann es geändert wurde  
- Von wem es geändert wurde  

Jeder Commit bekommt eine eindeutige **ID (Hash)** – eine lange Zahlen- und Buchstabenreihe, die ihn identifiziert.

---

## Beispielablauf

1. Du erstellst ein neues Projekt auf GitHub.  
2. Du legst einen Branch mit dem Namen `neues-feature` an.  
3. Du änderst Dateien und machst Commits.  
4. Wenn du fertig bist, erstellst du einen **Pull Request** – also eine Anfrage, deine Änderungen in den main-Branch zu übernehmen.  
5. Jemand überprüft die Änderungen, und dann wird **gemerged** (zusammengeführt).  

---

## Inhalt des Repositories

- `run.py` – Hauptskript zum Ausführen des Programms.  
- `blocks.py` – Modul mit Codeblöcken, die im Hauptprogramm verwendet werden.  
- `schieben.py` – Programm, mit dem man den Roboter über das Spielfeld bewegen kann, um Positionen oder Abläufe zu testen.  
- `tests.py` – Dokument für temporäre Tests (wird nicht dauerhaft im Git-Repository gespeichert).

---

## Repository klonen

### Schritt 1: GitHub-Konto erstellen
Erstelle ein Konto auf [https://github.com](https://github.com).

### Schritt 2: Git installieren
- Lade den Installer von [https://git-scm.com/downloads](https://git-scm.com/downloads) herunter und führe ihn aus.  
- Alternativ kann Git über die Kommandozeile installiert werden.

### Schritt 3: Visual Studio Code installieren
Lade **Visual Studio Code (VS Code)** von der offiziellen Website herunter und installiere es.

### Schritt 4: Repository klonen
1. Öffne VS Code.  
2. Klicke links auf der Taskleiste auf **Source Control**.  
3. Wähle **Clone Git Repository** aus.  
4. Füge den Link zu diesem Repository ein.  
5. Melde dich mit deinem GitHub-Konto an oder gewähre VS Code Zugriff.  
6. Wähle einen Ordner, in dem das Repository lokal gespeichert werden soll.

---

## Projekt starten

Wenn du Änderungen gemacht hast, kannst du das Programm über das Terminal starten.  
Öffne in VS Code oben das Menü **Terminal → New Terminal** und gib folgenden Befehl ein: `py -3 -m pipx run pybricksdev run ble main.py`

Der Roboter muss dafür **Bluetooth aktiviert** haben.

---

## Beiträge

Wenn du zum Projekt beitragen möchtest:

1. Öffne **Source Control**.  
2. Erstelle einen neuen Branch.  
3. Committe deine Änderungen und pushe sie.  
4. Erstelle einen **Pull Request** auf GitHub, um deine Änderungen zur Überprüfung einzureichen.
