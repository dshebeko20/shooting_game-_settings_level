import pygame.font

class Button:
    """Класс для создания нопок для игры."""

    def __init__(self, sg_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = sg_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.height = 200, 50
        self.button_color = (220, 20, 60)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Создание объекта rect кнопки и выравнивание по ценру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создаётся тольько один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                 self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отображаеет пустую кнопку и выводит сообщение."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)