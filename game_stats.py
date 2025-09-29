class GameStats:
    """Отслеживает статистику для игры"""
    def __init__(self, sg_game):
        """Инициализирут статистику."""
        self.settings = sg_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Инициализирует сттистику, изменяющуюся в ходе игры."""
        self.rockeet_left = self.settings.rocket_limit