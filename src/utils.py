"""
Hilfsfunktionen für Pixel Jump Adventure
"""

import pygame
import random
from typing import Tuple, List
from constants import COLORS


def draw_pixel_text(surface: pygame.Surface, text: str, x: int, y: int, 
                    size: int = 24, color: Tuple[int, int, int] = None,
                    center: bool = False) -> None:
    """
    Zeichnet Pixel-artigen Text
    
    Args:
        surface: Pygame Surface zum Zeichnen
        text: Der anzuzeigende Text
        x, y: Position
        size: Schriftgröße
        color: Textfarbe (default: ui_text)
        center: Ob der Text zentriert werden soll
    """
    if color is None:
        color = COLORS['ui_text']
    
    font = pygame.font.SysFont('courier', size, bold=True)
    text_surface = font.render(text, True, color)
    
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    
    surface.blit(text_surface, (x, y))


def draw_button(surface: pygame.Surface, text: str, x: int, y: int, 
                width: int = 200, height: int = 50,
                hovered: bool = False) -> pygame.Rect:
    """
    Zeichnet einen Pixel-artigen Button
    
    Args:
        surface: Pygame Surface
        text: Button-Text
        x, y: Position
        width, height: Button-Größe
        hovered: Ob der Mauszeiger über dem Button ist
        
    Returns:
        Das Button-Rechteck für Kollisionsprüfung
    """
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    
    # Hintergrund
    bg_color = (167, 139, 250) if hovered else (139, 92, 246)
    pygame.draw.rect(surface, bg_color, button_rect)
    
    # Rand
    pygame.draw.rect(surface, COLORS['platform_light'], button_rect, 2)
    
    # Text
    draw_pixel_text(surface, text, x, y, 18, COLORS['ui_text'], center=True)
    
    return button_rect


def check_rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Prüft Kollision zwischen zwei Rechtecken
    
    Args:
        rect1, rect2: Die zu prüfenden Rechtecke
        
    Returns:
        True wenn Kollision, sonst False
    """
    return rect1.colliderect(rect2)


def lerp(start: float, end: float, t: float) -> float:
    """
    Lineare Interpolation zwischen zwei Werten
    
    Args:
        start: Startwert
        end: Endwert
        t: Interpolationsfaktor (0.0 - 1.0)
        
    Returns:
        Interpolierter Wert
    """
    return start + (end - start) * t


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Begrenzt einen Wert auf einen Bereich
    
    Args:
        value: Der zu begrenzende Wert
        min_val: Minimum
        max_val: Maximum
        
    Returns:
        Begrenzter Wert
    """
    return max(min_val, min(max_val, value))


class Camera:
    """
    Kamera-System für sanftes Scrollen
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothness = 0.1
    
    def update(self, target_x: float, target_y: float, 
               level_width: int, level_height: int) -> None:
        """
        Aktualisiert die Kamera-Position mit sanfter Interpolation
        
        Args:
            target_x, target_y: Zielposition (normalerweise Spieler)
            level_width, level_height: Level-Grenzen
        """
        # Zielposition berechnen (Spieler im linken Drittel)
        target_cam_x = target_x - self.screen_width / 3
        target_cam_y = target_y - self.screen_height / 2
        
        # Sanfte Bewegung
        self.x += (target_cam_x - self.x) * self.smoothness
        self.y += (target_cam_y - self.y) * self.smoothness
        
        # Begrenzen auf Level-Grenzen
        self.x = clamp(self.x, 0, level_width - self.screen_width)
        self.y = clamp(self.y, -200, level_height - self.screen_height)
    
    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """
        Wendet die Kamera-Transformation auf ein Rechteck an
        
        Args:
            rect: Das zu transformierende Rechteck
            
        Returns:
            Transformiertes Rechteck
        """
        return pygame.Rect(
            rect.x - int(self.x),
            rect.y - int(self.y),
            rect.width,
            rect.height
        )
    
    def apply_pos(self, x: float, y: float) -> Tuple[int, int]:
        """
        Wendet die Kamera-Transformation auf eine Position an
        
        Args:
            x, y: Die zu transformierende Position
            
        Returns:
            Transformierte Position als Tuple
        """
        return (int(x - self.x), int(y - self.y))


class Particle:
    """
    Einzelner Partikel für Effekte
    """
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 size: int, color: Tuple[int, int, int], lifetime: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
    def update(self) -> bool:
        """
        Aktualisiert den Partikel
        
        Returns:
            False wenn der Partikel tot ist
        """
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """
        Zeichnet den Partikel
        
        Args:
            surface: Pygame Surface
            camera: Kamera für Offset
        """
        alpha = self.lifetime / self.max_lifetime
        # Erstelle eine Kopie der Farbe mit Alpha
        color_with_alpha = tuple(int(c * alpha) for c in self.color)
        
        pos = camera.apply_pos(self.x, self.y)
        pygame.draw.rect(surface, color_with_alpha, 
                        (pos[0], pos[1], self.size, self.size))


class ParticleSystem:
    """
    Verwaltet alle Partikel-Effekte
    """
    
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_particle(self, x: float, y: float, vx: float, vy: float,
                     size: int, color: Tuple[int, int, int], lifetime: int) -> None:
        """Fügt einen neuen Partikel hinzu"""
        self.particles.append(Particle(x, y, vx, vy, size, color, lifetime))
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], 
                         count: int = 10) -> None:
        """Erstellt eine Explosion aus Partikeln"""
        for _ in range(count):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-4, 4)
            size = random.randint(3, 6)
            lifetime = random.randint(20, 30)
            self.add_particle(x, y, vx, vy, size, color, lifetime)
    
    def create_jump_dust(self, x: float, y: float) -> None:
        """Erstellt Staub-Effekt beim Springen"""
        for _ in range(5):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-1, 0)
            size = random.randint(2, 4)
            self.add_particle(x, y, vx, vy, size, COLORS['particle_smoke'], 20)
    
    def create_sparkles(self, x: float, y: float, color: Tuple[int, int, int]) -> None:
        """Erstellt Funkel-Effekt für Collectibles"""
        for _ in range(8):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-3, 3)
            size = random.randint(2, 4)
            self.add_particle(x, y, vx, vy, size, color, 25)
    
    def update(self) -> None:
        """Aktualisiert alle Partikel"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """Zeichnet alle Partikel"""
        for particle in self.particles:
            particle.draw(surface, camera)
    
    def clear(self) -> None:
        """Löscht alle Partikel"""
        self.particles.clear()
