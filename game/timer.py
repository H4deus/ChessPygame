from datetime import datetime
from menu.text import Text
import pygame

class Timer:
    def __init__(self, x, y, font, text_color, screen):
        self.screen = screen

        self.time = 0
        self.last_time = datetime.now().second

        self.pause = True
        self.hide = True

        self.x = x
        self.y = y

        self.text = Text(x, y, "", font, text_color, screen)

    def set_time(self, time_in_seconds):
        self.time = time_in_seconds
        self.text.text = self.convert_time_to_string(time_in_seconds)

    def update(self):
        if self.hide:
            return

        pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, 100, 40))

        if self.last_time != datetime.now().second and not self.pause:
            print("changing the time")
            self.time -= 1

        self.text.text = self.convert_time_to_string(self.time)
        self.text.x = self.x + self.text.get_width() / 2

        self.last_time = datetime.now().second
        self.text.update()

    def convert_time_to_string(self, time_in_seconds):
        seconds = str(time_in_seconds % 60)
        minutes = str(time_in_seconds // 60)
        if len(seconds) < 2:
            seconds = "0" + str(seconds)
        return minutes + ":" + seconds

