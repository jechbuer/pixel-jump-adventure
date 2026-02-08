"""
Haupt-Spielengine für Pixel Jump Adventure
Verwaltet Spiel-Loop, Physik, Rendering und Zustände
"""

import pygame
import random
import math
from typing import Optional

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE,
    LEVEL_WIDTH, LEVEL_HEIGHT, TILE_SIZE,
    PLATFORM_LAYOUTS, COLORS, STATE_MENU, STATE_PLAYING, 
    STATE_PAUSED, STATE_GAMEOVER, STATE_VICTORY,
    SCORE_ENEMY_JUMP, SCORE_ENEMY_SHOT, PLAYER_START_X, PLAYER_START_Y
)
from player import Player
from enemy import Enemy, EnemyManager
from platform import Platform, PlatformManager
from collectible import Collectible, CollectibleManager
from projectile import Projectile, ProjectileManager
from utils import Camera, ParticleSystem, draw_pixel_text, draw_button


class GameEngine:
    """
    Hauptklasse die das komplette Spiel verwaltet
    """
    
    def __init__(self):
        """Initialisiert Pygame und alle Spiel-Systeme"""
        # Pygame initialisieren
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        # Fenster erstellen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Spiel-Zustand
        self.state = STATE_MENU
        self.score = 0
        
        # Kamera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Partikel-System
        self.particles = ParticleSystem()
        
        # Spiel-Objekte
        self.player: Optional[Player] = None
        self.platforms = PlatformManager()
        self.enemies = EnemyManager()
        self.collectibles = CollectibleManager()
        self.projectiles = ProjectileManager()
        
        # Eingabe-Zustand
        self.input_left = False
        self.input_right = False
        self.input_jump = False
        self.input_shoot = False
        self.input_shoot_pressed = False  # Für Einzel-Schuss
        
        # UI-Elemente
        self.menu_buttons = []
        self.pause_buttons = []
        self.game_over_buttons = []
        self.victory_buttons = []
        
        # Font für UI
        self.font_large = pygame.font.SysFont('courier', 48, bold=True)
        self.font_medium = pygame.font.SysFont('courier', 24, bold=True)
        self.font_small = pygame.font.SysFont('courier', 14, bold=True)
        
        # Level initialisieren
        self._init_level()
    
    def _init_level(self) -> None:
        """Initialisiert das Level mit Plattformen, Gegnern und Items"""
        # Plattformen erstellen
        self.platforms.create_ground(LEVEL_WIDTH, TILE_SIZE)
        self.platforms.create_from_layouts(PLATFORM_LAYOUTS, TILE_SIZE)
        
        # Gegner erstellen
        for x, y, width_tiles in PLATFORM_LAYOUTS:
            if random.random() > 0.5:
                enemy_x = x + 20
                enemy_y = y - 35
                patrol_dist = width_tiles * TILE_SIZE - 40
                self.enemies.add_enemy(enemy_x, enemy_y, patrol_dist)
        
        # Items erstellen
        self.collectibles.generate_level_items(PLATFORM_LAYOUTS, TILE_SIZE)
        
        # Spieler erstellen
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
    
    def reset_game(self) -> None:
        """Setzt das Spiel zurück"""
        self.score = 0
        self.state = STATE_PLAYING
        
        # Spieler zurücksetzen
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        
        # Gegner zurücksetzen
        self.enemies.clear()
        for x, y, width_tiles in PLATFORM_LAYOUTS:
            if random.random() > 0.5:
                enemy_x = x + 20
                enemy_y = y - 35
                patrol_dist = width_tiles * TILE_SIZE - 40
                self.enemies.add_enemy(enemy_x, enemy_y, patrol_dist)
        
        # Items zurücksetzen
        self.collectibles.clear()
        self.collectibles.generate_level_items(PLATFORM_LAYOUTS, TILE_SIZE)
        
        # Projektile löschen
        self.projectiles.clear()
        
        # Partikel löschen
        self.particles.clear()
        
        # Kamera zurücksetzen
        self.camera.x = 0
        self.camera.y = 0
    
    def handle_events(self) -> None:
        """Verarbeitet alle Pygame-Events"""
        self.input_shoot_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
        
        # Maus-Position für Button-Hover
        self.mouse_pos = pygame.mouse.get_pos()
    
    def _handle_keydown(self, key: int) -> None:
        """Verarbeitet Tastendruck"""
        from constants import KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_SHOOT, KEY_PAUSE
        
        if key in KEY_LEFT:
            self.input_left = True
        elif key in KEY_RIGHT:
            self.input_right = True
        elif key in KEY_JUMP:
            self.input_jump = True
        elif key in KEY_SHOOT:
            self.input_shoot = True
            self.input_shoot_pressed = True
        elif key in KEY_PAUSE:
            self._toggle_pause()
    
    def _handle_keyup(self, key: int) -> None:
        """Verarbeitet Tastenloslassen"""
        from constants import KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_SHOOT
        
        if key in KEY_LEFT:
            self.input_left = False
        elif key in KEY_RIGHT:
            self.input_right = False
        elif key in KEY_JUMP:
            self.input_jump = False
        elif key in KEY_SHOOT:
            self.input_shoot = False
    
    def _handle_mouse_click(self, pos: tuple) -> None:
        """Verarbeitet Mausklicks für Buttons"""
        if self.state == STATE_MENU:
            self._check_menu_buttons(pos)
        elif self.state == STATE_PAUSED:
            self._check_pause_buttons(pos)
        elif self.state == STATE_GAMEOVER:
            self._check_gameover_buttons(pos)
        elif self.state == STATE_VICTORY:
            self._check_victory_buttons(pos)
    
    def _toggle_pause(self) -> None:
        """Wechselt zwischen Pause und Spiel"""
        if self.state == STATE_PLAYING:
            self.state = STATE_PAUSED
        elif self.state == STATE_PAUSED:
            self.state = STATE_PLAYING
    
    def _check_menu_buttons(self, pos: tuple) -> None:
        """Prüft Menü-Button-Klicks"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 + 20
        
        if self._is_button_clicked(pos, center_x, center_y, 200, 50):
            self.reset_game()
    
    def _check_pause_buttons(self, pos: tuple) -> None:
        """Prüft Pause-Menü Button-Klicks"""
        center_x = SCREEN_WIDTH // 2
        
        # Weiter-Button
        if self._is_button_clicked(pos, center_x, 360, 200, 50):
            self.state = STATE_PLAYING
        
        # Neustart-Button
        if self._is_button_clicked(pos, center_x, 420, 200, 50):
            self.reset_game()
    
    def _check_gameover_buttons(self, pos: tuple) -> None:
        """Prüft Game Over Button-Klicks"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 + 50
        
        if self._is_button_clicked(pos, center_x, center_y, 200, 50):
            self.reset_game()
    
    def _check_victory_buttons(self, pos: tuple) -> None:
        """Prüft Victory Button-Klicks"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 + 50
        
        if self._is_button_clicked(pos, center_x, center_y, 200, 50):
            self.reset_game()
    
    def _is_button_clicked(self, mouse_pos: tuple, btn_x: int, btn_y: int, 
                          btn_w: int, btn_h: int) -> bool:
        """Prüft ob ein Button geklickt wurde"""
        rect = pygame.Rect(btn_x - btn_w // 2, btn_y - btn_h // 2, btn_w, btn_h)
        return rect.collidepoint(mouse_pos)
    
    def update(self) -> None:
        """Aktualisiert den Spiel-Zustand"""
        if self.state != STATE_PLAYING:
            return
        
        # === SPIELER AKTUALISIEREN ===
        projectile_data = self.player.update(
            self.input_left, self.input_right, 
            self.input_jump, self.input_shoot_pressed
        )
        
        # Projektil hinzufügen wenn geschossen
        if projectile_data:
            self.projectiles.add_projectile(
                projectile_data['x'], projectile_data['y'],
                projectile_data['vx'], projectile_data['vy'],
                projectile_data['width'], projectile_data['height'],
                projectile_data['is_player']
            )
        
        # === KOLLISIONEN PRÜFEN ===
        self._check_collisions()
        
        # === ANDERE SYSTEME AKTUALISIEREN ===
        # Plattformen (keine Updates nötig, statisch)
        
        # Gegner
        self.enemies.update(self.platforms.platforms)
        
        # Items
        self.collectibles.update()
        
        # Projektile
        self.projectiles.update(LEVEL_WIDTH)
        
        # Partikel
        self.particles.update()
        
        # Kamera
        self.camera.update(
            self.player.x, self.player.y,
            LEVEL_WIDTH, LEVEL_HEIGHT
        )
        
        # === SPIEL-ZUSTAND PRÜFEN ===
        self._check_game_state()
    
    def _check_collisions(self) -> None:
        """Prüft alle Kollisionen"""
        player_rect = self.player.get_rect()
        
        # === SPIELER vs PLATTFORMEN ===
        self.player.is_grounded = False
        
        # Füße-Rechteck für Boden-Kollision
        feet_rect = pygame.Rect(
            player_rect.x, player_rect.y + player_rect.height - 5,
            player_rect.width, 10
        )
        
        for platform in self.platforms.platforms:
            plat_rect = platform.get_rect()
            
            # Vertikale Kollision (Landen)
            if feet_rect.colliderect(plat_rect) and self.player.vy >= 0:
                if self.player.y + self.player.height <= plat_rect.y + 20:
                    self.player.y = plat_rect.y - self.player.height
                    self.player.vy = 0
                    self.player.is_grounded = True
                    player_rect.y = int(self.player.y)
                    feet_rect.y = int(self.player.y + self.player.height - 5)
            
            # Horizontale Kollision
            if player_rect.colliderect(plat_rect):
                # Von links
                if self.player.vx > 0 and player_rect.right > plat_rect.left:
                    if player_rect.left < plat_rect.left:
                        self.player.x = plat_rect.left - self.player.width
                        self.player.vx = 0
                # Von rechts
                elif self.player.vx < 0 and player_rect.left < plat_rect.right:
                    if player_rect.right > plat_rect.right:
                        self.player.x = plat_rect.right
                        self.player.vx = 0
        
        # === SPIELER vs GEGNER ===
        collision_type, enemy_idx = self.enemies.check_collision_with_player(
            player_rect, self.player.vy
        )
        
        if collision_type == 'jump':
            # Spieler springt auf Gegner
            enemy = self.enemies.get_enemy(enemy_idx)
            if enemy and enemy.take_damage():
                self.player.vy = -7  # Kleiner Bounce
                self.score += SCORE_ENEMY_JUMP
                self.particles.create_explosion(
                    enemy.x + enemy.width / 2, 
                    enemy.y + enemy.height / 2,
                    COLORS['enemy']
                )
        elif collision_type == 'hit':
            # Spieler wird getroffen
            if self.player.take_damage():
                # Schaden genommen
                pass
        
        # === SPIELER vs ITEMS ===
        collected, value, is_health = self.collectibles.check_collision_with_player(player_rect)
        
        if collected:
            if is_health:
                self.player.heal()
            else:
                self.score += value
            
            self.particles.create_sparkles(
                self.player.center_x, self.player.center_y,
                COLORS['coin'] if not is_health else COLORS['heart']
            )
        
        # === PROJEKTILE vs GEGNER ===
        for projectile in self.projectiles.get_player_projectiles():
            enemy_idx = self.enemies.check_collision_with_projectile(projectile.get_rect())
            if enemy_idx >= 0:
                enemy = self.enemies.get_enemy(enemy_idx)
                if enemy and enemy.take_damage():
                    self.score += SCORE_ENEMY_SHOT
                    self.particles.create_explosion(
                        enemy.x + enemy.width / 2,
                        enemy.y + enemy.height / 2,
                        COLORS['enemy']
                    )
                projectile.deactivate()
        
        # === FALLEN AUS DER WELT ===
        if self.player.y > LEVEL_HEIGHT + 100:
            if self.player.take_damage(1):
                self.player.respawn()
    
    def _check_game_state(self) -> None:
        """Prüft Spiel-Endbedingungen"""
        # Game Over
        if self.player.health <= 0:
            self.state = STATE_GAMEOVER
            return
        
        # Victory (alle Items gesammelt)
        if self.collectibles.count_remaining() == 0 and self.collectibles.count_collected() > 0:
            self.state = STATE_VICTORY
    
    def draw(self) -> None:
        """Zeichnet das komplette Spiel"""
        # Hintergrund löschen
        self.screen.fill(COLORS['bg_dark'])
        
        # === PARALLAX-HINTERGRUND ===
        self._draw_parallax_background()
        
        # === WELT-ELEMENTE (mit Kamera-Offset) ===
        cam_x = self.camera.x
        cam_y = self.camera.y
        
        # Plattformen
        self.platforms.draw(self.screen, cam_x, cam_y)
        
        # Items
        self.collectibles.draw(self.screen, cam_x, cam_y)
        
        # Gegner
        self.enemies.draw(self.screen, cam_x, cam_y)
        
        # Spieler
        if self.player:
            self.player.draw(self.screen, cam_x, cam_y)
        
        # Projektile
        self.projectiles.draw(self.screen, cam_x, cam_y)
        
        # Partikel
        self.particles.draw(self.screen, cam_x, cam_y)
        
        # === UI (ohne Kamera-Offset) ===
        self._draw_ui()
        
        # === MENÜS ===
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PAUSED:
            self._draw_pause_menu()
        elif self.state == STATE_GAMEOVER:
            self._draw_game_over()
        elif self.state == STATE_VICTORY:
            self._draw_victory()
        
        # Bildschirm aktualisieren
        pygame.display.flip()
    
    def _draw_parallax_background(self) -> None:
        """Zeichnet den Parallax-Hintergrund"""
        layers = [
            (0.1, COLORS['bg_dark']),
            (0.3, COLORS['bg_light']),
            (0.5, COLORS['bg_mid'])
        ]
        
        for i, (speed, color) in enumerate(layers):
            offset_x = (self.camera.x * speed) % SCREEN_WIDTH
            
            for j in range(-1, 2):
                x = offset_x + j * SCREEN_WIDTH
                
                if i == 0:
                    # Ferne Sterne
                    for k in range(20):
                        star_x = int((x + k * 80) % SCREEN_WIDTH)
                        star_y = (k * 37) % SCREEN_HEIGHT
                        self.screen.set_at((star_x, star_y), (200, 200, 200))
                
                elif i == 1:
                    # Mittlere Berge
                    points = []
                    for px in range(0, SCREEN_WIDTH + 50, 50):
                        height = 100 + math.sin((px + x) * 0.01) * 50
                        points.append((px, SCREEN_HEIGHT - int(height)))
                    points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
                    points.append((0, SCREEN_HEIGHT))
                    pygame.draw.polygon(self.screen, color, points)
                
                else:
                    # Nähere Details
                    points = []
                    for px in range(0, SCREEN_WIDTH + 30, 30):
                        height = 50 + math.sin((px + x) * 0.02) * 30
                        points.append((px, SCREEN_HEIGHT - int(height)))
                    points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
                    points.append((0, SCREEN_HEIGHT))
                    pygame.draw.polygon(self.screen, color, points)
    
    def _draw_ui(self) -> None:
        """Zeichnet die Benutzeroberfläche"""
        # Gesundheitsanzeige (Herzen)
        heart_size = 24
        padding = 10
        
        for i in range(self.player.max_health):
            x = padding + i * (heart_size + 5)
            y = padding
            
            if i < self.player.health:
                # Gefülltes Herz
                pygame.draw.rect(self.screen, COLORS['heart'], 
                               (x + 6, y + 4, 12, 16))
                pygame.draw.rect(self.screen, COLORS['heart'],
                               (x + 2, y + 8, 20, 12))
            else:
                # Leeres Herz (nur Rand)
                pygame.draw.rect(self.screen, COLORS['ui_muted'],
                               (x + 6, y + 4, 12, 16), 2)
                pygame.draw.rect(self.screen, COLORS['ui_muted'],
                               (x + 2, y + 8, 20, 12), 2)
        
        # Punktestand
        score_text = f"SCORE: {str(self.score).zfill(6)}"
        score_surface = self.font_medium.render(score_text, True, COLORS['ui_accent'])
        self.screen.blit(score_surface, (SCREEN_WIDTH - score_surface.get_width() - 10, 10))
        
        # Steuerungshinweis
        hint_text = "← → : Bewegen | SPACE : Sprung | F : Schießen | ESC : Pause"
        hint_surface = self.font_small.render(hint_text, True, COLORS['ui_muted'])
        self.screen.blit(hint_surface, (10, SCREEN_HEIGHT - 20))
    
    def _draw_menu(self) -> None:
        """Zeichnet das Hauptmenü"""
        # Halbtransparenter Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((15, 23, 42))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Titel
        title = self.font_large.render("PIXEL JUMP", True, COLORS['player'])
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 80))
        
        subtitle = self.font_medium.render("ADVENTURE", True, COLORS['platform_light'])
        self.screen.blit(subtitle, (center_x - subtitle.get_width() // 2, center_y - 40))
        
        # Start-Button
        btn_rect = draw_button(self.screen, "START GAME", center_x, center_y + 20)
        
        # Anleitung
        hint1 = self.font_small.render("Sammle alle Münzen und Edelsteine!", True, COLORS['ui_muted'])
        self.screen.blit(hint1, (center_x - hint1.get_width() // 2, center_y + 100))
        
        hint2 = self.font_small.render("Vermeide die roten Gegner oder schieße sie!", True, COLORS['ui_muted'])
        self.screen.blit(hint2, (center_x - hint2.get_width() // 2, center_y + 120))
    
    def _draw_pause_menu(self) -> None:
        """Zeichnet das Pause-Menü"""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((15, 23, 42))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Titel
        title = self.font_large.render("PAUSE", True, COLORS['ui_accent'])
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 40))
        
        # Buttons
        draw_button(self.screen, "WEITER", center_x, center_y + 20)
        draw_button(self.screen, "NEU STARTEN", center_x, center_y + 80)
    
    def _draw_game_over(self) -> None:
        """Zeichnet den Game Over Bildschirm"""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((15, 23, 42))
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0, 0))
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Titel
        title = self.font_large.render("GAME OVER", True, COLORS['ui_danger'])
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 60))
        
        # Score
        score_text = f"SCORE: {self.score}"
        score_surface = self.font_medium.render(score_text, True, COLORS['ui_accent'])
        self.screen.blit(score_surface, (center_x - score_surface.get_width() // 2, center_y - 10))
        
        # Button
        draw_button(self.screen, "NOCHMAL SPIELEN", center_x, center_y + 50)
    
    def _draw_victory(self) -> None:
        """Zeichnet den Victory Bildschirm"""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((15, 23, 42))
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0, 0))
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Titel
        title = self.font_large.render("GEWONNEN!", True, COLORS['player'])
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 60))
        
        # Score
        score_text = f"FINAL SCORE: {self.score}"
        score_surface = self.font_medium.render(score_text, True, COLORS['ui_accent'])
        self.screen.blit(score_surface, (center_x - score_surface.get_width() // 2, center_y - 10))
        
        # Button
        draw_button(self.screen, "NOCHMAL SPIELEN", center_x, center_y + 50)
    
    def run(self) -> None:
        """Haupt-Spiel-Loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


# Einstiegspunkt
if __name__ == "__main__":
    game = GameEngine()
    game.run()
