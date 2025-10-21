class Settings:
    """Класс для хранения всех настроек игры "Shooting game"."""

    def __init__(self):
        """Инициализирует настойки игры."""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.margin = 95 # Отступ от верхнего края экрана.
        
        # Параметры снаряда.
        self.bullet_width = 12
        self.bullet_height = 3
        self.bullet_color = (146, 51, 169)

        # Темп усколения игры.
        self.speedup_scale = 1.1

        # Темп роста стоиости риишельца.
        self.score_scale = 1.5

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        if self.difficulty_level == 'easy':
            self.rocket_limit = 4
            self.bullets_allowed = 10
            self.rocket_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 1.0
            self.alien_frequency = 0.005 # Частота появления пришельцев.
            self.alien_points = 25
        elif self.difficulty_level == 'medium':
            self.rocket_limit = 3
            self.bullets_allowed = 8
            self.rocket_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 1.5
            self.alien_frequency = 0.010 # Частота появления пришельцев.
            self.alien_points = 50
        elif self.difficulty_level == 'difficult':
            self.rocket_limit = 2
            self.bullets_allowed = 6
            self.rocket_speed = 3
            self.bullet_speed = 6
            self.alien_speed = 2.0
            self.alien_frequency = 0.015 # Частота появления пришельцев.
            self.alien_points = 75

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.rocket_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, dif_settings):
        if dif_settings == 'easy':
            print('easy')
        elif dif_settings == 'medium':
            pass
        elif dif_settings == 'difficult':
            pass