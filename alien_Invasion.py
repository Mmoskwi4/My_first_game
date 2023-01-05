import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from button import Button_Dif
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from donat import Donat
from random import randint
from upgrades import Upgrade

class AlienInvasion():
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые процессы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Создание игровых моделей
        self.ship = Ship(self)
        self.upgrade = Upgrade(self)
        self.bullet = Bullet(self)
        self.alien = Alien(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.donats = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

        # Создание флота и неба
        self._create_fleet()
        self._donat_sky()

        # Создание кнопки
        self.play_button = Button(self, "Play")
        self.dif = Button_Dif(self)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
                # Отрисовка улучшений
                self.create_upgrade()
                self.upgrade.update()
                self._update_upgrades()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._change_dif(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                self._change_dif_res(mouse_pos)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.game_active = True
        elif event.key == pygame.K_ESCAPE:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _change_dif(self,mouse_pos):
        """Анимация переключения кнопки"""
        # Меняет цвет кнопки при нажатии
        set_dif_easy = self.dif.rect_easy.collidepoint(mouse_pos)
        if set_dif_easy and not self.stats.game_active:
            self.dif.button_color_ea = (0, 130, 0)
            self.dif._start_set_easy()

        set_dif_normal = self.dif.rect_normal.collidepoint(mouse_pos)
        if set_dif_normal and not self.stats.game_active:
            self.dif.button_color_no = (0, 130, 0)
            self.dif._start_set_normal()

        set_dif_expert = self.dif.rect_expert.collidepoint(mouse_pos)
        if set_dif_expert and not self.stats.game_active:
            self.dif.button_color_ex = (0, 130, 0)
            self.dif._start_set_expert()

    def _change_dif_res(self,mouse_pos):
        """Изменения сложности игры"""
        # Возвращает прежний цвет кнопки при отпускании кнопки и меняет сложность (коэффициент)
        set_dif_easy = self.dif.rect_easy.collidepoint(mouse_pos)
        if set_dif_easy and not self.stats.game_active:
            self.dif.button_color_ea = (0, 255, 0)
            self.settings.speedup_scale = 1.2
            self.settings.score_scale = 1.5
            self.dif._start_set_easy()

        set_dif_normal = self.dif.rect_normal.collidepoint(mouse_pos)
        if set_dif_normal and not self.stats.game_active:
            self.dif.button_color_no = (0, 255, 0)
            self.settings.speedup_scale = 1.4
            self.settings.score_scale = 2.0
            self.dif._start_set_normal()


        set_dif_expert = self.dif.rect_expert.collidepoint(mouse_pos)
        if set_dif_expert and not self.stats.game_active:
            self.dif.button_color_ex = (0, 255, 0)
            self.settings.speedup_scale = 1.6
            self.settings.score_scale = 2.5
            self.dif._start_set_expert()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        self._change_dif(mouse_pos)
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()


            # Отчистка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # оздание нового флота и размещение корабля в центра
            self._create_fleet()
            self.ship.centre_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и удаляет старые снаряды"""
        # Обновление позиции снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка колизий снарядов с пришельцами"""
        # Удаление снарядов и пришельцев, участвующих в колизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Создает флот пришельцев"""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (7 * alien_width) # 15 alien on _x = (2 * alien_width)

        """Определяет количество рядов, помещающихся на окране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        numbers_rows = available_space_y // (4 * alien_height)

        # Создание флота вторжения
        for row_number in range(numbers_rows):
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)

    def _create_aliens(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцами"""
        if self.stats.ships_left > 0:
            # Уменьшение ship_left -= 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Отчистка списков пришелцев и снарядов
            self.bullets.empty()
            self.aliens.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.centre_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        """Проверяет, коснулся ли пришелец нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что и при столкновении с кораблем
                self._ship_hit()
                break

    def _update_aliens(self):
        """Обновляет позиции пришельцев"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка колизии "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края жкрана
        self._check_alien_bottom()

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _donat_sky(self):
        """Создает пончиковое небо"""
        donat = Donat(self)
        donat_width, donat_height = donat.rect.size
        available_space_x = self.settings.screen_width + (10 * donat_width)
        number_donats_x = available_space_x // (10 * donat_width)

        """Определяет количество возможных рядов, помещяющихся на экране"""
        available_space_y = self.settings.screen_height + (10 * donat_width)
        numbers_rows = available_space_y // donat_height

        # Создание "звездного" неба
        for row_number in range(numbers_rows):
            for number_donat in range(number_donats_x):
                self._create_donats(number_donat, row_number, random_number=randint(-1, 1))

    def _create_donats(self, number_donat, row_number, random_number):
        donat = Donat(self)
        donat_width, donat_height = donat.rect.size
        donat.x = donat_width + 10 * donat_width * number_donat * random_number
        donat.rect.x = donat.x
        donat.rect.y = donat.rect.height + 10 * donat.rect.height * row_number * random_number
        if donat.rect.x < self.settings.screen_width:
            if donat.rect.y < self.settings.screen_height:
                self.donats.add(donat)

    def create_upgrade(self):
        """Создает улучшение на экране"""


    def _update_upgrades(self):
        """Обновляет позици на экране"""
        for upgrade in self.upgrades.copy():
            if upgrade.rect.bottom >= self.upgrade.screen_rect.bottom:
                self.settings.upgrade_drop_speed = 0

        self._check_ship_upgrade_collision()

    def _check_ship_upgrade_collision(self):
        """Проверяет колизию корабля с улучшением"""
        collections = pygame.sprite.spritecollide(self.ship, self.upgrades, True)
        if collections:
            self.upgrade.grade_1()

    def _update_screen(self):
        """Отображает изображение на экране и отображает новый экран"""
        # Отрисовка экрана
        self.screen.fill(self.settings.bg_color)
        # Отрисовка снарядов
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отрисовка неба
        self.donats.draw(self.screen)
        # Вывод информации о счете
        self.sb.show_score()

        for upgrade in self.upgrades.sprites():
            upgrade.blitme()

        # Отрисовка корабля
        self.ship.blitme()
        # Отрисовка пришельцев
        self.aliens.draw(self.screen)


        # Кнопка Play отображается в том случае, если игра не активна
        if not self.stats.game_active:
            self.screen.fill(self.settings.stop_bg_color)
            self.donats.draw(self.screen)
            self.play_button.draw_button()
            self.dif.draw_button()
            self.dif.show_score()

        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()