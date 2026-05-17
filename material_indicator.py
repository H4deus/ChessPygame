import pygame
from menu.text import Text

class MaterialIndicator:
    def __init__(self, color, text_color, font, x, y, screen):
        self.color = color
        self.x = x
        self.y = y

        self.screen = screen

        self.text = Text(self.x, self.y, "", font, text_color, screen)

    def update(self, captured_pieces, adv):
        offset = 0
        for piece in captured_pieces:
            match piece:
                case 1:
                    if self.color == 0:
                        img = pygame.image.load("images/black-pawn.png")
                    elif self.color == 1:
                        img = pygame.image.load("images/white-pawn.png")
                case 3:
                    if self.color == 0:
                        img = pygame.image.load("images/black-queen.png")
                    elif self.color == 1:
                        img = pygame.image.load("images/white-queen.png")
                case 4:
                    if self.color == 0:
                        img = pygame.image.load("images/black-rook.png")
                    elif self.color == 1:
                        img = pygame.image.load("images/white-rook.png")
                case 5:
                    if self.color == 0:
                        img = pygame.image.load("images/black-bishop.png")
                    elif self.color == 1:
                        img = pygame.image.load("images/white-bishop.png")
                case 6:
                    if self.color == 0:
                        img = pygame.image.load("images/black-knight.png")
                    elif self.color == 1:
                        img = pygame.image.load("images/white-knight.png")
                case _:
                    img = pygame.image.load("images/black-pawn.png")

            img = pygame.transform.scale(img, (40, 40))
            self.screen.blit(img, (self.x + offset, self.y))
            offset += img.get_width()

        if adv <= 0:
            return
        self.text.text = "+" + str(adv)
        self.text.x = self.x + offset
        self.text.update()
