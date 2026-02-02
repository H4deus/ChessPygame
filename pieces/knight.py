from piece import Piece

class Knight(Piece):
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

        self.possible_moves = [self.index - self.game.num_of_rows * 2 - 1, self.index - self.game.num_of_rows * 2 + 1,
                               self.index - self.game.num_of_rows - 2, self.index - self.game.num_of_rows + 2,
                               self.index + self.game.num_of_rows - 2, self.index + self.game.num_of_rows + 2,
                               self.index + self.game.num_of_rows * 2 - 1, self.index + self.game.num_of_rows * 2 + 1]

        for move in self.possible_moves:
            self.check_index(move)

        if check_checks:
            self.check_checks()

    def check_index(self, index):
        if self.check_bounds(index):
            if self.check_moving(index):
                self.legal_moves.append(index)
            self.attacks.append(index)