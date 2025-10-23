import pygame 

from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными ракетой."""
    
    def __init__(self, sg_game):
        """Создаёт объект снарядов в текщей позиции ракеты."""
        super().__init__()
        self.screen = sg_game.screen
        self.settings = sg_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции (0, 0) и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
            self.settings.bullet_height)
        self.rect.midright = sg_game.rocket.rect.midright

        # Позиция снаряда хранится в вещественном формате.
        self.x = float(self.rect.x)

    def update(self):
        """Перемещаает снаряд вправо по экрану."""
        # Обновление точной позиции снаряда.
        self.x += self.settings.bullet_speed
        # Обновление позиции прямоугольника.
        self.rect.x = self.x

    def draw_bullet(self):
        """Выводит снаряд на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)