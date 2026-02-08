"""
Plattform-Klasse für Pixel Jump Adventure
"""

import pygame
from constants import COLORS, TILE_SIZE


class Platform:
    """
    Eine Plattform auf der der Spieler stehen kann
    """
    
    def __init__(self, x: float, y: float, width: int, height: int = None):
        """
        Initialisiert eine Plattform
        
        Args:
            x, y: Position
            width: Breite in Pixeln
            height: Höhe in Pixeln (default: TILE_SIZE)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height if height is not None else TILE_SIZE
        
        # Rechteck für Kollision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """
        Zeichnet die Plattform im Retro-Pixel-Stil
        
        Args:
            surface: Pygame Surface
            camera_x, camera_y: Kamera-Offset
        """
        # Bildschirm-Position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Nur zeichnen wenn auf dem Bildschirm sichtbar
        if screen_x + self.width < 0 or screen_x > surface.get_width():
            return
        if screen_y + self.height < 0 or screen_y > surface.get_height():
            return
        
        # Hauptkörper (Lila)
        main_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
        pygame.draw.rect(surface, COLORS['platform'], main_rect)
        
        # Helle Oberkante (Pixel-Art Detail)
        top_rect = pygame.Rect(screen_x, screen_y, self.width, 4)
        pygame.draw.rect(surface, COLORS['platform_light'], top_rect)
        
        # Dunkle Unterkante (Schatten)
        bottom_rect = pygame.Rect(screen_x, screen_y + self.height - 4, self.width, 4)
        pygame.draw.rect(surface, COLORS['platform_dark'], bottom_rect)
        
        # Optional: Pixel-Muster auf der Plattform
        self._draw_pattern(surface, screen_x, screen_y)
    
    def _draw_pattern(self, surface: pygame.Surface, screen_x: int, screen_y: int) -> None:
        """
        Zeichnet ein dekoratives Pixel-Muster auf die Plattform
        
        Args:
            surface: Pygame Surface
            screen_x, screen_y: Bildschirm-Position
        """
        # Einfaches Muster: Kleine Quadrate
        pattern_color = COLORS['platform_dark']
        
        for i in range(8, self.width - 8, 16):
            if i + 4 < self.width:
                # Kleine Dekoration
                dot_rect = pygame.Rect(screen_x + i, screen_y + 10, 4, 4)
                pygame.draw.rect(surface, pattern_color, dot_rect)
    
    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck zurück"""
        return self.rect


class PlatformManager:
    """
    Verwaltet alle Plattformen im Spiel
    """
    
    def __init__(self):
        self.platforms: list[Platform] = []
    
    def add_platform(self, x: float, y: float, width: int, height: int = None) -> None:
        """Fügt eine neue Plattform hinzu"""
        self.platforms.append(Platform(x, y, width, height))
    
    def create_ground(self, level_width: int, tile_size: int = TILE_SIZE) -> None:
        """
        Erstellt den Boden des Levels
        
        Args:
            level_width: Gesamtbreite des Levels
            tile_size: Größe eines Tiles
        """
        # Boden-Plattformen erstellen
        for x in range(0, level_width, tile_size * 4):
            self.add_platform(x, 600 - tile_size, tile_size * 4, tile_size)
    
    def create_from_layouts(self, layouts: list, tile_size: int = TILE_SIZE) -> None:
        """
        Erstellt Plattformen aus Layout-Daten
        
        Args:
            layouts: Liste von (x, y, width_in_tiles) Tupeln
            tile_size: Größe eines Tiles
        """
        for x, y, width_tiles in layouts:
            self.add_platform(x, y, tile_size * width_tiles, tile_size)
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Zeichnet alle Plattformen"""
        for platform in self.platforms:
            platform.draw(surface, camera_x, camera_y)
    
    def check_collision(self, rect: pygame.Rect) -> Platform:
        """
        Prüft Kollision mit einer Plattform
        
        Args:
            rect: Das zu prüfende Rechteck
            
        Returns:
            Die kollidierende Plattform oder None
        """
        for platform in self.platforms:
            if rect.colliderect(platform.get_rect()):
                return platform
        return None
    
    def get_all_rects(self) -> list:
        """Gibt alle Plattform-Rechtecke zurück"""
        return [p.get_rect() for p in self.platforms]
    
    def clear(self) -> None:
        """Löscht alle Plattformen"""
        self.platforms.clear()
    
    def count(self) -> int:
        """Gibt die Anzahl der Plattformen zurück"""
        return len(self.platforms)
