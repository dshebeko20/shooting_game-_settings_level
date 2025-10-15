class Settings:
    """Класс для хранения всех настроек игры "Shooting game"."""

    def __init__(self):
        """Инициализирует настойки игры."""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки ракеты.
        self.rocket_limit = 3

        # Параметры снаряда.
        self.bullet_width = 12
        self.bullet_height = 3
        self.bullet_color = (146, 51, 169)
        self.bullets_allowed = 10

        # Настройки пришельцев.
        # Задаёт частоту появления пришельцев.
        self.alien_frequency = 0.008

        # Темп усколения игры.
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игрыю"""
        self.rocket_speed = 2.5
        self.bullet_speed = 3.5
        self.alien_speed = 1.0

    def increase_speed(self):
        """Увеличивает ннастройки скорости."""
        self.rocket_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale