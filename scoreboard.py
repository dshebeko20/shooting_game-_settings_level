import pygame.font
from pygame.sprite import Group

from rocket import Rocket

class Scoreboard:
    """Класс для вывода игровой информации."""
    
    def __init__(self, sg_game):
        """Инициализирует атрибуты подсчёта очков."""
        self.sg_game = sg_game
        self.screen = sg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sg_game.settings
        self.stats = sg_game.stats

        # Настройки шрифта для вывода счёта.
        self.text_color = (102, 102, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    def prep_images(self):
        """Подготавливает изображение счетов."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_rockets()

    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Вывод счёта в правой части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счёт в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"Record: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Рекорд выравнивается ближе к правой стороне экрана.
        self.hight_score_rect = self.high_score_image.get_rect()
        self.hight_score_rect.right = self.score_rect.right
        self.hight_score_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = f"Level: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
        
        # Уровень выводится под текущим счётом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.hight_score_rect.bottom + 10

    def prep_rockets(self):
        """Сообщает количество оставшихся кораблей."""
        self.rockets = Group()
        for rocket_number in range(self.stats.rocket_left):
            rocket = Rocket(self.sg_game)
            rocket.rect.x = 10 + rocket_number * rocket.rect.width
            rocket.rect.y = 10
            self.rockets.add(rocket)

    def show_score(self):
        """Выводит счета, уровень и количество ракет на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.hight_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.rockets.draw(self.screen)