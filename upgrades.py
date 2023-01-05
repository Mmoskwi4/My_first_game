import pygame
from pygame.sprite import Sprite
from random import randint

class Upgrade(Sprite):
    """Класс улучшения корабля"""
    def __init__(self, ai_game):
        """Инициализирует улучшения в процессе игры"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.ship = ai_game.ship

        # Загружает изображение улучшения
        self.image = pygame.image.load('images/upgrade.bmp')
        self.image1 = self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = self.screen_rect.top

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = randint(0, (self.settings.screen_width - self.rect.width))
        self.y = -200

    def grade_1(self):
        """Выпускает снаряда, который проелтает насквозь"""
        self.ship.image = pygame.image.load('images/ship-1.bmp')

    def update(self):
        """Обновляет позицию улучшения"""
        self.y += self.settings.upgrade_drop_speed
        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        """Рисует улучшение"""
        self.screen.blit(self.image, self.rect)
