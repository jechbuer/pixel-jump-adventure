"""
Sammelbare Items für Pixel Jump Adventure
"""

import pygame
import math
from constants import COLORS, SCORE_COIN, SCORE_GEM


class Collectible:
    """
    Ein sammelbares Item (Münze, Edelstein, Herz)
    """
    
    def __init__(self, x: float, y: float, item_type: str = 'coin'):
        """
        Initialisiert ein sammelbares Item
        
        Args:
            x, y: Position
            item_type: 'coin', 'gem', oder 'health'
        """
        self.x = x
        self.y = y
        self.type = item_type
        self.collected = False
        
        # Animation
        self.animation_offset = 0
        self.bob_amount = 3
        
        # Größe und Wert basierend auf Typ
        if item_type == 'coin':
            self.width = 16
            self.height = 16
            self.value = SCORE_COIN
            self.color = COLORS['coin']
        elif item_type == 'gem':
            self.width = 20
            self.height = 20
            self.value = SCORE_GEM
            self.color = COLORS['gem']
        elif item_type == 'health':
            self.width = 20
            self.height = 20
            self.value = 0
            self.color = COLORS['heart']
        
        # Rechteck für Kollision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self) -> None:
        """Aktualisiert die Animation"""
        if not self.collected:
            self.animation_offset += 0.1
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """
        Zeichnet das Item
        
        Args:
            surface: Pygame Surface
            camera_x, camera_y: Kamera-Offset
        """
        if self.collected:
            return
        
        # Bobbing-Animation
        bob_offset = math.sin(self.animation_offset) * self.bob_amount
        
        # Bildschirm-Position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y + bob_offset)
        
        if self.type == 'coin':
            self._draw_coin(surface, screen_x, screen_y)
        elif self.type == 'gem':
            self._draw_gem(surface, screen_x, screen_y)
        elif self.type == 'health':
            self._draw_heart(surface, screen_x, screen_y)
    
    def _draw_coin(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Zeichnet eine Münze"""
        # Äußerer Ring
        pygame.draw.rect(surface, COLORS['coin'], (x + 4, y, 8, 16))
        pygame.draw.rect(surface, COLORS['coin'], (x, y + 4, 16, 8))
        
        # Innerer Teil
        pygame.draw.rect(surface, COLORS['coin_dark'], (x + 6, y + 2, 4, 12))
    
    def _draw_gem(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Zeichnet einen Edelstein (Diamant-Form)"""
        center_x = x + self.width // 2
        center_y = y + self.height // 2
        
        # Diamant-Form
        points = [
            (center_x, y),           # Oben
            (x + self.width, center_y),  # Rechts
            (center_x, y + self.height), # Unten
            (x, center_y)             # Links
        ]
        
        pygame.draw.polygon(surface, self.color, points)
        
        # Highlight
        highlight_points = [
            (center_x, y + 4),
            (x + self.width - 4, center_y),
            (center_x, y + self.height - 4),
            (x + 4, center_y)
        ]
        highlight_color = tuple(min(255, c + 40) for c in self.color)
        pygame.draw.polygon(surface, highlight_color, highlight_points)
    
    def _draw_heart(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Zeichnet ein Herz"""
        # Einfaches Herz aus Rechtecken
        pygame.draw.rect(surface, self.color, (x + 4, y + 4, 12, 12))
        pygame.draw.rect(surface, self.color, (x, y + 8, 20, 8))
        
        # Highlight
        pygame.draw.rect(surface, (255, 150, 150), (x + 6, y + 6, 4, 4))
    
    def collect(self) -> int:
        """
        Sammelt das Item ein
        
        Returns:
            Der Wert des Items
        """
        if not self.collected:
            self.collected = True
            return self.value
        return 0
    
    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck zurück"""
        return self.rect
    
    def is_health(self) -> bool:
        """Prüft ob das Item ein Herz ist"""
        return self.type == 'health'


class CollectibleManager:
    """
    Verwaltet alle sammelbaren Items
    """
    
    def __init__(self):
        self.items: list[Collectible] = []
    
    def add_coin(self, x: float, y: float) -> None:
        """Fügt eine Münze hinzu"""
        self.items.append(Collectible(x, y, 'coin'))
    
    def add_gem(self, x: float, y: float) -> None:
        """Fügt einen Edelstein hinzu"""
        self.items.append(Collectible(x, y, 'gem'))
    
    def add_heart(self, x: float, y: float) -> None:
        """Fügt ein Herz hinzu"""
        self.items.append(Collectible(x, y, 'health'))
    
    def add_item(self, x: float, y: float, item_type: str) -> None:
        """Fügt ein Item eines bestimmten Typs hinzu"""
        self.items.append(Collectible(x, y, item_type))
    
    def update(self) -> None:
        """Aktualisiert alle Items"""
        for item in self.items:
            item.update()
    
    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Zeichnet alle Items"""
        for item in self.items:
            item.draw(surface, camera_x, camera_y)
    
    def check_collision_with_player(self, player_rect: pygame.Rect) -> tuple:
        """
        Prüft Kollision mit Spieler
        
        Args:
            player_rect: Spieler-Rechteck
            
        Returns:
            (gesammelt, wert, ist_herz) oder (False, 0, False)
        """
        for item in self.items:
            if not item.collected and player_rect.colliderect(item.get_rect()):
                value = item.collect()
                return (True, value, item.is_health())
        
        return (False, 0, False)
    
    def count_remaining(self) -> int:
        """Zählt nicht gesammelte Items"""
        return sum(1 for item in self.items if not item.collected)
    
    def count_collected(self) -> int:
        """Zählt gesammelte Items"""
        return sum(1 for item in self.items if item.collected)
    
    def clear(self) -> None:
        """Löscht alle Items"""
        self.items.clear()
    
    def generate_level_items(self, platform_layouts: list, tile_size: int = 32) -> None:
        """
        Generiert Items basierend auf Plattform-Layouts
        
        Args:
            platform_layouts: Liste der Plattform-Positionen
            tile_size: Größe eines Tiles
        """
        import random
        
        for x, y, width_tiles in platform_layouts:
            # Chance für Item auf Plattform
            if random.random() > 0.3:
                item_x = x + width_tiles * tile_size / 2 - 10
                item_y = y - 50
                
                # Zufälliger Typ
                if random.random() > 0.7:
                    self.add_gem(item_x, item_y)
                else:
                    self.add_coin(item_x, item_y)
        
        # Zusätzliche Coins in der Luft
        for i in range(20):
            coin_x = 300 + i * 140 + random.random() * 50
            coin_y = 150 + random.random() * 200
            self.add_coin(coin_x, coin_y)
