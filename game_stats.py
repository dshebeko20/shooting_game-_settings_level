class GameStats:
    """Отслеживает статистику для игры"""
    def __init__(self, sg_game):
        """Инициализирут статистику."""
        self.settings = sg_game.settings
        self.reset_stats()
        
        # Рекорд не должен сбрасываться
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.rockeet_left = self.settings.rocket_limit
        self.score = 0
        self.level = 1