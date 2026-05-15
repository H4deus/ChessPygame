import pygame
from game.pieces.pawn import Pawn
from game.pieces.king import King
from game.pieces.queen import Queen
from game.pieces.rook import Rook
from game.pieces.knight import Knight
from game.pieces.bishop import Bishop
from game.square import Square
from game.bot import Bot
from time import sleep
import random

class Game:
    def __init__(self, program):
        # Getting the window info
        self.program = program
        self.screen = program.screen

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.y_offset = (self.height - self.width) / 2

        # Defining constants
        self.num_of_rows = 8
        self.num_of_squares = self.num_of_rows ** 2
        self.square_size = self.width / self.num_of_rows

        # Defining variables
        self.pieces = []
        self.squares = []

        self.bot = Bot(self)

    def reset(self, bot):
        # Resetting the variables
        self.selected_piece = None
        self.last_move = 0
        if not bot:
            self.flip = True
            if random.random() < 0.5:
                self.program.menu.swap_players()
        else:
            self.flip = False
            if random.random() < 0.5:
                self.white_is_player = True
            else:
                self.white_is_player = False
        self.whose_turn = True

        # Resetting the booleans
        self.end_of_game = False

        self.can_en_passant = False

        self.white_can_short_castle = True
        self.white_can_long_castle = True

        self.black_can_short_castle = True
        self.black_can_long_castle = True

        self.white_in_check = False
        self.black_in_check = False

        # Resetting the lists
        self.board = [14, 16, 15, 13, 12, 15, 16, 14, # 0 - Empty, 1 - Pawn, 2 - King, 3 - Queen, 4 - Rook, 5 - Bishop, 6 - Knight, +10 - Black, +100 - Selected
                      11, 11, 11, 11, 11, 11, 11, 11,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      1, 1, 1, 1, 1, 1, 1, 1,
                      4, 6, 5, 3, 2, 5, 6, 4]

        self.white_attacks = [0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0]

        self.black_attacks = [0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0,
                              0,0,0,0,0,0,0,0]

        # Resetting the pieces
        for piece in self.pieces:
            if piece is None:
                continue
            del piece
        self.pieces = []

        # Resetting the squares
        for square in self.squares:
            del square
        self.squares = []

    def process_mouse_click(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1] - self.y_offset
        if (self.flip and self.whose_turn) or (not self.flip and self.white_is_player):
            index = int(mouse_x // self.square_size + self.num_of_rows * (mouse_y // self.square_size))
        else:
            index = 63 - int(mouse_x // self.square_size + self.num_of_rows * (mouse_y // self.square_size))
        if 0 > index > len(self.board):
            return
        clicked_value = self.board[index]

        if self.selected_piece is None and clicked_value == 0:
            return

        # Moving the piece, taking others and castling
        if self.selected_piece is not None and clicked_value >= 100 and self.selected_piece.index != index:
            self.whose_turn = not self.whose_turn

            # Taking the piece if possible
            if self.board[index] % 100 != 0:
                self.pieces[index].capture()

            # En passant
            if self.selected_piece.value % 10 == 1:
                # En passant to the right
                if self.pieces[self.selected_piece.index + 1] is not None and self.selected_piece.color == self.pieces[self.selected_piece.index + 1].color:
                    pass

                elif self.can_en_passant and self.board[self.selected_piece.index + 1] % 10 == 1:
                    self.pieces[self.selected_piece.index + 1].capture()

                # En passant to the left
                elif self.pieces[self.selected_piece.index - 1] is not None and self.selected_piece.color == self.pieces[self.selected_piece.index - 1].color:
                    pass

                elif self.can_en_passant and self.board[self.selected_piece.index - 1] % 10 == 1:
                    self.pieces[self.selected_piece.index - 1].capture()

                # Checking if can en passant
                if abs(index - self.selected_piece.index) == 2 * self.num_of_rows:
                    self.can_en_passant = True
                else:
                    self.can_en_passant = False

            # Castling
            # Disallowing if any of the relevant pieces have moved
            if self.board[63] != 4 or self.board[60] != 2:
                self.white_can_short_castle = False

            if self.board[56] != 4 or self.board[60] != 2:
                self.white_can_long_castle = False

            if self.board[7] != 14 or self.board[4] != 12:
                self.black_can_short_castle = False

            if self.board[0] != 14 or self.board[4] != 12:
                self.black_can_long_castle = False

            # Moving the rook if the king castled
            if self.selected_piece.value % 10 == 2 and abs(self.selected_piece.index - index) == 2:
                # White
                if self.selected_piece.color == 0:
                    # Short castle
                    if self.selected_piece.index < index:
                        self.update_lists(self.selected_piece.index + 1, 63)
                    # Long castle
                    if self.selected_piece.index > index:
                        self.update_lists(self.selected_piece.index - 1, 56)
                # Black
                elif self.selected_piece.color == 1:
                    # Short castle
                    if self.selected_piece.index < index:
                        self.update_lists(self.selected_piece.index + 1, 7)
                    # Long castle
                    if self.selected_piece.index > index:
                        self.update_lists(self.selected_piece.index - 1, 0)

            # Swapping the elements of the lists
            self.deselect_all(True)
            self.update_lists(index, self.selected_piece.index)
            self.board[index], self.board[self.selected_piece.index] = (self.board[index] % 100) + 200, (self.board[self.selected_piece.index] % 100) + 200

            # Promoting the pawn into a queen
            if self.board[index] % 100 == 1 and index < self.num_of_rows:
                self.board[index] = 3
            elif self.board[index] % 100 == 11 and index >= self.num_of_squares - self.num_of_rows:
                self.board[index] = 13

            self.selected_piece = None
            self.deselect_all(False)
            self.program.update()
            self.black_attacks, self.white_attacks = self.reset_attacks(self.pieces, self.board)

            # Checking if white is in check
            if self.black_attacks[self.board.index(2)] != 0:
                self.white_in_check = True
            else:
                self.white_in_check = False

            # Checking if black is in check
            if self.white_attacks[self.board.index(12)] != 0:
                self.black_in_check = True
            else:
                self.black_in_check = False

            if self.check_win():
                if self.whose_turn:
                    self.program.menu.black_won = True
                else:
                    self.program.menu.white_won = True
            elif self.check_draw():
                self.program.menu.draw = True

            sleep(0.25)
            self.last_move = index
            self.bot.evaluate_pos(self.pieces, self.board)
            if self.flip:
                self.program.menu.swap_players()
            return

        # Deselecting the pieces
        if self.pieces[index] is None:
            self.deselect_all(False)
            self.program.update()
            return

        # Selecting the piece
        if self.whose_turn and self.pieces[index].color == 0:
            self.deselect_all(False)
            self.pieces[index].select()
            self.selected_piece = self.pieces[index]
            self.program.update()
        elif not self.whose_turn and self.pieces[index].color == 1:
            self.deselect_all(False)
            self.pieces[index].select()
            self.selected_piece = self.pieces[index]
            self.program.update()

    def swap_in_list(self, list, a, b):
        if a == b: return list
        if a > b: a, b = b, a
        return list[:a] + list[b:b+1] + list[a+1:b] + list[a:a+1] + list[b+1:]

    def update_lists(self, a, b):
        self.pieces = self.swap_in_list(self.pieces, a, b)
        self.board = self.swap_in_list(self.board, a, b)

    def check_win(self):
        if not self.white_in_check and not self.black_in_check:
            return False

        for piece in self.pieces:
            if piece is None or (piece.color == 0 and not self.white_in_check) or (piece.color == 1 and not self.black_in_check):
                continue
            piece.get_legal_moves(True, self.board)
            if (self.white_in_check and piece.color == 0 and len(piece.legal_moves) > 0) or (self.black_in_check and piece.color == 1 and len(piece.legal_moves) > 0):
                return False

        return True

    def check_draw(self):
        if self.white_in_check or self.black_in_check:
            return False

        white_stalemate = True
        black_stalemate = True

        for piece in self.pieces:
            if not white_stalemate and not black_stalemate:
                return False
            if piece is None:
                continue
            piece.get_legal_moves(True, self.board)
            if piece.color == 0 and len(piece.legal_moves) > 0:
                white_stalemate = False
            elif piece.color == 1 and len(piece.legal_moves) > 0:
                black_stalemate = False

        return True

    def update(self):
        # Deleting the pieces
        for piece in self.pieces:
            if piece is None:
                continue
            del piece
        self.pieces = []

        # Deleting the squares
        for square in self.squares:
            del square
        self.squares = []

        # Adding everything
        if (self.flip and self.whose_turn) or (not self.flip and self.white_is_player):
            for i, v in enumerate(self.board):
                piece = None
                square = Square(self.num_of_rows, self.screen, self.square_size, i, v, self.y_offset)
                self.squares.append(square)

                match v % 10:
                    case 1:
                        piece = Pawn(self, i, i, v, self.y_offset)
                    case 2:
                        piece = King(self, i, i, v, self.y_offset)
                    case 3:
                        piece = Queen(self, i, i, v, self.y_offset)
                    case 4:
                        piece = Rook(self, i, i, v, self.y_offset)
                    case 5:
                        piece = Bishop(self, i, i, v, self.y_offset)
                    case 6:
                        piece = Knight(self, i, i, v, self.y_offset)

                self.pieces.append(piece)
        else:
            for i, v in enumerate(self.board):
                piece = None
                square = Square(self.num_of_rows, self.screen, self.square_size, 63 - i, v, self.y_offset)
                self.squares.append(square)

                match v % 10:
                    case 1:
                        piece = Pawn(self, 63 - i, i, v, self.y_offset)
                    case 2:
                        piece = King(self, 63 - i, i, v, self.y_offset)
                    case 3:
                        piece = Queen(self, 63 - i, i, v, self.y_offset)
                    case 4:
                        piece = Rook(self, 63 - i, i, v, self.y_offset)
                    case 5:
                        piece = Bishop(self, 63 - i, i, v, self.y_offset)
                    case 6:
                        piece = Knight(self, 63 - i, i, v, self.y_offset)

                self.pieces.append(piece)

    def reset_attacks(self, pieces, board):
        white_attacks = []
        black_attacks = []

        for i in range(self.num_of_squares):
            white_attacks.append(0)
            black_attacks.append(0)

        for piece in pieces:
            if piece is None:
                continue
            piece.get_legal_moves(False, board)
            if piece.color == 0:
                for attack in piece.attacks:
                    white_attacks[attack] += 1

            elif piece.color == 1:
                for attack in piece.attacks:
                    black_attacks[attack] += 1

        return black_attacks, white_attacks

    def deselect_all(self, deselect_highlight):
        for i, v in enumerate(self.board):
            if v >= 200 and not deselect_highlight:
                continue
            self.board[i] = v % 100

    def quit(self, event):
        self.end_of_game = True
