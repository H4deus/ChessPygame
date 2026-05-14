import pygame

class Text:
    def __init__(self, x, y, text, font, text_color, screen):
        if x < 0:
            self.x = screen.get_width() / 2 - font.render(text, True, text_color).get_width() / 2
        else:
            self.x = x
        if y < 0:
            self.y = screen.get_height() / 2 - font.render(text, True, text_color).get_height() / 2
        else:
            self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        self.screen = screen

    def update(self):
        self.screen.blit(self.font.render(self.text, True, self.text_color), (self.x, self.y))

    def get_width(self):
        return self.font.render(self.text, True, self.text_color).get_width()