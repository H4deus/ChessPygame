import pygame
from menu.text import Text
from menu.button import Button

class PopUp:
    def __init__(self, text, font, button1_text, button2_text, button_color_light, button_color_dark, text_color, background_color, width, height, screen):
        self.text = Text(-1, (screen.get_height() - height - 50) / 2 + 5, text, font, text_color, screen)
        self.button1 = Button((screen.get_width() - width + width / 2 - (width / 2 - 10)) / 2, -1, width / 2 - 10, 50, button_color_light, button_color_dark, button1_text, font, text_color, screen)
        self.button2 = Button((screen.get_width() + width - width / 2 - (width / 2 - 10)) / 2, -1, width / 2 - 10, 50, button_color_light, button_color_dark, button2_text, font, text_color, screen)

        self.background_color = background_color
        self.width = width
        self.height = height

    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, self.background_color, ((screen.get_width() - self.width) / 2, (screen.get_height() - self.height) / 2 - 50, self.width, self.height))
        self.text.update()
        self.button1.draw(mouse_pos)
        self.button2.draw(mouse_pos)
