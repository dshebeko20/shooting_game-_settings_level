import json

from pathlib import Path

class GameStats:
    """Отслеживает статистику для игры"""
    
    def __init__(self, sg_game):
        """Инициализирут статистику."""
        self.settings = sg_game.settings
        self.reset_stats()
        
        # Рекорд никогда не должен сбрасываться
        self.high_score = self.get_saved_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.rocket_left = self.settings.rocket_limit
        self.score = 0
        self.level = 1

    def get_saved_high_score(self):
        """Получает сохранённый рекорд из файла."""
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0