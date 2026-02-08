"""
Konstanten für Pixel Jump Adventure
Alle wichtigen Spiel-Parameter an einem Ort
"""

import pygame

# =============================================================================
# FENSTER-EINSTELLUNGEN
# =============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "Pixel Jump Adventure"

# =============================================================================
# PHYSIK-KONSTANTEN
# =============================================================================
GRAVITY = 0.6
JUMP_FORCE = -14
MOVE_SPEED = 5
MAX_FALL_SPEED = 12
FRICTION = 0.85
PROJECTILE_SPEED = 10
TILE_SIZE = 32

# =============================================================================
# SPIELER-EINSTELLUNGEN
# =============================================================================
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 40
PLAYER_START_X = 100
PLAYER_START_Y = 300
PLAYER_MAX_HEALTH = 3
PLAYER_INVULNERABILITY_FRAMES = 60

# =============================================================================
# GEGNER-EINSTELLUNGEN
# =============================================================================
ENEMY_WIDTH = 24
ENEMY_HEIGHT = 30
ENEMY_SPEED = 1.5
ENEMY_PATROL_DISTANCE = 100

# =============================================================================
# FARBPALETTE (Retro-Pixel-Stil)
# =============================================================================
COLORS = {
    # Hintergrund
    'bg_dark': (15, 23, 42),      # #0f172a
    'bg_light': (30, 41, 59),      # #1e293b
    'bg_mid': (51, 65, 85),        # #334155
    
    # Spieler
    'player': (74, 222, 128),      # #4ade80
    'player_helmet': (34, 197, 94), # #22c55e
    'player_eye': (31, 41, 55),    # #1f2937
    
    # Plattformen
    'platform': (139, 92, 246),    # #8b5cf6
    'platform_light': (167, 139, 250), # #a78bfa
    'platform_dark': (109, 40, 217),   # #6d28d9
    
    # Gegner
    'enemy': (239, 68, 68),        # #ef4444
    'enemy_eye': (254, 240, 138),  # #fef08a
    'enemy_pupil': (127, 29, 29),  # #7f1d1d
    
    # Items
    'coin': (251, 191, 36),        # #fbbf24
    'coin_dark': (245, 158, 11),   # #f59e0b
    'gem': (236, 72, 153),         # #ec4899
    'heart': (239, 68, 68),        # #ef4444
    
    # Projektile
    'projectile_player': (56, 189, 248),  # #38bdf8
    'projectile_glow': (125, 211, 252),   # #7dd3fc
    
    # UI
    'ui_text': (241, 245, 249),    # #f1f5f9
    'ui_muted': (148, 163, 184),   # #94a3b8
    'ui_accent': (251, 191, 36),   # #fbbf24
    'ui_danger': (239, 68, 68),    # #ef4444
    'ui_success': (74, 222, 128),  # #4ade80
    
    # Partikel
    'particle_smoke': (203, 213, 225),  # #cbd5e1
    'particle_sparkle': (251, 191, 36), # #fbbf24
}

# =============================================================================
# LEVEL-KONFIGURATION
# =============================================================================
LEVEL_WIDTH = 3200
LEVEL_HEIGHT = 600

# Plattform-Layouts (x, y, breite_in_tiles)
PLATFORM_LAYOUTS = [
    (200, 450, 3),
    (400, 350, 2),
    (600, 250, 3),
    (900, 400, 2),
    (1100, 300, 3),
    (1400, 450, 2),
    (1600, 350, 3),
    (1900, 250, 2),
    (2100, 400, 3),
    (2400, 300, 2),
    (2600, 200, 3),
    (2900, 450, 2),
]

# =============================================================================
# PUNKTE-SYSTEM
# =============================================================================
SCORE_COIN = 10
SCORE_GEM = 50
SCORE_ENEMY_JUMP = 100
SCORE_ENEMY_SHOT = 50

# =============================================================================
# ZUSTÄNDE
# =============================================================================
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAMEOVER = 'gameover'
STATE_VICTORY = 'victory'

# =============================================================================
# TASTENBELEGUNG
# =============================================================================
KEY_LEFT = [pygame.K_LEFT, pygame.K_a]
KEY_RIGHT = [pygame.K_RIGHT, pygame.K_d]
KEY_JUMP = [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
KEY_SHOOT = [pygame.K_f, pygame.K_LSHIFT, pygame.K_RSHIFT]
KEY_PAUSE = [pygame.K_ESCAPE, pygame.K_p]
