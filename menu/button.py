import pygame
from menu.text import Text

class Button:
    def __init__(self, x, y, width, height, color_light, color_dark, text, font, text_color, screen):
        if x < 0:
            self.x = (screen.get_width() - width) / 2
        else:
            self.x = x
        if y < 0:
            self.y = (screen.get_height() - height) / 2
        else:
            self.y = y

        self.width = width
        self.height = height

        self.color_light = color_light
        self.color_dark = color_dark
        self.text_color = text_color

        self.font = font

        self.screen = screen

        self.update_text(text)

    def draw(self, mouse_pos):
        if self.check_mouse_pos(mouse_pos):
            pygame.draw.rect(self.screen, self.color_light, [self.x, self.y, self.width, self.height])
        else:
            pygame.draw.rect(self.screen, self.color_dark, [self.x, self.y, self.width, self.height])

        self.text.update()

    def check_mouse_pos(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def update_text(self, text):
        self.render = self.font.render(text, True, self.text_color)
        self.text = Text(self.x + (self.width - self.render.get_width()) / 2, self.y + (self.height - self.render.get_height()) / 2, text, self.font, self.text_color, self.screen)