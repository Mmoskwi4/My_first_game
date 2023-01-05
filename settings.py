class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 200, 250)
        self.stop_bg_color = (55, 55, 55)

        # Настройка корабля
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройка пришельцев
        self.fleet_drop_speed = 70

        # Темп ускорения игры
        self.speedup_scale = 1.2
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Настройка улучшений
        self.upgrade_drop_speed = 0.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 0.3
        self.bullet_speed = 1
        self.alien_speed = 0.2

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 20

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # Ограничение скорости
        if self.ship_speed > 2.5:
            self.ship_speed = 2.5
        if self.alien_speed > 2.5:
            self.alien_speed = 2.5
        if self.bullet_speed > 3.0:
            self.bullet_speed = 3.0

        self.alien_points = int(self.alien_points * self.score_scale)