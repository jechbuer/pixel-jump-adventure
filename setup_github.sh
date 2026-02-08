#!/bin/bash
# GitHub Upload Script für Pixel Jump Adventure
# Führe dieses Skript im Projektverzeichnis aus

echo "🎮 Pixel Jump Adventure - GitHub Upload"
echo "========================================"
echo ""

# GitHub Username
USERNAME="jechbuer"
REPO_NAME="pixel-jump-adventure"

echo "📋 Konfiguration:"
echo "  Username: $USERNAME"
echo "  Repository: $REPO_NAME"
echo ""

# Prüfe ob Git installiert ist
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert!"
    echo "   Installiere Git von: https://git-scm.com"
    exit 1
fi

echo "✅ Git gefunden"
echo ""

# Git konfigurieren (falls noch nicht geschehen)
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️  Git Konfiguration:"
    read -p "Dein Name: " git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    read -p "Deine Email: " git_email
    git config --global user.email "$git_email"
fi

# Git initialisieren
echo ""
echo "🔄 Initialisiere Git..."
if [ -d ".git" ]; then
    echo "   Git ist bereits initialisiert"
else
    git init --initial-branch=main
    echo "   ✅ Git initialisiert"
fi

# Dateien hinzufügen
echo ""
echo "📁 Füge Dateien hinzu..."
git add .
echo "   ✅ Dateien hinzugefügt"

# Commit erstellen
echo ""
echo "💾 Erstelle Commit..."
git commit -m "🎮 Initial commit: Pixel Jump Adventure v1.0"
echo "   ✅ Commit erstellt"

# Remote hinzufügen
echo ""
echo "🔗 Verbinde mit GitHub..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
echo "   ✅ Remote hinzugefügt"

# Hochladen
echo ""
echo "📤 Lade auf GitHub hoch..."
echo "   (Du wirst möglicherweise nach deinem GitHub-Passwort oder Token gefragt)"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ERFOLG!"
    echo ""
    echo "Dein Projekt ist jetzt live auf:"
    echo "  🌐 https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "Nächste Schritte:"
    echo "  1. Besuche dein Repository auf GitHub"
    echo "  2. Erstelle ein Release (optional)"
    echo "  3. Teile den Link mit Freunden!"
else
    echo ""
    echo "❌ Fehler beim Hochladen!"
    echo ""
    echo "Mögliche Lösungen:"
    echo "  1. Erstelle das Repository erst auf GitHub:"
    echo "     https://github.com/new"
    echo "  2. Verwende einen Personal Access Token:"
    echo "     https://github.com/settings/tokens"
    echo "  3. Prüfe deinen Username: $USERNAME"
fi

echo ""
echo "========================================"
