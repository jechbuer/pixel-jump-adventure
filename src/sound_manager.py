"""
Sound Manager für Pixel Jump Adventure
Sound-Effekte und Musik im Stil von Hans Zimmer
"""

import pygame
import math
import random
import numpy as np
from typing import Optional, Dict
from constants import COLORS


class SoundManager:
    """
    Verwaltet alle Sound-Effekte und Musik
    Erzeugt prozedurale Sounds im Hans Zimmer Stil
    """
    
    def __init__(self):
        """Initialisiert den Sound Manager"""
        # Pygame Mixer initialisieren
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        # Lautstärke-Einstellungen
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.5
        
        # Sound-Cache
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_playing = False
        self.current_music = None
        
        # Sound-Effekte generieren
        self._generate_sounds()
        
        # Musik initialisieren
        self._init_music()
    
    def _generate_sounds(self):
        """Generiert alle Sound-Effekte prozedural"""
        print("🎵 Generiere Sound-Effekte...")
        
        # Sprung-Sound (epischer Whoosh)
        self.sounds['jump'] = self._create_jump_sound()
        
        # Schuss-Sound (laser-artig)
        self.sounds['shoot'] = self._create_shoot_sound()
        
        # Münze einsammeln (glitzernd)
        self.sounds['coin'] = self._create_coin_sound()
        
        # Edelstein einsammeln (höher, wertvoller)
        self.sounds['gem'] = self._create_gem_sound()
        
        # Explosion (tief, episch)
        self.sounds['explosion'] = self._create_explosion_sound()
        
        # Schaden nehmen (dissonant)
        self.sounds['hurt'] = self._create_hurt_sound()
        
        # Landen (dumpf)
        self.sounds['land'] = self._create_land_sound()
        
        # Schritt-Sound
        self.sounds['step'] = self._create_step_sound()
        
        # Menü-Select
        self.sounds['select'] = self._create_select_sound()
        
        # Victory (triumphal)
        self.sounds['victory'] = self._create_victory_sound()
        
        # Game Over (düster)
        self.sounds['gameover'] = self._create_gameover_sound()
        
        print("✅ Sound-Effekte bereit!")
    
    def _create_jump_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen epischen Sprung-Sound (Hans Zimmer Style)"""
        sample_rate = 44100
        duration = 0.3
        samples = int(sample_rate * duration)
        
        # Buffer erstellen
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # Frequenz-Sweep (tief zu hoch)
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Hauptfrequenz: steigender Sweep
            freq = 150 + (800 * progress)
            
            # Sinus-Wellen mit Obertönen
            value = 0.6 * math.sin(2 * math.pi * freq * t)
            value += 0.3 * math.sin(2 * math.pi * freq * 2 * t)
            value += 0.1 * math.sin(2 * math.pi * freq * 3 * t)
            
            # Hüllkurve (Attack-Decay)
            envelope = 1.0 - progress
            envelope = envelope ** 0.5
            
            # Stereo mit leichtem Chorus
            left = int(value * envelope * 8000)
            right = int(value * envelope * 8000 * (0.95 + 0.05 * math.sin(t * 10)))
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_shoot_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen Laser-Schuss-Sound"""
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Schneller Frequenzabfall
            freq = 2000 - (1800 * progress)
            
            # Sägezahn-Welle für Laser-Effekt
            value = 0.7 * (2 * (t * freq - math.floor(t * freq + 0.5)))
            value += 0.3 * math.sin(2 * math.pi * freq * t)
            
            # Exponentielle Hüllkurve
            envelope = math.exp(-5 * progress)
            
            left = int(value * envelope * 6000)
            right = int(value * envelope * 6000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_coin_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen glitzernden Münz-Sound"""
        sample_rate = 44100
        duration = 0.2
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Hohe, helle Frequenz
            freq = 1200
            
            # Mehrere Obertöne für Glitzern
            value = 0.5 * math.sin(2 * math.pi * freq * t)
            value += 0.3 * math.sin(2 * math.pi * freq * 1.5 * t)
            value += 0.2 * math.sin(2 * math.pi * freq * 2 * t)
            
            # Schnelle Hüllkurve
            envelope = math.exp(-10 * progress)
            
            left = int(value * envelope * 7000)
            right = int(value * envelope * 7000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_gem_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen wertvollen Edelstein-Sound"""
        sample_rate = 44100
        duration = 0.4
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Noch höhere Frequenz
            freq = 1800
            
            # Komplexer Klang
            value = 0.4 * math.sin(2 * math.pi * freq * t)
            value += 0.3 * math.sin(2 * math.pi * freq * 1.25 * t)
            value += 0.2 * math.sin(2 * math.pi * freq * 1.5 * t)
            value += 0.1 * math.sin(2 * math.pi * freq * 2 * t)
            
            # Längere Hüllkurve
            envelope = math.exp(-5 * progress)
            
            left = int(value * envelope * 8000)
            right = int(value * envelope * 8000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_explosion_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen epischen Explosions-Sound (Hans Zimmer Style)"""
        sample_rate = 44100
        duration = 0.5
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Weißes Rauschen mit Filter
            noise = random.uniform(-1, 1)
            
            # Tiefe Frequenz für Impact
            freq = 80
            sub = 0.5 * math.sin(2 * math.pi * freq * t)
            
            # Kombination
            value = 0.6 * noise + 0.4 * sub
            
            # Lange Hüllkurve mit Sustain
            if progress < 0.1:
                envelope = progress / 0.1  # Attack
            else:
                envelope = math.exp(-3 * (progress - 0.1))
            
            left = int(value * envelope * 10000)
            right = int(value * envelope * 10000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_hurt_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen Schaden-Sound"""
        sample_rate = 44100
        duration = 0.3
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Dissonante Frequenzen
            freq1 = 300
            freq2 = 315  # Leicht verstimmt für Dissonanz
            
            value = 0.5 * math.sin(2 * math.pi * freq1 * t)
            value += 0.5 * math.sin(2 * math.pi * freq2 * t)
            
            # Hüllkurve
            envelope = math.exp(-8 * progress)
            
            left = int(value * envelope * 8000)
            right = int(value * envelope * 8000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_land_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen Lande-Sound"""
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Tiefer Thump
            freq = 100 - (50 * progress)
            
            value = math.sin(2 * math.pi * freq * t)
            
            # Sehr kurze Hüllkurve
            envelope = math.exp(-15 * progress)
            
            left = int(value * envelope * 6000)
            right = int(value * envelope * 6000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_step_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen Schritt-Sound"""
        sample_rate = 44100
        duration = 0.08
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            # Kurzes Rauschen
            noise = random.uniform(-0.5, 0.5)
            
            # Tiefer Thump
            thump = 0.3 * math.sin(2 * math.pi * 80 * t)
            
            value = noise + thump
            
            envelope = math.exp(-20 * progress)
            
            left = int(value * envelope * 4000)
            right = int(value * envelope * 4000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_select_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen Menü-Select-Sound"""
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            freq = 600
            value = math.sin(2 * math.pi * freq * t)
            
            envelope = math.exp(-10 * progress)
            
            left = int(value * envelope * 5000)
            right = int(value * envelope * 5000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_victory_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen triumphalen Victory-Sound (Hans Zimmer Style)"""
        sample_rate = 44100
        duration = 2.0
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # Akkord-Frequenzen (C-Dur: C-E-G-C)
        freqs = [261.63, 329.63, 392.00, 523.25]
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            value = 0
            for j, freq in enumerate(freqs):
                # Leichte Verstimmung für Choruseffekt
                detune = 1 + (j * 0.001)
                value += (0.25 / len(freqs)) * math.sin(2 * math.pi * freq * detune * t)
            
            # Crescendo-Hüllkurve
            if progress < 0.3:
                envelope = progress / 0.3
            elif progress < 0.7:
                envelope = 1.0
            else:
                envelope = 1.0 - ((progress - 0.7) / 0.3)
            
            left = int(value * envelope * 8000)
            right = int(value * envelope * 8000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_gameover_sound(self) -> pygame.mixer.Sound:
        """Erstellt einen düsteren Game Over-Sound"""
        sample_rate = 44100
        duration = 1.5
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # Dissonanter Akkord
        freqs = [220.00, 233.08, 277.18]  # A - A# - C#
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            value = 0
            for freq in freqs:
                value += (0.33) * math.sin(2 * math.pi * freq * t)
            
            # Abnehmende Hüllkurve
            envelope = math.exp(-2 * progress)
            
            left = int(value * envelope * 7000)
            right = int(value * envelope * 7000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _init_music(self):
        """Initialisiert die Hintergrundmusik"""
        # Musik wird prozedural generiert
        self.music_tracks = {
            'menu': self._create_menu_music(),
            'game': self._create_game_music(),
            'boss': self._create_boss_music(),
            'victory': self._create_victory_music()
        }
    
    def _create_menu_music(self) -> pygame.mixer.Sound:
        """Erstellt epische Menü-Musik (Hans Zimmer Style)"""
        sample_rate = 44100
        duration = 8.0  # 8 Sekunden Loop
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # Epic Bass-Line (wie Inception: BRAAM)
        bass_freq = 55  # A1
        
        # Pad-Akkord
        pad_freqs = [110, 138.59, 164.81, 220]  # A2, C#3, E3, A3
        
        for i in range(samples):
            t = i / sample_rate
            progress = (i % (sample_rate * 2)) / (sample_rate * 2)  # 2-Sekunden-Loop
            
            # Epic Bass (langsamer Attack)
            bass = 0
            if progress < 0.5:
                # Crescendo
                attack = progress / 0.5
                bass = 0.6 * attack * math.sin(2 * math.pi * bass_freq * t)
            else:
                # Sustain
                bass = 0.6 * math.sin(2 * math.pi * bass_freq * t)
            
            # Pad (stimmungsvoll)
            pad = 0
            for freq in pad_freqs:
                pad += 0.1 * math.sin(2 * math.pi * freq * t)
            
            # Arpeggio (hoch)
            arp_note = int(t * 2) % 4
            arp_freqs = [440, 554.37, 659.25, 880]
            arp = 0.05 * math.sin(2 * math.pi * arp_freqs[arp_note] * t)
            
            # Kombinieren
            value = bass + pad + arp
            
            # Master-Lautstärke
            value *= 0.7
            
            left = int(value * 6000)
            right = int(value * 6000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_game_music(self) -> pygame.mixer.Sound:
        """Erstellt dynamische Spiel-Musik"""
        sample_rate = 44100
        duration = 16.0  # 16 Sekunden Loop
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # Treibende Bass-Line
        bass_notes = [65.41, 65.41, 73.42, 73.42, 55.00, 55.00, 61.74, 61.74]  # C2, D2, A1, B1
        
        for i in range(samples):
            t = i / sample_rate
            beat = int(t * 4) % 32  # 8 beats
            
            # Bass
            bass_freq = bass_notes[beat // 4]
            bass = 0.4 * math.sin(2 * math.pi * bass_freq * t)
            
            # Kick-Drum auf jedem Beat
            kick = 0
            if beat % 4 == 0:
                kick_phase = (t * 4) % 1
                kick = 0.5 * math.sin(2 * math.pi * 60 * kick_phase) * math.exp(-5 * kick_phase)
            
            # Hi-Hat auf Off-Beats
            hihat = 0
            if beat % 2 == 1:
                hihat_phase = (t * 4) % 1
                noise = random.uniform(-0.3, 0.3)
                hihat = noise * math.exp(-10 * hihat_phase)
            
            # Melodische Linie
            melody_notes = [523.25, 587.33, 659.25, 698.46, 783.99, 698.46, 659.25, 587.33]
            melody_freq = melody_notes[beat % 8]
            melody = 0.15 * math.sin(2 * math.pi * melody_freq * t)
            
            # Kombinieren
            value = bass + kick + hihat + melody
            value *= 0.6
            
            left = int(value * 6000)
            right = int(value * 6000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_boss_music(self) -> pygame.mixer.Sound:
        """Erstellt intensive Boss-Musik"""
        sample_rate = 44100
        duration = 8.0
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        for i in range(samples):
            t = i / sample_rate
            beat = int(t * 8) % 64
            
            # Schneller, aggressiver Bass
            bass_freq = 41.20 if beat % 8 < 4 else 43.65  # E1, F1
            bass = 0.5 * math.sin(2 * math.pi * bass_freq * t)
            
            # Dissonante Stimmung
            dissonance = 0.3 * math.sin(2 * math.pi * 100 * t) * math.sin(2 * math.pi * 103 * t)
            
            # Kombinieren
            value = bass + dissonance
            value *= 0.7
            
            left = int(value * 6000)
            right = int(value * 6000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    def _create_victory_music(self) -> pygame.mixer.Sound:
        """Erstellt triumphale Victory-Musik"""
        sample_rate = 44100
        duration = 6.0
        samples = int(sample_rate * duration)
        
        buffer = np.zeros((samples, 2), dtype=np.int16)
        
        # C-Dur Akkord
        chord = [261.63, 329.63, 392.00, 523.25, 659.25]
        
        for i in range(samples):
            t = i / sample_rate
            progress = i / samples
            
            value = 0
            for freq in chord:
                value += 0.2 * math.sin(2 * math.pi * freq * t)
            
            # Crescendo
            envelope = min(1.0, progress * 2)
            if progress > 0.8:
                envelope *= (1 - progress) / 0.2
            
            left = int(value * envelope * 7000)
            right = int(value * envelope * 7000)
            
            buffer[i][0] = left
            buffer[i][1] = right
        
        return pygame.mixer.Sound(buffer=buffer)
    
    # === ÖFFENTLICHE METHODEN ===
    
    def play_sound(self, sound_name: str):
        """Spielt einen Sound-Effekt ab"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sfx_volume * self.master_volume)
            sound.play()
    
    def play_music(self, track_name: str, loops: int = -1):
        """Spielt Hintergrundmusik ab"""
        if track_name in self.music_tracks:
            # Stoppe aktuelle Musik
            self.stop_music()
            
            # Spiele neue Musik
            music = self.music_tracks[track_name]
            music.set_volume(self.music_volume * self.master_volume)
            music.play(loops)
            
            self.current_music = track_name
            self.music_playing = True
    
    def stop_music(self):
        """Stoppt die Musik"""
        for track in self.music_tracks.values():
            track.stop()
        self.music_playing = False
    
    def pause_music(self):
        """Pausiert die Musik"""
        pygame.mixer.pause()
    
    def unpause_music(self):
        """Setzt die Musik fort"""
        pygame.mixer.unpause()
    
    def set_master_volume(self, volume: float):
        """Setzt die Master-Lautstärke"""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume: float):
        """Setzt die Sound-Effekt-Lautstärke"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume: float):
        """Setzt die Musik-Lautstärke"""
        self.music_volume = max(0.0, min(1.0, volume))
        # Aktualisiere aktuelle Musik
        if self.current_music and self.current_music in self.music_tracks:
            self.music_tracks[self.current_music].set_volume(
                self.music_volume * self.master_volume
            )
    
    def toggle_mute(self) -> bool:
        """Schaltet Stumm an/aus"""
        if self.master_volume > 0:
            self._previous_volume = self.master_volume
            self.master_volume = 0
            return True  # Jetzt stumm
        else:
            self.master_volume = getattr(self, '_previous_volume', 0.7)
            return False  # Jetzt nicht stumm
