#!/usr/bin/env python3
"""
Pixel Jump Adventure - Ein 2D-Jump-and-Run-Spiel im Retro-Stil

Ein klassisches Plattform-Spiel inspiriert von Commander Keen und anderen
Retro-Titeln. Implementiert mit Python und Pygame.

Steuerung:
    - Pfeiltasten / A,D: Bewegen
    - Leertaste / W: Springen
    - F: Schießen
    - ESC: Pause

Autor: AI Assistant
Version: 1.0.0
"""

import sys
import os

# Füge src-Verzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_engine import GameEngine


def main():
    """
    Hauptfunktion - Startet das Spiel
    """
    print("=" * 60)
    print("  PIXEL JUMP ADVENTURE")
    print("  Ein Retro 2D-Jump-and-Run-Spiel")
    print("=" * 60)
    print()
    print("Steuerung:")
    print("  ← / → oder A / D  - Bewegen")
    print("  SPACE oder W      - Springen")
    print("  F                 - Schießen")
    print("  ESC               - Pause")
    print()
    print("Ziel: Sammle alle Münzen und Edelsteine!")
    print("      Besiege die roten Gegner!")
    print()
    print("Drücke STRG+C zum Beenden")
    print("=" * 60)
    print()
    
    try:
        # Spiel initialisieren und starten
        game = GameEngine()
        game.run()
        
    except KeyboardInterrupt:
        print("\nSpiel beendet.")
        
    except Exception as e:
        print(f"\nFehler: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
