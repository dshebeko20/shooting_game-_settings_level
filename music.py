import pygame
from pygame.mixer import Sound

class Music(Sound):
    """Класс для управления музыкой."""

    def __init__(self, sh_game):
        """Инициализирует атибуты музыки."""
        self.ai_game = sh_game
        self.music_game = pygame.mixer.music.load('sound/osd.mp3')
        self.music_shoot = pygame.mixer.music.load('sound/FX061.mp3')
        self.music_exp =  pygame.mixer.music.load('sound/explosion.wav')
        
    def play_music_game(self):
        """Воспроизводит фоновую музыку."""
        self.music_game = pygame.mixer.Sound('sound/osd.mp3')
        self.music_game.play(-1)
    
    def play_music_shoot(self):
        """Воспроизводит звук выстрела."""
        self.music_shoot = pygame.mixer.Sound('sound/FX061.mp3')
        self.music_shoot.play()

    def play_music_exp(self):
        """Воспроизводит звук взрыва при столкновении с пришельцем."""
        self.music_exp = pygame.mixer.Sound('sound/explosion.wav')
        self.music_exp.play()

    def stop_music(self):
        """Останавливает звук воспроизведения."""
        self.music_game.stop()
        self.music_shoot.stop()
        self.music_exp.stop()


