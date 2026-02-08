# ⚡ Schnell-Setup

## Installation & Start (30 Sekunden)

```bash
# 1. Repository klonen
git clone https://github.com/dein-username/pixel-jump-adventure.git
cd pixel-jump-adventure

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Spiel starten
python main.py
```

## Für Entwickler

```bash
# Virtuelle Umgebung (empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Development-Dependencies
pip install -r requirements.txt
pip install flake8 pylint pytest

# Tests ausführen
python -m py_compile main.py src/*.py
```

## Als Executable bauen

```bash
pip install pyinstaller
pyinstaller --onefile --name "pixel-jump-adventure" main.py
# Executable finden unter: dist/pixel-jump-adventure
```

---

**🎮 Fertig! Viel Spaß beim Spielen!**
