import sys
from time import sleep
from random import random

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from rocket import Rocket
from bullet import Bullet
from alien import Alien

class ShootingGame:
    """Класс для управлением ресурсами и поведением игры."""
    
    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Shooting game")

        # Создание экземпляра для хранениия игровой статистики.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Инициализируем счётчик сбитых пришельцев.
        self.kill_count = 0
       
        # Игра запускается в неактивном состоянии.
        self.game_active = False

        # Создание кнопки Play.
        self.play_button = Button(self, "Play")

        # Coздание кнопок сложности.
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Создаёт кнопки повышения сложности уровня."""
        self.easy_button =  Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.difficult_button = Button(self, "Difficult")

        # Размещаем позиции кнопок.
        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.difficult_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.difficult_button._update_msg_position()

        # Устанавливаем для средней кнопки цвет, выделенный на изобоажении.
        self.medium_button.set_highlighted_color()

    def run_game(self):
        """Запукскает основной цикл игры."""
        while True:
            self._check_events()
            
            if self.game_active:
                self._create_alien()
                
                self.rocket.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Устанавливает подходящий уровень сложности."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        diff_button_clicked = self.difficult_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_base_color()
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.difficult_button.set_base_color()
        elif diff_button_clicked:
            self.settings.difficulty_level = 'difficult'
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_highlighted_color()

    def _check_keydown_events(self, event):
        """Реагирует на нажатия клавиш."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()
            
    def _check_keyup_events(self, event):
        """Реагирует на отпускания клавиш."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False

    def _start_game(self):
        """Начинает новую игру."""
        # Срос игровой статистики. 
        self.stats.reset_stats()
        self.sb.prep_images()
        self.game_active = True

        # Очистка групп aliens и bullets.
        self.bullets.empty()
        self.aliens.empty()

        # Создание нового флота и размещение ракеты в центре.
        self._create_alien()
        self.rocket.center_rocket()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Создаёт новый снаряд и добавляет его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
             new_bullet = Bullet(self)
             self.bullets.add(new_bullet)

    def _update_bullets(self): 
        """ Обнвляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()
            
        # Удаление снарядов, вышедших за кай экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right: 
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Обрабатывает коллизии снарядов с пришельцами."""
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
                self.kill_count += 1
            
            if self.kill_count >= 50:
                self._start_new_level()
                
    def _start_new_level(self):
        self.stats.level += 1 
        self.sb.prep_level()
        self.aliens.empty()
        self.kill_count = 0
        # Пауза
        sleep(0.5) 
        self.rocket.center_rocket()
        self._create_alien()
        self.settings.increase_speed()

    def _create_alien(self):
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)

    def _update_aliens(self):
        """Обновляет позиции пришельцев и проверяет столкновения."""
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.rocket, self.aliens):
            self._rocket_hit()

        # Проверить, сталкиваются ли пришельцы с левым краем экрана.
        self._check_aliens_left_edge()

    def _check_aliens_left_edge(self):
        """Проверяет, добрались ли пришельцы до левого края экрана."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Происходит то же, что и при столкновении с ракетой.
                self._rocket_hit()
                break

    def _rocket_hit(self):
        """Обрабатывает столкновение ракеты с пришельцем."""
        if self.stats.rocket_left > 1:
            # Уменьшение rocket_left и обновление панели счёта.
            self.stats.rocket_left -= 1
            self.sb.prep_rockets()

            # Очистка групп aliens и bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_alien()
            self.rocket.center_rocket()
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.rocket.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.aliens.draw(self.screen)

        # Вывод информации о счёте.
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.difficult_button.draw_button()
        
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    sg = ShootingGame()
    sg.run_game()