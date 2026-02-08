# Contributing to Pixel Jump Adventure

Vielen Dank für dein Interesse an diesem Projekt! Wir freuen uns über jede Form von Beitrag.

## 🚀 Wie du beitragen kannst

### 🐛 Bugs melden

Wenn du einen Bug findest:

1. Überprüfe zuerst, ob der Bug bereits gemeldet wurde
2. Erstelle ein neues Issue mit folgenden Informationen:
   - Beschreibung des Bugs
   - Schritte zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - Python-Version und Betriebssystem
   - Screenshots (falls relevant)

### 💡 Feature-Vorschläge

Hast du eine Idee für ein neues Feature?

1. Erstelle ein Issue mit dem Label "enhancement"
2. Beschreibe das Feature detailliert
3. Erkläre, warum es nützlich wäre

### 🔧 Code beitragen

#### Voraussetzungen

- Python 3.8+
- pygame 2.5+
- Git

#### Setup

```bash
# Repository forken und klonen
git clone https://github.com/dein-username/pixel-jump-adventure.git
cd pixel-jump-adventure

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv

# Virtuelle Umgebung aktivieren
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

#### Entwicklungsworkflow

1. **Branch erstellen**
   ```bash
   git checkout -b feature/dein-feature-name
   ```

2. **Änderungen vornehmen**
   - Folge dem bestehenden Code-Stil
   - Schreibe klare, beschreibende Commit-Nachrichten
   - Füge Docstrings zu neuen Funktionen hinzu

3. **Testen**
   ```bash
   python main.py
   ```

4. **Commit und Push**
   ```bash
   git add .
   git commit -m "feat: Beschreibung der Änderung"
   git push origin feature/dein-feature-name
   ```

5. **Pull Request erstellen**
   - Beschreibe deine Änderungen
   - Verlinke relevante Issues
   - Warte auf Review

## 📝 Code-Stil

### Python

- Folge [PEP 8](https://pep8.org/)
- Maximale Zeilenlänge: 100 Zeichen
- Verwende Type Hints wo möglich
- Dokumentiere Funktionen mit Docstrings

```python
def beispiel_funktion(param1: int, param2: str) -> bool:
    """
    Kurze Beschreibung der Funktion.
    
    Args:
        param1: Beschreibung von param1
        param2: Beschreibung von param2
        
    Returns:
        Beschreibung des Rückgabewerts
    """
    return True
```

### Git Commit Messages

Verwende [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Neue Funktion
- `fix:` Bugfix
- `docs:` Dokumentation
- `style:` Formatierung (keine Code-Änderung)
- `refactor:` Code-Refactoring
- `test:` Tests
- `chore:` Wartung

Beispiele:
```
feat: add new enemy type "Flying Enemy"
fix: correct collision detection on platforms
docs: update README with installation instructions
```

## 🎨 Spiel-Design-Richtlinien

### Neue Gegner

- Sollten visuell unterscheidbar sein
- Benötigen eindeutige Bewegungsmuster
- Sollten fair sein (vorhersehbar)

### Neue Level

- Progressive Schwierigkeit
- Genug Plattformen für Flow
- Ausgewogene Item-Verteilung

### Neue Features

- Sollten das Retro-Feeling beibehalten
- Performance beachten (60 FPS)
- Mobile-Kompatibilität wahren

## 🧪 Testing

```bash
# Spiel starten
python main.py

# Syntax-Prüfung
python -m py_compile main.py src/*.py

# Import-Test
python -c "import sys; sys.path.insert(0, 'src'); from game_engine import GameEngine"
```

## 📋 Checkliste für Pull Requests

- [ ] Code folgt dem Projekt-Stil
- [ ] Alle Tests bestanden
- [ ] Dokumentation aktualisiert
- [ ] CHANGELOG.md aktualisiert (bei größeren Änderungen)
- [ ] Keine Hardcoded-Pfade
- [ ] Rückwärtskompatibilität beachtet

## 🏷️ Labels

Wir verwenden folgende Labels:

| Label | Bedeutung |
|-------|-----------|
| `bug` | Etwas funktioniert nicht |
| `enhancement` | Neue Funktion |
| `documentation` | Dokumentation |
| `good first issue` | Gut für Einsteiger |
| `help wanted` | Hilfe gesucht |
| `question` | Frage |

## 💬 Kommunikation

- Sei respektvoll und freundlich
- Akzeptiere konstruktive Kritik
- Fokussiere dich auf das Problem, nicht die Person

## 📜 Lizenz

Durch deinen Beitrag stimmst du zu, dass dein Code unter der MIT-Lizenz veröffentlicht wird.

---

**Vielen Dank für deinen Beitrag!** 🎮✨
