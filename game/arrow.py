import pygame
import math

class Arrow:
    def __init__(self, screen, index0, index1, num_of_rows, size, y_offset):
        self.screen = screen

        self.start_tile_x = index0 % num_of_rows * size + size / 2
        self.start_tile_y = index0 // num_of_rows * size + size / 2 + y_offset

        self.end_tile_x = index1 % num_of_rows * size + size / 2
        self.end_tile_y = index1 // num_of_rows * size + size / 2 + y_offset

        color = (255, 204, 50)

        knight_moves = [index0 - num_of_rows * 2 - 1, index0 - num_of_rows * 2 + 1,
                          index0 - num_of_rows - 2, index0 - num_of_rows + 2,
                          index0 + num_of_rows - 2, index0 + num_of_rows + 2,
                          index0 + num_of_rows * 2 - 1, index0 + num_of_rows * 2 + 1]

        if index1 in knight_moves:
            if knight_moves.index(index1) in (0,6):
                pygame.draw.polygon(self.screen, color, (self.rotate(self.end_tile_x - 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(270)),
                                                    self.rotate(self.end_tile_x + 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(270)),
                                                    self.rotate(self.end_tile_x, self.end_tile_y - 50, self.end_tile_x, self.end_tile_y, math.radians(270))))
            elif knight_moves.index(index1) in (1,7):
                pygame.draw.polygon(self.screen, color, (self.rotate(self.end_tile_x - 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(90)),
                                                    self.rotate(self.end_tile_x + 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(90)),
                                                    self.rotate(self.end_tile_x, self.end_tile_y - 50, self.end_tile_x, self.end_tile_y, math.radians(90))))
            elif knight_moves.index(index1) in (2,3):
                pygame.draw.polygon(self.screen, color, (self.rotate(self.end_tile_x - 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(0)),
                                                    self.rotate(self.end_tile_x + 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(0)),
                                                    self.rotate(self.end_tile_x, self.end_tile_y - 50, self.end_tile_x, self.end_tile_y, math.radians(0))))
            elif knight_moves.index(index1) in (4,5):
                pygame.draw.polygon(self.screen, color, (self.rotate(self.end_tile_x - 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(180)),
                                                    self.rotate(self.end_tile_x + 50, self.end_tile_y, self.end_tile_x, self.end_tile_y, math.radians(180)),
                                                    self.rotate(self.end_tile_x, self.end_tile_y - 50, self.end_tile_x, self.end_tile_y, math.radians(180))))

            if knight_moves.index(index1) in (0,1):
                pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y), (self.start_tile_x, self.start_tile_y - size * 2 - 25), 50)

            elif knight_moves.index(index1) in (3,5):
                pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y), (self.start_tile_x + size * 2 + 25, self.start_tile_y), 50)

            elif knight_moves.index(index1) in (6,7):
                pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y), (self.start_tile_x, self.start_tile_y + size * 2 + 25), 50)

            elif knight_moves.index(index1) in (2,4):
                pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y), (self.start_tile_x - size * 2 - 25, self.start_tile_y), 50)
            
            match knight_moves.index(index1):
                case 0:
                    pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y - size * 2), (self.start_tile_x - size, self.start_tile_y - size * 2), 50)
                
                case 1:
                    pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y - size * 2), (self.start_tile_x + size, self.start_tile_y - size * 2), 50)
                
                case 2:
                    pygame.draw.line(self.screen, color, (self.start_tile_x - size * 2, self.start_tile_y), (self.start_tile_x - size * 2, self.start_tile_y - size), 50)
                
                case 3:
                    pygame.draw.line(self.screen, color, (self.start_tile_x + size * 2, self.start_tile_y), (self.start_tile_x + size * 2, self.start_tile_y - size), 50)
                
                case 4:
                    pygame.draw.line(self.screen, color, (self.start_tile_x - size * 2, self.start_tile_y), (self.start_tile_x - size * 2, self.start_tile_y + size), 50)
                
                case 5:
                    pygame.draw.line(self.screen, color, (self.start_tile_x + size * 2, self.start_tile_y), (self.start_tile_x + size * 2, self.start_tile_y + size), 50)
                
                case 6:
                    pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y + size * 2), (self.start_tile_x - size, self.start_tile_y + size * 2), 50)
                
                case 7:
                    pygame.draw.line(self.screen, color, (self.start_tile_x, self.start_tile_y + size * 2), (self.start_tile_x + size, self.start_tile_y + size * 2), 50)

        else:
            pygame.draw.polygon(self.screen, color, (self.rotate(self.start_tile_x-25, self.start_tile_y, self.start_tile_x, self.start_tile_y),
                                                     self.rotate(self.end_tile_x-25, self.end_tile_y, self.end_tile_x, self.end_tile_y),
                                                     self.rotate(self.end_tile_x+25, self.end_tile_y, self.end_tile_x, self.end_tile_y),
                                                     self.rotate(self.start_tile_x+25, self.start_tile_y, self.start_tile_x, self.start_tile_y)), 0)

            pygame.draw.polygon(self.screen, color,(self.rotate(self.end_tile_x - 50, self.end_tile_y, self.end_tile_x, self.end_tile_y),
                                                        self.rotate(self.end_tile_x + 50, self.end_tile_y, self.end_tile_x, self.end_tile_y),
                                                        self.rotate(self.end_tile_x, self.end_tile_y - 50, self.end_tile_x, self.end_tile_y)), 0)

    def rotate(self, px, py, cx, cy, angle=-4.0):
        if angle <= -4:
            angle = math.atan2(self.end_tile_y - self.start_tile_y, self.end_tile_x - self.start_tile_x) + math.radians(90)
        return (cx + math.cos(angle) * (px - cx) - math.sin(angle) * (py - cy),
                cy + math.sin(angle) * (px - cx) + math.cos(angle) * (py - cy))




