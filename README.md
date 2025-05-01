# Monte-Carlo-Simulation einer Fahrradwerkstatt

Dieses Projekt simuliert mithilfe der Monte-Carlo-Methode die saisonale Auslastung und Personalplanung einer Fahrradwerkstatt. Ziel ist es, durch zufallsbasierte Modellierung von Kundennachfrage, Wetterbedingungen und Reparaturzeiten wirtschaftlich optimale Personalentscheidungen abzuleiten.

## 📁 Projektstruktur

```
├── documentation.adoc          # Ausführliche Dokumentation im AsciiDoc-Format
├── documentation.pdf           # Gerenderte PDF-Version der Dokumentation
├── README.md                   # Diese Projektbeschreibung
├── shell.nix                   # Entwicklungsumgebung mit Nix
├── src                         # Quellcode und Simulationsergebnisse
│   ├── main.py                 # Hauptskript zur Durchführung der Simulation
│   ├── poetry.lock             # Abhängigkeiten (Poetry)
│   ├── pyproject.toml          # Projektkonfiguration (Poetry)
│   └── results                 # Output-Dateien der Simulation
│       ├── *.json              # Rohdaten der Simulationsergebnisse
│       └── *.png               # Grafische Auswertung
```

## 🚀 Lokale Ausführung

### Voraussetzungen

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) zum Dependency-Management  
  **oder** alternativ: Standard `pip` + `requirements.txt` (siehe unten)
- Optional: [Nix](https://nixos.org/download.html) für reproduzierbare Umgebung via `shell.nix`

### 1. Projekt klonen

```bash
git clone <REPO-URL>
cd <PROJEKTORDNER>
```

### 2. Umgebung vorbereiten

Mit Poetry:

```bash
cd src
poetry install
poetry shell
```

Oder mit Nix:

```bash
nix-shell
```

### 3. Simulation starten

```bash
python main.py
```

Die Ergebnisse werden im Verzeichnis `src/results/` gespeichert. Dort findest du JSON-Dateien mit Rohdaten und PNG-Grafiken zur Visualisierung.

## 📄 Dokumentation

Die vollständige Beschreibung des Modells, der Fragestellungen und der Ergebnisse befindet sich in:

- `documentation.adoc` (bearbeitbar)
- `documentation.pdf` (druckfertige Version)

## 📬 Kontakt

Erstellt von: **Alexander Schulz**  
Datum: 2025-05-01  
Matrikelnummer: 55297

---

Feel free to open Issues oder Pull Requests für Feedback oder Erweiterungen!
```

Möchtest du außerdem ein Badge für „Made with Python“ oder eine Anleitung zum PDF-Export mit Asciidoctor ergänzen?