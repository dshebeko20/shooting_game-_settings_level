from random import randint

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, sg_game):
        """Инициализирует пришельца и создаёт его начаальную позицию."""
        super().__init__()
        self.screen = sg_game.screen
        self.settings = sg_game.settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/alien_ship.png')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в случайном порядке с правой 
        # стороны экрана.
        self.rect.left = self.screen.get_rect().right

        # Размещение пришельца на высоту экрана минус высота одного пришельца.
        margin = self.settings.margin  
        alien_top_max = self.settings.screen_height - self.rect.height 
        self.rect.top = randint(margin, alien_top_max)

        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)

    def update(self):
        """Обновляет горизонтальную позицию пришельца"""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x
