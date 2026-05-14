from piece import Piece

class Pawn(Piece):
    def __init__(self, game, graphics_index, index, value, y_offset):
        Piece.__init__(self, game, graphics_index, index, value, y_offset)

        self.game = game

        self.index = index

        self.has_moved = False

        self.legal_moves = []
        self.attacks = []

    def get_legal_moves(self, check_checks, board):
        self.legal_moves = []
        self.attacks = []

        on_left_edge = True if self.index % self.game.num_of_rows == 0 else False
        on_right_edge = True if self.index % self.game.num_of_rows == 7 else False

        # White
        if self.color == 0:
            # Getting the moves forward
            if self.game.board[self.index - self.game.num_of_rows] == 0:
                if self.index in range(48, 56) and self.game.board[self.index - self.game.num_of_rows * 2] == 0:
                    self.legal_moves.append(self.index - self.game.num_of_rows * 2)
                self.legal_moves.append(self.index - self.game.num_of_rows)

            # Getting the captures
            if not on_left_edge:
                if ((self.game.board[self.index - self.game.num_of_rows - 1] // 10 == 1) or # Normal capture
                        (self.game.board[self.index - 1] == 11 and self.index - 1 == self.game.last_move and self.game.can_en_passant)): # En passant
                    self.legal_moves.append(self.index - self.game.num_of_rows - 1)
                self.attacks.append(self.index - self.game.num_of_rows - 1)

            if not on_right_edge:
                if ((self.game.board[self.index - self.game.num_of_rows + 1] // 10 == 1) or # Normal capture
                        (self.game.board[self.index + 1] == 11 and self.index + 1 == self.game.last_move and self.game.can_en_passant)): # En passant
                    self.legal_moves.append(self.index - self.game.num_of_rows + 1)
                self.attacks.append(self.index - self.game.num_of_rows + 1)

        # Black
        elif self.color == 1:
            # Getting the moves forward
            if self.game.board[self.index + self.game.num_of_rows] == 0:
                if self.index in range(8, 16) and self.game.board[self.index + self.game.num_of_rows * 2] == 0:
                    self.legal_moves.append(self.index + self.game.num_of_rows * 2)
                self.legal_moves.append(self.index + self.game.num_of_rows)

            # Getting the captures
            if not on_left_edge:
                if ((self.game.board[self.index + self.game.num_of_rows - 1] // 10 != 1 and self.game.board[self.index + self.game.num_of_rows - 1] != 0) # Normal capture
                        or (self.game.board[self.index - 1] == 1 and self.index - 1 == self.game.last_move and self.game.can_en_passant)): # En passant
                    self.legal_moves.append(self.index + self.game.num_of_rows - 1)
                self.attacks.append(self.index + self.game.num_of_rows - 1)

            if not on_right_edge:
                if ((self.game.board[self.index + self.game.num_of_rows + 1] // 10 != 1 and self.game.board[self.index + self.game.num_of_rows + 1] != 0) # Normal capture
                        or (self.game.board[self.index + 1] == 1 and self.index + 1 == self.game.last_move and self.game.can_en_passant)): # En passant
                    self.legal_moves.append(self.index + self.game.num_of_rows + 1)
                self.attacks.append(self.index + self.game.num_of_rows + 1)

        if check_checks:
            self.check_checks()
