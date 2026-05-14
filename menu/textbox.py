import pygame
from menu.text import Text

class TextBox:
    def __init__(self, x, y, width, height, color_active, color_inactive, font, text_color, screen):
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

        self.font = font
        self.text_color = text_color
        self.screen = screen

        self.active = False

        self.color_active = color_active
        self.color_inactive = color_inactive
        self.string = ""

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.color_active, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.color_inactive, (self.x, self.y, self.width, self.height))

        self.text = Text(self.x, self.y + (self.height - self.font.render(self.string, True, self.text_color).get_height()) / 2, self.string, self.font, self.text_color, self.screen)
        self.text.update()

    def check_mouse_pos(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def update_text(self, char, key):
        if key == pygame.K_BACKSPACE:
            self.string = self.string[:-1]
        elif self.text.get_width() > self.width - 20:
            return
        else:
            self.string += char