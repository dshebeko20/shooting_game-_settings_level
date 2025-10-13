import sys
from random import random

import pygame

from settings import Settings
from game_stats import GameStats
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
        pygame.display.set_caption("Shooting Game")

        # Создание экземпляра для хранениия игровой статистики.
        self.stats = GameStats(self)

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # Игра запускается в неактивном состоянии.
        self.game_active = False

        # создание кнопки Play.
        self.play_button = Button(self, "Play")

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

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
    
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
        # Срос иигровой статистики. 
        self.stats.reset_stats()
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
        """Обрабатывает столскновение ракеты с пришельцем."""
        if self.stats.rockeet_left > 0:
            # Уменьшение rocket_left.
            self.stats.rockeet_left -= 1

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

        # Кнопка Play отображаетсяя в том случае, если игра неактивна.
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    sg = ShootingGame()
    sg.run_game()