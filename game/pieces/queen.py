from piece import Piece

class Queen(Piece):
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

        self.get_straight(self.game.num_of_rows * (self.index // self.game.num_of_rows) - 1, -1, board)  # Left
        self.get_straight(self.game.num_of_rows * ((self.index + self.game.num_of_rows) // self.game.num_of_rows),1, board)  # Right
        self.get_straight(-1, -self.game.num_of_rows, board)  # Top
        self.get_straight(self.game.num_of_squares, self.game.num_of_rows, board)  # Bottom

        self.get_diagonal_left(-1, -self.game.num_of_rows - 1, board)  # Top left
        self.get_diagonal_left(self.game.num_of_squares, self.game.num_of_rows - 1, board)  # Bottom left

        self.get_diagonal_right(-1, -self.game.num_of_rows + 1, board)  # Top right
        self.get_diagonal_right(self.game.num_of_squares, self.game.num_of_rows + 1, board)  # Bottom right

        if check_checks:
            self.check_checks()