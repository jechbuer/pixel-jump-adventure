# 🎮 Pixel Jump Adventure

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-blue.svg)](https://www.python.org/dev/peps/pep-0008/)

> Ein klassisches 2D-Jump-and-Run-Spiel im Retro-Pixel-Stil, implementiert mit **Python** und **Pygame**.

![Game Preview](https://via.placeholder.com/800x400/0f172a/4ade80?text=Pixel+Jump+Adventure)

## 🎯 Features

### 🕹️ Spiel-Mechanik
- ✅ **Physik-basierte Bewegung** mit Gravitation und Sprungmechanik
- ✅ **Präzise Kollisionserkennung** für Plattformen und Gegner
- ✅ **Patrouillen-KI** für Gegner mit automatischer Richtungsänderung
- ✅ **Schuss-System** mit Projektilen
- ✅ **Partikel-Effekte** (Explosionen, Funkeln, Staub)

### 🗺️ Level-Design
- 🟪 **Großes Level** (3200x600 Pixel)
- 🟪 **Mehrere Plattformen** mit unterschiedlichen Höhen
- 👾 **Gegner** auf Plattformen
- 🪙 **Sammelbare Items** (Münzen, Edelsteine)

### 🎨 Grafik & UI
- 🌄 **Parallax-Hintergrund** mit 3 Ebenen
- 📱 **Responsive UI** mit Gesundheitsanzeige und Score
- 🎮 **Menü-System** (Start, Pause, Game Over, Victory)

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone https://github.com/dein-username/pixel-jump-adventure.git
cd pixel-jump-adventure

# Abhängigkeiten installieren
pip install -r requirements.txt

# Spiel starten
python main.py
```

## 🎮 Steuerung

| Taste | Aktion |
|-------|--------|
| `←` / `→` | Bewegen |
| `A` / `D` | Bewegen (Alternativ) |
| `SPACE` / `W` | Springen |
| `F` | Schießen |
| `ESC` / `P` | Pause |

## 🏆 Punktesystem

| Aktion | Punkte |
|--------|--------|
| 🪙 Münze einsammeln | 10 |
| 💎 Edelstein einsammeln | 50 |
| 👾 Gegner besiegen (Sprung) | 100 |
| 👾 Gegner besiegen (Schuss) | 50 |

## 📁 Projektstruktur

```
pixel_jump_adventure/
├── main.py                 # Einstiegspunkt
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Diese Datei
├── LICENSE                # MIT-Lizenz
├── CONTRIBUTING.md        # Beitragsrichtlinien
├── .gitignore             # Git Ignore-Regeln
├── .github/
│   └── workflows/
│       └── python-app.yml # CI/CD Pipeline
├── assets/                # Spiel-Assets
│   ├── images/
│   └── sounds/
├── docs/                  # Dokumentation
└── src/                   # Quellcode (~2100 Zeilen)
    ├── constants.py       # Spiel-Konstanten & Farben
    ├── game_engine.py     # Haupt-Spielengine
    ├── player.py          # Spieler-Klasse
    ├── enemy.py           # Gegner-Klasse mit KI
    ├── platform.py        # Plattformen
    ├── collectible.py     # Sammelbare Items
    ├── projectile.py      # Projektil-System
    └── utils.py           # Hilfsfunktionen & Kamera
```

## 🛠️ Technische Details

### Physik-Parameter

```python
GRAVITY = 0.6           # Gravitationsstärke
JUMP_FORCE = -14        # Sprungkraft
MOVE_SPEED = 5          # Bewegungsgeschwindigkeit
MAX_FALL_SPEED = 12     # Maximale Fallgeschwindigkeit
FRICTION = 0.85         # Reibung
PROJECTILE_SPEED = 10   # Geschwindigkeit der Schüsse
```

### Farbpalette

| Farbe | Hex | Verwendung |
|-------|-----|------------|
| 🟢 Grün | `#4ade80` | Spieler |
| 🟣 Lila | `#8b5cf6` | Plattformen |
| 🔴 Rot | `#ef4444` | Gegner |
| 🟡 Gold | `#fbbf24` | Münzen |
| 🩷 Pink | `#ec4899` | Edelsteine |

## 🎯 Spielziel

1. **Sammle alle Münzen und Edelsteine** im Level
2. **Besiege Gegner** durch:
   - Springen auf sie von oben (+100 Punkte)
   - Schießen mit `F` (+50 Punkte)
3. **Vermeide Berührungen** mit Gegnern von der Seite
4. **Erreiche das Ende** mit möglichst vielen Punkten!

## 🔧 Entwicklung

### Setup für Entwickler

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate
# Aktivieren (macOS/Linux)
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Spiel starten
python main.py
```

### Build als Executable

```bash
# PyInstaller installieren
pip install pyinstaller

# Executable erstellen
pyinstaller --onefile --name "pixel-jump-adventure" main.py
```

## 🧪 Tests

```bash
# Syntax-Prüfung
python -m py_compile main.py src/*.py

# Import-Test
python -c "import sys; sys.path.insert(0, 'src'); from game_engine import GameEngine"
```

## 🔮 Roadmap

- [ ] Sound-Effekte und Musik
- [ ] Mehrere Level
- [ ] Verschiedene Gegner-Typen
- [ ] Power-Ups
- [ ] Boss-Kämpfe
- [ ] Highscore-Speicherung
- [ ] Level-Editor

## 🤝 Mitwirken

Wir freuen uns über Beiträge! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Credits

- **Engine**: Python 3.x + Pygame
- **Inspiration**: Commander Keen, Super Mario Bros., Celeste

---

<div align="center">

**[⬇️ Download](https://github.com/dein-username/pixel-jump-adventure/releases)** • **[🐛 Issues](https://github.com/dein-username/pixel-jump-adventure/issues)** • **[💡 Discussions](https://github.com/dein-username/pixel-jump-adventure/discussions)**

Made with ❤️ and Python

</div>
