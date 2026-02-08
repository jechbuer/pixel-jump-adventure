"""
Projektil-System für Pixel Jump Adventure
"""

import pygame
from constants import COLORS


class Projectile:
    """
    Ein Projektil (Schuss)
    """
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 width: int = 12, height: int = 6, is_player: bool = True):
        """
        Initialisiert ein Projektil
        
        Args:
            x, y: Startposition
            vx, vy: Geschwindigkeit
            width, height: Größe
            is_player: True wenn Spieler-Projektil, False wenn Gegner-Projektil
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.is_player = is_player
        self.active = True
        self.lifetime = 60  # Frames bis das Projektil verschwindet
        
        # Rechteck für Kollision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, level_width: int) -> bool:
        """
        Aktualisiert das Projektil
        
        Args:
            level_width: Breite des Levels für Grenzen-Prüfung
            
        Returns:
            False wenn das Projektil inaktiv ist
        """
        if not self.active:
            return False
        
        # Bewegung
        self.x += self.vx
        self.y += self.vy
        
        # Rechteck aktualisieren
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Lebenszeit herunterzählen
        self.lifetime -= 1
        
        # Prüfe ob außerhalb des Levels oder Lebenszeit abgelaufen
        if self.lifetime <= 0 or self.x < 0 or self.x > level_width:
            self.active = False
            return False
        
        return True
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """
        Zeichnet das Projektil
        
        Args:
            surface: Pygame Surface
            camera_x, camera_y: Kamera-Offset
        """
        if not self.active:
            return
        
        # Bildschirm-Position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Farbe basierend auf Besitzer
        if self.is_player:
            main_color = COLORS['projectile_player']
            glow_color = COLORS['projectile_glow']
        else:
            main_color = COLORS['enemy']
            glow_color = COLORS['enemy_eye']
        
        # Hauptkörper
        pygame.draw.rect(surface, main_color, 
                        (screen_x, screen_y, self.width, self.height))
        
        # Leuchteffekt
        pygame.draw.rect(surface, glow_color,
                        (screen_x + 2, screen_y + 1, self.width - 4, self.height - 2))
    
    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck zurück"""
        return self.rect
    
    def deactivate(self) -> None:
        """Deaktiviert das Projektil"""
        self.active = False


class ProjectileManager:
    """
    Verwaltet alle Projektile im Spiel
    """
    
    def __init__(self):
        self.projectiles: list[Projectile] = []
    
    def add_projectile(self, x: float, y: float, vx: float, vy: float,
                       width: int = 12, height: int = 6, is_player: bool = True) -> None:
        """Fügt ein neues Projektil hinzu"""
        self.projectiles.append(Projectile(x, y, vx, vy, width, height, is_player))
    
    def add_player_shot(self, x: float, y: float, direction: int, speed: float = 10) -> None:
        """
        Fügt einen Spieler-Schuss hinzu
        
        Args:
            x, y: Startposition
            direction: 1 für rechts, -1 für links
            speed: Geschwindigkeit
        """
        self.add_projectile(x, y, speed * direction, 0, is_player=True)
    
    def update(self, level_width: int) -> None:
        """
        Aktualisiert alle Projektile
        
        Args:
            level_width: Breite des Levels
        """
        # Aktualisiere und entferne inaktive Projektile
        self.projectiles = [p for p in self.projectiles if p.update(level_width)]
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Zeichnet alle Projektile"""
        for projectile in self.projectiles:
            projectile.draw(surface, camera_x, camera_y)
    
    def check_collision_with_rect(self, rect: pygame.Rect, only_player: bool = True) -> bool:
        """
        Prüft Kollision mit einem Rechteck
        
        Args:
            rect: Das zu prüfende Rechteck
            only_player: Nur Spieler-Projektile prüfen
            
        Returns:
            True wenn Kollision, das Projektil wird deaktiviert
        """
        for projectile in self.projectiles:
            if not projectile.active:
                continue
            
            if only_player and not projectile.is_player:
                continue
            
            if projectile.get_rect().colliderect(rect):
                projectile.deactivate()
                return True
        
        return False
    
    def get_player_projectiles(self) -> list[Projectile]:
        """Gibt alle Spieler-Projektile zurück"""
        return [p for p in self.projectiles if p.is_player and p.active]
    
    def clear(self) -> None:
        """Löscht alle Projektile"""
        self.projectiles.clear()
    
    def count_active(self) -> int:
        """Zählt aktive Projektile"""
        return sum(1 for p in self.projectiles if p.active)
