import pygame.font

class Button():

    def __init__(self, ai_game, msg):
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None,48)

        # Построение объекта rect кнопки и выравниевание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создаётся только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравниает текст пр центру"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center



    def draw_button(self):
        """Отображение пустой кнопки и вывод собщения"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Button_Dif():
    def __init__(self, ai_game):
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.easy = "Easy"
        self.normal = "Normal"
        self.expert = "Expert"

        # Назначение размеров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color_ea = (0, 255, 0)
        self.button_color_no = (0, 255, 0)
        self.button_color_ex = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None,48)

        # Создание кнопок
        self._start_set_easy()
        self._start_set_normal()
        self._start_set_expert()


    def _start_set_easy(self):
        """Преобразование текста и Построение объекта rect кнопки и выравниевание в левом нижнем углу экрана"""
        self.rect_easy = pygame.Rect(0, 0, self.width, self.height)
        self.rect_easy.bottomleft = self.screen_rect.bottomleft
        self.rect_easy.bottomleft = self.screen_rect.bottomleft
        self.ea_image = self.font.render(self.easy, True, self.text_color, self.button_color_ea)
        self.easy_image_rect_easy = self.ea_image.get_rect()
        self.easy_image_rect_easy.center = self.rect_easy.center

    def _start_set_normal(self):
        """Преобразование текста и Построение объекта rect кнопки и выравниевание в середине нижней части экрана"""
        self.rect_normal = pygame.Rect(0, 0, self.width, self.height)
        self.rect_normal.midbottom = self.screen_rect.midbottom
        self.rect_normal.midbottom = self.screen_rect.midbottom
        self.no_image = self.font.render(self.normal, True, self.text_color, self.button_color_no)
        self.normal_image_rect_normal = self.no_image.get_rect()
        self.normal_image_rect_normal.center = self.rect_normal.center

    def _start_set_expert(self):
        """Преобразование текста и Построение объекта rect кнопки и выравниевание в правом нижнем углу экрана"""
        self.rect_expert = pygame.Rect(0, 0, self.width, self.height)
        self.rect_expert.bottomright = self.screen_rect.bottomright
        self.rect_expert.bottomright = self.screen_rect.bottomright
        self.ex_image = self.font.render(self.expert, True, self.text_color, self.button_color_ex)
        self.expert_image_rect_expert = self.ex_image.get_rect()
        self.expert_image_rect_expert.center = self.rect_expert.center

    def draw_button(self):
        """Отображение пустой кнопки и вывод собщения"""
        self.screen.fill(self.button_color_ea, self.rect_easy)
        self.screen.blit(self.ea_image, self.easy_image_rect_easy)
        self.screen.fill(self.button_color_no, self.rect_normal)
        self.screen.blit(self.no_image, self.normal_image_rect_normal)
        self.screen.fill(self.button_color_ex, self.rect_expert)
        self.screen.blit(self.ex_image, self.expert_image_rect_expert)

    def show_score(self):
        # Вывод сложности на экран

        self.dif_easy = self.font.render(self.easy, True, (255, 255, 255), self.settings.stop_bg_color)
        self.dif_easy_rect = self.dif_easy.get_rect()
        self.dif_easy_rect.right = self.screen_rect.right - 30
        self.dif_easy_rect.top = 20
        self.dif_normal = self.font.render(self.normal, True, (0, 0, 255), self.settings.stop_bg_color)
        self.dif_normal_rect = self.dif_normal.get_rect()
        self.dif_normal_rect.right = self.screen_rect.right - 30
        self.dif_normal_rect.top = 20
        self.dif_expert = self.font.render(self.expert, True, (255, 0, 0), self.settings.stop_bg_color)
        self.dif_expert_rect = self.dif_expert.get_rect()
        self.dif_expert_rect.right = self.screen_rect.right - 30
        self.dif_expert_rect.top = 20

        # Вывод сложности на экран
        if self.settings.speedup_scale < 1.4:
            self.screen.blit(self.dif_easy, self.dif_easy_rect)
        elif self.settings.speedup_scale < 1.6:
            self.screen.blit(self.dif_normal, self.dif_normal_rect)
        elif self.settings.speedup_scale >= 1.6:
            self.screen.blit(self.dif_expert, self.dif_expert_rect)

