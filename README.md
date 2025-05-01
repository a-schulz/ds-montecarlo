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

---

### Variante A: Mit Poetry

```bash
cd src
poetry install
poetry shell
python main.py
```

---

### Variante B: Mit pip (ohne Poetry)

#### 1. Virtuelle Umgebung erstellen (optional, empfohlen)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

#### 2. Installation via pip

```bash
pip install -r requirements.txt
```

#### 3. Simulation starten

```bash
python main.py
```

---

### Variante C: Mit Nix

Falls du `nix-shell` verwendest:

```bash
nix-shell
cd src
python main.py
```

---

## 📄 Dokumentation

Die vollständige Beschreibung des Modells, der Fragestellungen und der Ergebnisse befindet sich in:

- `documentation.adoc` (bearbeitbar)
- `documentation.pdf` (druckfertige Version)

## 📬 Kontakt

**Ersteller:** Alexander Schulz  
**Datum:** 2025-05-01  
**Matrikelnummer:** 55297
