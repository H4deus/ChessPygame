import pygame
from time import sleep
from game.game import Game
from menu.menu import Menu

class Program:
    def __init__(self):
        pygame.init()
        res = (1000, 1100)

        self.screen = pygame.display.set_mode(res)
        pygame.display.set_caption("Chess")
        pygame.display.set_icon(pygame.image.load('images/white-pawn.png'))

        self.game = Game(self)
        self.menu = Menu(self)

        self.game_running = False

    def main(self):
        while True:
            self.screen.fill((50, 50, 50))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_running:
                        self.game.process_mouse_click(pygame.mouse.get_pos())
                    self.menu.process_mouse_click(pygame.mouse.get_pos())
                elif ev.type == pygame.KEYDOWN:
                    self.menu.process_keyboard_clicks(ev.unicode, ev.key)

            self.update()

    def update(self):
        if self.game_running:
            self.game.update()
        self.menu.update(pygame.mouse.get_pos())

        pygame.display.update()