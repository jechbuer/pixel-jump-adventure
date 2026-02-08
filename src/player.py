"""
Spieler-Klasse für Pixel Jump Adventure
"""

import pygame
from typing import Optional
from constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_START_X, PLAYER_START_Y,
    PLAYER_MAX_HEALTH, PLAYER_INVULNERABILITY_FRAMES,
    GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL_SPEED, FRICTION,
    PROJECTILE_SPEED, COLORS
)


class Player:
    """
    Der Spieler-Charakter mit Physik und Animation
    """
    
    def __init__(self, x: float = PLAYER_START_X, y: float = PLAYER_START_Y):
        # Position und Größe
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Geschwindigkeit
        self.vx = 0.0
        self.vy = 0.0
        
        # Zustand
        self.is_grounded = False
        self.is_facing_right = True
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.invulnerable = 0
        
        # Rechteck für Kollision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    @property
    def center_x(self) -> float:
        """X-Koordinate der Mitte"""
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        """Y-Koordinate der Mitte"""
        return self.y + self.height / 2
    
    def update(self, input_left: bool, input_right: bool, 
               input_jump: bool, input_shoot: bool) -> Optional[dict]:
        """
        Aktualisiert den Spieler
        
        Args:
            input_left: Bewegung nach links
            input_right: Bewegung nach rechts
            input_jump: Sprung-Taste
            input_shoot: Schuss-Taste
            
        Returns:
            Projektil-Daten wenn geschossen wurde, sonst None
        """
        projectile = None
        
        # === BEWEGUNG ===
        if input_left:
            self.vx = -MOVE_SPEED
            self.is_facing_right = False
        elif input_right:
            self.vx = MOVE_SPEED
            self.is_facing_right = True
        else:
            self.vx *= FRICTION
        
        # === SPRUNG ===
        if input_jump and self.is_grounded:
            self.vy = JUMP_FORCE
            self.is_grounded = False
        
        # === SCHIESSEN ===
        if input_shoot:
            projectile = self.shoot()
        
        # === PHYSIK ===
        # Gravitation anwenden
        self.vy += GRAVITY
        self.vy = min(self.vy, MAX_FALL_SPEED)
        
        # Position aktualisieren
        self.x += self.vx
        self.y += self.vy
        
        # Rechteck aktualisieren
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Unverwundbarkeit herunterzählen
        if self.invulnerable > 0:
            self.invulnerable -= 1
        
        return projectile
    
    def shoot(self) -> dict:
        """
        Erstellt ein Projektil
        
        Returns:
            Projektil-Daten
        """
        direction = 1 if self.is_facing_right else -1
        
        return {
            'x': self.x + (self.width if direction > 0 else 0),
            'y': self.y + self.height / 3,
            'vx': PROJECTILE_SPEED * direction,
            'vy': 0,
            'width': 12,
            'height': 6,
            'is_player': True
        }
    
    def take_damage(self, amount: int = 1) -> bool:
        """
        Fügt dem Spieler Schaden zu
        
        Args:
            amount: Schadensmenge
            
        Returns:
            True wenn Schaden zugefügt wurde
        """
        if self.invulnerable <= 0:
            self.health -= amount
            self.invulnerable = PLAYER_INVULNERABILITY_FRAMES
            return True
        return False
    
    def heal(self, amount: int = 1) -> None:
        """
        Heilt den Spieler
        
        Args:
            amount: Heilmenge
        """
        self.health = min(self.health + amount, self.max_health)
    
    def respawn(self, x: float = PLAYER_START_X, y: float = PLAYER_START_Y) -> None:
        """
        Setzt den Spieler zurück
        
        Args:
            x, y: Neue Position
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.invulnerable = PLAYER_INVULNERABILITY_FRAMES * 2
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """
        Zeichnet den Spieler
        
        Args:
            surface: Pygame Surface
            camera_x, camera_y: Kamera-Offset
        """
        # Blinken bei Unverwundbarkeit
        if self.invulnerable > 0 and (self.invulnerable // 5) % 2 == 0:
            alpha = 128
        else:
            alpha = 255
        
        # Bildschirm-Position berechnen
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Körper
        body_color = COLORS['player']
        if alpha < 255:
            # Semi-transparent zeichnen
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            temp_surface.fill((*body_color, alpha))
            surface.blit(temp_surface, (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, body_color, 
                           (screen_x, screen_y, self.width, self.height))
        
        # Helm (Oberkante)
        helmet_rect = pygame.Rect(screen_x, screen_y, self.width, 6)
        pygame.draw.rect(surface, COLORS['player_helmet'], helmet_rect)
        
        # Augen (Richtung zeigen)
        eye_offset = 16 if self.is_facing_right else 4
        eye_rect = pygame.Rect(screen_x + eye_offset, screen_y + 8, 8, 8)
        pygame.draw.rect(surface, COLORS['player_eye'], eye_rect)
    
    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck zurück"""
        return self.rect
