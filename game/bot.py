class Bot:
    def __init__(self, game):
        self.game = game
        self.color = 1

    def get_move(self):
        ...

    def set_color(self, color):
        self.color = color

    def evaluate_pos(self, pieces, board):
        score = 0
        for piece in board:
            piece = piece % 100
            if piece // 10 == self.color:
                piece = piece % 10
                if piece == 1:
                    score += 1
                elif piece == 3:
                    score += 9
                elif piece == 4:
                    score += 5
                elif piece == 5 or piece == 6:
                    score += 3
            else:
                piece = piece % 10
                if piece == 1:
                    score -= 1
                elif piece == 3:
                    score -= 9
                elif piece == 4:
                    score -= 5
                elif piece == 5 or piece == 6:
                    score -= 3

        black_attacks, white_attacks = self.game.reset_attacks(pieces, board)
        if black_attacks[board.index(2)] > 0:
            if self.color == 0:
                score -= 10
            else:
                score += 5
        if white_attacks[board.index(12)] > 0:
            if self.color == 1:
                score -= 10
            else:
                score += 5

        if 3 in board and black_attacks[board.index(3)] > 0:
            if self.color == 0:
                score -= 9
            else:
                score += 9
        if 13 in board and white_attacks[board.index(13)] > 0:
            if self.color == 1:
                score -= 9
            else:
                score += 9

        print(score)
        return score
