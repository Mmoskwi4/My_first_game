import pygame
from pygame.sprite import Sprite

class Donat(Sprite):
    """Класс представляющий один пончик"""
    def __init__(self, ai_game):
        """Инициализирует пончик и задает его наальную позицию"""
        super().__init__()
        self.screen = ai_game.screen

        # Загрузка оизображение пончика и назначение атрибута rect
        self.image = pygame.image.load('images/donat.bmp')
        self.image2 = self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # Каждый новый пончик появится в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пончика
        self.x = float(self.rect.x)