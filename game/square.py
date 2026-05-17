import pygame

class Square:
    def __init__(self, num_of_rows, screen, size, index, value, y_offset):
        # Finding the coordinates
        x = index % num_of_rows * size
        y = index // num_of_rows * size + y_offset

        # Getting the color

        if index % 2 == 0 and index // num_of_rows % 2 == 1 or index % 2 == 1 and index // num_of_rows % 2 == 0:
            if value // 100 == 1:
                color = (225, 124, 0)
            elif value % 10 == 1:
                color = (143, 186, 200)
            elif value >= 20:
                color = (220, 97, 97)
            elif value >= 10:
                color = (225, 202, 111)
            else:
                color = (118, 118, 118)
        else:
            if value // 100 == 1:
                color = (255, 154, 0)
            elif value % 10 == 1:
                color = (173, 216, 230)
            elif value >= 20:
                color = (250, 127, 127)
            elif value >= 10:
                color = (255, 232, 141)
            else:
                color = (255, 255, 255)

        # Actually drawing the square
        pygame.draw.rect(screen, color, (x, y, size, size))
