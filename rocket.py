import pygame
from pygame.sprite import Sprite

class Rocket(Sprite):
    """Класс для управления ракетой."""
    
    def __init__(self, sg_game):
        """Инициализирует ракету и задаёт её начальную позицию."""
        super().__init__()
        self.screen = sg_game.screen
        self.settings = sg_game.settings
        self.screen_rect = sg_game.screen.get_rect()

        # Загружает иображение ракеты и поучает прямоугольник.
        self.image = pygame.image.load('images/rocket_small.png')
        self.rect = self.image.get_rect()

        # Каждая новая ракета появляется у левого края крана.
        self.rect.midleft = self.screen_rect.midleft

        # Сохранение вещественной координаты центра ракеты.
        self.y = float(self.rect.y)

        # Флаги перемещения, начинаем с неподвижнеой ракеты. 
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """Обновляет позицию ракеты с учетом флагов."""
        # Обновляется атрибут y, а не rect.
        if self.moving_up and self.rect.top > self.settings.margin:
            self.y -= self.settings.rocket_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.rocket_speed

        # Обновление атрибута rect на основании self.y
        self.rect.y = self.y

    def center_rocket(self):
        """Рамещает ракету в центре левой части экрана."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        """Рисует ракету в текущей позиции."""
        self.screen.blit(self.image, self.rect)