"""
Gegner-Klasse mit Patrouillen-KI für Pixel Jump Adventure
"""

import pygame
import random
from constants import ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, GRAVITY, COLORS


class Enemy:
    """
    Ein Gegner mit Patrouillen-Verhalten
    """
    
    def __init__(self, x: float, y: float, patrol_distance: float, speed: float = None):
        """
        Initialisiert einen Gegner
        
        Args:
            x, y: Startposition
            patrol_distance: Wie weit der Gegner patrouilliert
            speed: Bewegungsgeschwindigkeit (default: ENEMY_SPEED)
        """
        self.x = x
        self.y = y
        self.start_x = x
        self.patrol_distance = patrol_distance
        
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = speed if speed is not None else ENEMY_SPEED
        self.direction = 1  # 1 = rechts, -1 = links
        
        self.vx = 0.0
        self.vy = 0.0
        self.health = 1
        
        # Animation
        self.anim_timer = 0
        self.anim_frame = 0
        
        # Rechteck für Kollision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, platforms: list) -> None:
        """
        Aktualisiert den Gegner
        
        Args:
            platforms: Liste der Plattformen für Bodenkollision
        """
        if self.health <= 0:
            return
        
        # === PATROUILLEN-BEWEGUNG ===
        self.vx = self.speed * self.direction
        self.x += self.vx
        
        # Richtung umkehren am Patrouillen-Ende
        distance = self.x - self.start_x
        if distance > self.patrol_distance:
            self.direction = -1
            self.x = self.start_x + self.patrol_distance
        elif distance < 0:
            self.direction = 1
            self.x = self.start_x
        
        # === GRAVITATION ===
        self.vy += GRAVITY * 0.5
        self.y += self.vy
        
        # === BODEN-KOLLISION ===
        feet_rect = pygame.Rect(self.x, self.y + self.height, self.width, 5)
        
        for platform in platforms:
            if feet_rect.colliderect(platform.rect):
                self.vy = 0
                self.y = platform.rect.y - self.height
                break
        
        # Rechteck aktualisieren
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Animation
        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2
    
    def take_damage(self, amount: int = 1) -> bool:
        """
        Fügt dem Gegner Schaden zu
        
        Args:
            amount: Schadensmenge
            
        Returns:
            True wenn der Gegner besiegt wurde
        """
        self.health -= amount
        return self.health <= 0
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """
        Zeichnet den Gegner
        
        Args:
            surface: Pygame Surface
            camera_x, camera_y: Kamera-Offset
        """
        if self.health <= 0:
            return
        
        # Bildschirm-Position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Animation-Offset für "Wackeln"
        wobble = 0 if self.anim_frame == 0 else 1
        
        # Körper
        body_rect = pygame.Rect(screen_x, screen_y + wobble, self.width, self.height)
        pygame.draw.rect(surface, COLORS['enemy'], body_rect)
        
        # Augen (gelb)
        eye_size = 6
        eye_y = screen_y + 6 + wobble
        
        # Linkes Auge
        left_eye = pygame.Rect(screen_x + 4, eye_y, eye_size, eye_size)
        pygame.draw.rect(surface, COLORS['enemy_eye'], left_eye)
        
        # Rechtes Auge
        right_eye = pygame.Rect(screen_x + 14, eye_y, eye_size, eye_size)
        pygame.draw.rect(surface, COLORS['enemy_eye'], right_eye)
        
        # Pupillen (dunkelrot - böser Blick)
        pupil_size = 2
        pupil_y = eye_y + 2
        
        left_pupil = pygame.Rect(screen_x + 6, pupil_y, pupil_size, pupil_size)
        right_pupil = pygame.Rect(screen_x + 16, pupil_y, pupil_size, pupil_size)
        pygame.draw.rect(surface, COLORS['enemy_pupil'], left_pupil)
        pygame.draw.rect(surface, COLORS['enemy_pupil'], right_pupil)
    
    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck zurück"""
        return self.rect
    
    def is_alive(self) -> bool:
        """Prüft ob der Gegner noch lebt"""
        return self.health > 0


class EnemyManager:
    """
    Verwaltet alle Gegner im Spiel
    """
    
    def __init__(self):
        self.enemies: list[Enemy] = []
    
    def add_enemy(self, x: float, y: float, patrol_distance: float, speed: float = None) -> None:
        """Fügt einen neuen Gegner hinzu"""
        self.enemies.append(Enemy(x, y, patrol_distance, speed))
    
    def update(self, platforms: list) -> None:
        """Aktualisiert alle Gegner"""
        for enemy in self.enemies:
            enemy.update(platforms)
        
        # Entferne tote Gegner
        self.enemies = [e for e in self.enemies if e.is_alive()]
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Zeichnet alle Gegner"""
        for enemy in self.enemies:
            enemy.draw(surface, camera_x, camera_y)
    
    def check_collision_with_player(self, player_rect: pygame.Rect, player_vy: float) -> tuple:
        """
        Prüft Kollision mit Spieler
        
        Args:
            player_rect: Spieler-Rechteck
            player_vy: Vertikale Geschwindigkeit des Spielers
            
        Returns:
            (kollision_typ, gegner_index oder None)
            kollision_typ: 'jump' (Spieler springt auf Gegner), 'hit' (Spieler wird getroffen), None
        """
        for i, enemy in enumerate(self.enemies):
            if not enemy.is_alive():
                continue
            
            if player_rect.colliderect(enemy.get_rect()):
                # Prüfe ob Spieler auf Gegner springt
                if player_vy > 0 and player_rect.bottom < enemy.get_rect().centery:
                    return ('jump', i)
                else:
                    return ('hit', i)
        
        return (None, None)
    
    def check_collision_with_projectile(self, projectile_rect: pygame.Rect) -> int:
        """
        Prüft Kollision mit Projektil
        
        Args:
            projectile_rect: Projektil-Rechteck
            
        Returns:
            Index des getroffenen Gegners oder -1
        """
        for i, enemy in enumerate(self.enemies):
            if enemy.is_alive() and projectile_rect.colliderect(enemy.get_rect()):
                return i
        return -1
    
    def get_enemy(self, index: int) -> Optional[Enemy]:
        """Gibt einen Gegner anhand des Index zurück"""
        if 0 <= index < len(self.enemies):
            return self.enemies[index]
        return None
    
    def clear(self) -> None:
        """Löscht alle Gegner"""
        self.enemies.clear()
    
    def count_alive(self) -> int:
        """Zählt lebende Gegner"""
        return sum(1 for e in self.enemies if e.is_alive())
