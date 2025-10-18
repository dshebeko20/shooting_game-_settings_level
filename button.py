import pygame.font

class Button:
    """Класс для создания нопок для игры."""

    def __init__(self, sg_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = sg_game.screen
        self.screen_rect = self.screen.get_rect()

        # Поддерживает базовый цвет и цвет выделения.
        self.base_color = (220, 20, 60)
        self.highlighted_color = (102, 102, 255)
        # Сохраним сообщение, чтобы вызвать _prep_msg()
        # изменив цвет кнопки.
        self.msg = msg

        # Назначение размеров и свойств кнопок.
        self.width, self.height = 200, 50
        self.button_color = self.base_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Создание объекта rect кнопки и выравнивание по ценру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки должно быть педварительно подготовлено.
        self._prep_msg()

    def _prep_msg(self):
        """Преобразует msg в прямоугольник и выравнивает текст по центру."""
        self.msg_image = self.font.render(self.msg, True, self.text_color, 
                 self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        """Перемещает текст вместе с кнопкой."""
        self.msg_image_rect.center = self.rect.center

    def set_highlighted_color(self):
        """Устанавливает выделенный цвет кнопки."""
        self.button_color = self.highlighted_color
        self._prep_msg()

    def set_base_color(self):
        """Устанавливает для кнопки основной цвет."""
        self.button_color = self.base_color
        self._prep_msg()

    def draw_button(self):
        """Отображаеет пустую кнопку и выводит сообщение."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)