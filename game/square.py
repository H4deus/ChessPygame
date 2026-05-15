import pygame

class Square:
    def __init__(self, num_of_rows, screen, size, index, value, y_offset):
        # Finding the coordinates
        x = index % num_of_rows * size
        y = index // num_of_rows * size + y_offset

        # Getting the color

        # Yellow
        if value % 10 == 1:
            color = (173, 216, 230)
        # Light blue
        elif value >= 10:
            color = (255, 232, 141)
        # Gray
        elif index % 2 == 0 and index // num_of_rows % 2 == 1 or index % 2 == 1 and index // num_of_rows % 2 == 0:
            color = (128, 128, 128)
        # White
        else:
            color = (255, 255, 255)

        # Actually drawing the square
        pygame.draw.rect(screen, color, (x, y, size, size))
