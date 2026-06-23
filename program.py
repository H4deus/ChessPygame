import pygame
from game.game import Game
from menu.menu import Menu

class Program:
    def __init__(self):
        pygame.init()
        res = (1024, 1124)

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
                    if ev.button == 1:
                        if self.game_running:
                            self.game.process_mouse_click(pygame.mouse.get_pos())
                        self.menu.process_mouse_click(pygame.mouse.get_pos())
                    elif ev.button == 3:
                        if self.game_running:
                            self.game.process_right_mouse_click(pygame.mouse.get_pos(), True)
                elif ev.type == pygame.KEYDOWN:
                    self.menu.process_keyboard_clicks(ev.unicode, ev.key)
                elif ev.type == pygame.MOUSEBUTTONUP:
                    if ev.button == 3:
                        if self.game_running:
                            self.game.process_right_mouse_click(pygame.mouse.get_pos(), False)

            self.update()

    def update(self):
        self.menu.update(pygame.mouse.get_pos())
        if self.game_running:
            self.game.update()

        pygame.display.update()