from piece import Piece

class King(Piece):
    def __init__(self, game, index, value):
        Piece.__init__(self, game, index, value)

        self.game = game

        self.index = index

        self.has_moved = False

        self.legal_moves = []
        self.attacks = []
        self.possible_moves = []

    def get_legal_moves(self, check_checks, board):
        self.legal_moves = []
        self.attacks = []

        self.possible_moves = [self.index - self.game.num_of_rows - 1, self.index - self.game.num_of_rows, self.index - self.game.num_of_rows + 1,
                               self.index - 1, self.index + 1,
                               self.index + self.game.num_of_rows - 1, self.index + self.game.num_of_rows, self.index + self.game.num_of_rows + 1]

        for move in self.possible_moves:
           self.check_index(move)

        if not check_checks:
            return

        # Castling
        if self.color == 0:
            if self.game.white_can_short_castle:
                self.check_short_castle(self.game.black_attacks)

            if self.game.white_can_long_castle:
                self.check_long_castle(self.game.black_attacks)

        elif self.color == 1:
            if self.game.black_can_short_castle:
                self.check_short_castle(self.game.white_attacks)

            if self.game.black_can_long_castle:
                self.check_long_castle(self.game.white_attacks)

    def check_index(self, index):
        if self.check_bounds(index):
            if self.check_moving(index):
                if self.color == 0 and self.game.black_attacks[index] == 0:
                    self.legal_moves.append(index)
                elif self.color == 1 and self.game.white_attacks[index] == 0:
                    self.legal_moves.append(index)
            self.attacks.append(index)

    def check_short_castle(self, attacks):
        can_short_castle = True
        for i in range(1, 3):
            if self.game.board[self.index + i] == 0 and attacks[self.index + i] == 0:
                continue
            can_short_castle = False
        if can_short_castle:
            self.legal_moves.append(self.index + 2)

    def check_long_castle(self, attacks):
        can_long_castle = True
        for i in range(1, 4):
            if self.game.board[self.index - i] == 0 and attacks[self.index - i] == 0:
                continue
            can_long_castle = False
        if can_long_castle:
            self.legal_moves.append(self.index - 2)