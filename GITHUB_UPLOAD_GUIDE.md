# GitHub Upload Guide

Diese Anleitung erklärt Schritt für Schritt, wie du das Pixel Jump Adventure Projekt auf GitHub hochlädst.

## 📋 Voraussetzungen

1. **GitHub Account** - Erstelle einen kostenlosen Account auf [github.com](https://github.com)
2. **Git** - Installiere Git von [git-scm.com](https://git-scm.com)
3. **Python** - Sollte bereits installiert sein

## 🔧 Schritt 1: Git konfigurieren

Öffne ein Terminal und konfiguriere Git mit deinen Daten:

```bash
git config --global user.name "Dein Name"
git config --global user.email "dein.email@beispiel.de"
```

## 📁 Schritt 2: Repository erstellen

### Option A: Über die GitHub Website

1. Gehe zu [github.com/new](https://github.com/new)
2. Gib einen Repository-Namen ein: `pixel-jump-adventure`
3. Wähle **Public** (oder Private, wenn du möchtest)
4. Aktiviere **"Add a README file"** (optional)
5. Klicke auf **"Create repository"**

### Option B: Über die GitHub CLI

```bash
# GitHub CLI installieren (falls nicht vorhanden)
# Windows: winget install --id GitHub.cli
# macOS: brew install gh
# Linux: siehe https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Anmelden
gh auth login

# Repository erstellen
gh repo create pixel-jump-adventure --public --description "Ein Retro 2D-Jump-and-Run-Spiel mit Python und Pygame"
```

## 📤 Schritt 3: Code hochladen

### Option A: Mit Git Befehlen (Empfohlen)

```bash
# In das Projektverzeichnis wechseln
cd /pfad/zu/pixel_jump_python

# Git initialisieren
git init

# Alle Dateien zum Staging-Bereich hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit: Pixel Jump Adventure v1.0"

# Remote Repository hinzufügen (ersetze USERNAME mit deinem GitHub-Namen)
git remote add origin https://github.com/USERNAME/pixel-jump-adventure.git

# Code hochladen
git branch -M main
git push -u origin main
```

### Option B: Mit GitHub Desktop

1. Lade [GitHub Desktop](https://desktop.github.com) herunter
2. Melde dich an
3. Klicke auf **"Add an Existing Repository"**
4. Wähle den `pixel_jump_python` Ordner
5. Gib eine Commit-Nachricht ein
6. Klicke auf **"Commit to main"**
7. Klicke auf **"Publish repository"**

### Option C: Direkter Upload (ohne Git)

1. Gehe zu deinem Repository auf GitHub
2. Klicke auf **"Add file"** → **"Upload files"**
3. Ziehe alle Dateien in den Upload-Bereich
4. Gib eine Commit-Nachricht ein
5. Klicke auf **"Commit changes"**

## ✅ Schritt 4: Überprüfen

Nach dem Upload solltest du folgende Struktur auf GitHub sehen:

```
pixel-jump-adventure/
├── .github/
│   └── workflows/
│       └── python-app.yml
├── assets/
│   ├── images/
│   └── sounds/
├── docs/
├── src/
│   ├── constants.py
│   ├── game_engine.py
│   ├── player.py
│   ├── enemy.py
│   ├── platform.py
│   ├── collectible.py
│   ├── projectile.py
│   └── utils.py
├── .gitignore
├── CONTRIBUTING.md
├── GITHUB_UPLOAD_GUIDE.md
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

## 🚀 Schritt 5: Erstes Release erstellen (Optional)

1. Gehe auf GitHub zu **"Releases"** (rechte Seitenleiste)
2. Klicke auf **"Create a new release"**
3. Gib eine Versionsnummer ein: `v1.0.0`
4. Titel: "Pixel Jump Adventure v1.0"
5. Beschreibung: Beschreibe die Features
6. Klicke auf **"Publish release"**

## 🔗 Nützliche Links

- **Dein Repository**: `https://github.com/USERNAME/pixel-jump-adventure`
- **Issues**: `https://github.com/USERNAME/pixel-jump-adventure/issues`
- **Releases**: `https://github.com/USERNAME/pixel-jump-adventure/releases`

## 🐛 Häufige Probleme

### Problem: "fatal: not a git repository"

**Lösung**: Stelle sicher, dass du im richtigen Verzeichnis bist:
```bash
cd /pfad/zu/pixel_jump_python
git init
```

### Problem: "Permission denied"

**Lösung**: Verwende HTTPS mit Token oder SSH:
```bash
# Token-basiert (empfohlen)
git remote set-url origin https://TOKEN@github.com/USERNAME/pixel-jump-adventure.git

# Oder SSH
git remote set-url origin git@github.com:USERNAME/pixel-jump-adventure.git
```

### Problem: "failed to push some refs"

**Lösung**: Pull vor dem Push:
```bash
git pull origin main --rebase
git push origin main
```

## 📝 Git Befehle Cheatsheet

```bash
# Status prüfen
git status

# Änderungen anzeigen
git diff

# Dateien hinzufügen
git add dateiname.py
git add .                    # Alle Dateien

# Commit erstellen
git commit -m "Beschreibung"

# Hochladen
git push origin main

# Herunterladen
git pull origin main

# Verlauf anzeigen
git log --oneline

# Branch wechseln
git checkout branch-name
```

## 🎉 Fertig!

Dein Projekt ist jetzt auf GitHub! Teile den Link mit Freunden:
```
https://github.com/USERNAME/pixel-jump-adventure
```

---

**Hilfe benötigt?**
- [GitHub Docs](https://docs.github.com)
- [Git Dokumentation](https://git-scm.com/doc)
- [GitHub Community](https://github.community)
