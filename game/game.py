import pygame

from piece import Piece
from game.square import Square
from game.arrow import Arrow
from game.timer import Timer
# from game.bot import Bot
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

        self.font = pygame.font.SysFont("comicsans", 30)

        # self.bot = Bot(self)
        self.timer_top = Timer(600, 5, self.font, (255, 255, 255), self.screen)
        self.timer_bottom = Timer(600, self.screen.get_height() - 45, self.font, (255, 255, 255), self.screen)

    def reset(self, bot):
        # Resetting the variables
        self.selected_piece = None
        self.last_move = 0
        if not bot:
            self.flip = True
            if random.random() < 0.5:
                self.program.menu.swap_players()

            self.timer_top.hide = False
            self.timer_bottom.hide = False
            self.timer_top.set_time(300)
            self.timer_bottom.set_time(300)
            self.timer_top.pause = True
            self.timer_bottom.pause = True
        else:
            self.flip = False
            if random.random() < 0.5:
                self.white_is_player = True
            else:
                self.white_is_player = False

            self.timer_top.hide = True
            self.timer_bottom.hide = True
        self.whose_turn = True

        # Resetting the booleans
        self.end_of_game = False

        self.can_en_passant = False

        self.fifty_move_rule = 0

        self.white_can_short_castle = True
        self.white_can_long_castle = True

        self.black_can_short_castle = True
        self.black_can_long_castle = True

        self.white_in_check = False
        self.black_in_check = False

        self.highlight_index = -1

        # Resetting the lists
        self.board = [14, 16, 15, 13, 12, 15, 16, 14, # 0 - Empty, 1 - Pawn, 2 - King, 3 - Queen, 4 - Rook, 5 - Bishop, 6 - Knight, +10 - Black
                      11, 11, 11, 11, 11, 11, 11, 11,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      1, 1, 1, 1, 1, 1, 1, 1,
                      4, 6, 5, 3, 2, 5, 6, 4]

        self.white_attacks = [0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0]

        self.black_attacks = [0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0]

        self.highlights = [0, 0, 0, 0, 0, 0, 0, 0, # +1 - legal move, +10 - previous move
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0]

        self.arrows = []

        self.past_positions = []

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
        if 0 > index or index >= self.num_of_squares:
            return
        clicked_value = self.board[index]

        if self.selected_piece is None and clicked_value == 0:
            return

        # Moving the piece, taking others and castling
        if self.selected_piece is not None and self.highlights[index] % 10 == 1 and self.selected_piece.index != index:
            self.fifty_move_rule += 1
            self.whose_turn = not self.whose_turn
            self.timer_top.time, self.timer_bottom.time = self.timer_bottom.time, self.timer_top.time
            self.timer_top.pause = True
            self.timer_bottom.pause = False

            # Taking the piece if possible
            if self.board[index] != 0:
                self.fifty_move_rule = 0
                if self.board[index] in (1,4,5,6,11,14,15,16):
                    self.past_positions = []
                self.board[index] = 0
                del self.pieces[index]

            # En passant
            if self.selected_piece.value % 10 == 1:
                self.fifty_move_rule = 0
                # En passant to the right
                if self.pieces[self.selected_piece.index + 1] is not None and self.selected_piece.color == self.pieces[self.selected_piece.index + 1].color:
                    pass

                elif self.can_en_passant and self.board[self.selected_piece.index + 1] % 10 == 1 and index == self.selected_piece.index - 1 - self.num_of_rows:
                    self.board[self.selected_piece.index + 1] = 0
                    del self.pieces[self.selected_piece.index + 1]

                # En passant to the left
                elif self.pieces[self.selected_piece.index - 1] is not None and self.selected_piece.color == self.pieces[self.selected_piece.index - 1].color:
                    pass

                elif self.can_en_passant and self.board[self.selected_piece.index - 1] % 10 == 1 and index == self.selected_piece.index - 1 - self.num_of_rows:
                    self.board[self.selected_piece.index - 1] = 0
                    del self.pieces[self.selected_piece.index - 1]

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
            self.highlights[index], self.highlights[self.selected_piece.index] = 10, 10

            # Promoting the pawn into a queen
            if self.board[index] == 1 and index < self.num_of_rows:
                self.board[index] = 3
            elif self.board[index] == 11 and index >= self.num_of_squares - self.num_of_rows:
                self.board[index] = 13

            self.selected_piece = None
            self.deselect_all(False)
            self.program.update()
            self.black_attacks, self.white_attacks = self.reset_attacks(self.pieces, self.board)

            # Checking if white is in check
            if self.black_attacks[self.board.index(2)] != 0:
                self.white_in_check = True
                self.highlights[self.board.index(2)] = 20
            else:
                self.white_in_check = False

            # Checking if black is in check
            if self.white_attacks[self.board.index(12)] != 0:
                self.black_in_check = True
                self.highlights[self.board.index(12)] = 20
            else:
                self.black_in_check = False

            # Checking for victory and draws
            if self.check_win():
                if self.whose_turn:
                    self.program.menu.black_won = True
                else:
                    self.program.menu.white_won = True
            elif self.check_draw():
                self.program.menu.draw = True

            self.last_move = index
            # self.bot.evaluate_pos(self.pieces, self.board)
            if self.flip:
                self.program.menu.swap_players()
            self.past_positions.append(self.board)
            return

        # Deselecting the pieces
        if self.pieces[index] is None:
            self.deselect_all(False)
            self.program.update()
            return

        # Selecting the piece
        if self.whose_turn and self.pieces[index].color == 0:
            self.deselect_all(False)
            moves = self.pieces[index].get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.white_can_short_castle, self.white_can_long_castle)
            self.highlight_moves(moves, index)
            self.selected_piece = self.pieces[index]
            self.program.update()
        elif not self.whose_turn and self.pieces[index].color == 1:
            self.deselect_all(False)
            moves = self.pieces[index].get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.black_can_short_castle, self.black_can_long_castle)
            self.highlight_moves(moves, index)
            self.selected_piece = self.pieces[index]
            self.program.update()

    def process_right_mouse_click(self, mouse_pos, mouse_button_down):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1] - self.y_offset
        if (self.flip and self.whose_turn) or (not self.flip and self.white_is_player):
            index = int(mouse_x // self.square_size + self.num_of_rows * (mouse_y // self.square_size))
        else:
            index = 63 - int(mouse_x // self.square_size + self.num_of_rows * (mouse_y // self.square_size))
        if 0 > index or index >= self.num_of_squares:
            return

        if mouse_button_down:
            self.highlight_index = index
        else:
            if self.highlight_index == index:
                if self.highlights[index] >= 100:
                    self.highlights[index] -= 100
                else:
                    self.highlights[index] += 100
            elif self.highlight_index != index:
                if not (self.flip and self.whose_turn) and not (not self.flip and self.white_is_player):
                    index, self.highlight_index = -index + 63, -self.highlight_index + 63
                if (self.highlight_index, index) not in self.arrows:
                    self.arrows.append((self.highlight_index, index))
                else:
                    self.arrows.remove((self.highlight_index, index))

    def swap_in_list(self, list, a, b):
        if a == b: return list
        if a > b: a, b = b, a
        return list[:a] + list[b:b + 1] + list[a + 1:b] + list[a:a + 1] + list[b + 1:]

    def update_lists(self, a, b):
        self.pieces = self.swap_in_list(self.pieces, a, b)
        self.board = self.swap_in_list(self.board, a, b)

    def check_win(self):
        if self.timer_bottom.time <= 0:
            return True
        if not self.white_in_check and not self.black_in_check:
            return False

        for piece in self.pieces:
            if piece is None or (piece.color == 0 and not self.white_in_check) or (piece.color == 1 and not self.black_in_check):
                continue

            moves = []
            if piece.color == 0:
                moves = piece.get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.white_can_short_castle, self.white_can_long_castle)
            elif piece.color == 1:
                moves = piece.get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.black_can_short_castle, self.black_can_long_castle)

            if (self.white_in_check and piece.color == 0 and len(moves) > 0) or (self.black_in_check and piece.color == 1 and len(moves) > 0):
                return False

        return True

    def check_draw(self):
        if self.fifty_move_rule >= 100:
            return True
        for position in self.past_positions:
            if self.past_positions.count(position) >= 3:
                return True
        if self.white_in_check or self.black_in_check:
            return False

        white_stalemate = True
        black_stalemate = True

        for piece in self.pieces:
            if not white_stalemate and not black_stalemate:
                return False

            if piece is None:
                continue

            moves = []
            if piece.color == 0:
                moves = piece.get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.white_can_short_castle, self.white_can_long_castle)
            elif piece.color == 1:
                moves = piece.get_legal_moves(-1, -1, self.board, self.pieces, self.last_move, self.can_en_passant, self.black_can_short_castle, self.black_can_long_castle)

            if piece.color == 0 and len(moves) > 0:
                white_stalemate = False
            elif piece.color == 1 and len(moves) > 0:
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
                square = Square(self.num_of_rows, self.screen, self.square_size, i, self.highlights[i], self.y_offset)
                self.squares.append(square)

                if v != 0:
                    piece = Piece(self, i, i, v, self.y_offset)

                self.pieces.append(piece)
        else:
            for i, v in enumerate(self.board):
                piece = None
                square = Square(self.num_of_rows, self.screen, self.square_size, 63 - i, self.highlights[i], self.y_offset)
                self.squares.append(square)

                if v != 0:
                    piece = Piece(self, 63 - i, i, v, self.y_offset)

                self.pieces.append(piece)

        for arrow in self.arrows:
            arr = Arrow(self.screen, arrow[0], arrow[1], self.num_of_rows, self.square_size, self.y_offset)

        if not self.flip:
            return
        self.timer_top.update()
        self.timer_bottom.update()
        if self.timer_bottom.time <= 0:
            if self.whose_turn:
                self.program.menu.black_won = True
            else:
                self.program.menu.white_won = True

    def reset_attacks(self, pieces, board):
        white_attacks = []
        black_attacks = []

        for i in range(self.num_of_squares):
            white_attacks.append(0)
            black_attacks.append(0)

        for piece in pieces:
            if piece is None:
                continue
            attacks = piece.get_attacks(-1, -1, board, pieces)
            if piece.color == 0:
                for attack in attacks:
                    white_attacks[attack] += 1

            elif piece.color == 1:
                for attack in attacks:
                    black_attacks[attack] += 1

        return black_attacks, white_attacks

    def deselect_all(self, deselect_highlight):
        if deselect_highlight:
            self.arrows = []
        for i, v in enumerate(self.highlights):
            if v >= 10 and not deselect_highlight:
                self.highlights[i] = (v // 10) * 10
                continue
            self.highlights[i] = 0

    def highlight_moves(self, moves, index):
        self.highlights[index] += 1
        for move in moves:
            self.highlights[move] += 1

    def get_white_captured_pieces(self):
        white_captured_pieces = []
        num_of_pawns = 0
        num_of_queens = 0
        num_of_rooks = 0
        num_of_bishops = 0
        num_of_knights = 0
        for v in self.board:
            match v:
                case 1:
                    num_of_pawns += 1
                case 3:
                    num_of_queens += 1
                case 4:
                    num_of_rooks += 1
                case 5:
                    num_of_bishops += 1
                case 6:
                    num_of_knights += 1

        if num_of_queens == 0:
            white_captured_pieces.append(3)
        for i in range(2 - num_of_rooks):
            white_captured_pieces.append(4)
        for i in range(2 - num_of_bishops):
            white_captured_pieces.append(5)
        for i in range(2 - num_of_knights):
            white_captured_pieces.append(6)
        for i in range(8 - num_of_pawns):
            white_captured_pieces.append(1)

        return white_captured_pieces

    def get_black_captured_pieces(self):
        black_captured_pieces = []
        num_of_pawns = 0
        num_of_queens = 0
        num_of_rooks = 0
        num_of_bishops = 0
        num_of_knights = 0
        for v in self.board:
            match v:
                case 11:
                    num_of_pawns += 1
                case 13:
                    num_of_queens += 1
                case 14:
                    num_of_rooks += 1
                case 15:
                    num_of_bishops += 1
                case 16:
                    num_of_knights += 1

        if num_of_queens == 0:
            black_captured_pieces.append(3)
        for i in range(2 - num_of_rooks):
            black_captured_pieces.append(4)
        for i in range(2 - num_of_bishops):
            black_captured_pieces.append(5)
        for i in range(2 - num_of_knights):
            black_captured_pieces.append(6)
        for i in range(8 - num_of_pawns):
            black_captured_pieces.append(1)

        return black_captured_pieces

    def get_white_material_advantage(self):
        adv = 0
        for v in self.board:
            match v:
                case 1:
                    adv += 1
                case 3:
                    adv += 9
                case 4:
                    adv += 5
                case 5:
                    adv += 3
                case 6:
                    adv += 3
                case 11:
                    adv -= 1
                case 13:
                    adv -= 9
                case 14:
                    adv -= 5
                case 15:
                    adv -= 3
                case 16:
                    adv -= 3

        return adv
