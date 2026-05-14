import pygame

class Piece:
    def __init__(self, game, graphics_index, index, value, y_offset):
        self.game = game

        self.color = value % 100 // 10
        self.value = value

        self.index = index

        self.get_image()
        self.x = graphics_index % self.game.num_of_rows * self.game.square_size + self.game.square_size // 2 - self.image.get_rect().width // 2
        self.y = graphics_index // self.game.num_of_rows * self.game.square_size + self.game.square_size // 2 - self.image.get_rect().height // 2 + y_offset

        self.game.screen.blit(self.image, (self.x, self.y))

    def get_image(self):
        match self.value % 100:
            case 1:
                self.image = pygame.image.load("images/white-pawn.png")
            case 2:
                self.image = pygame.image.load("images/white-king.png")
            case 3:
                self.image = pygame.image.load("images/white-queen.png")
            case 4:
                self.image = pygame.image.load("images/white-rook.png")
            case 5:
                self.image = pygame.image.load("images/white-bishop.png")
            case 6:
                self.image = pygame.image.load("images/white-knight.png")

            case 11:
                self.image = pygame.image.load("images/black-pawn.png")
            case 12:
                self.image = pygame.image.load("images/black-king.png")
            case 13:
                self.image = pygame.image.load("images/black-queen.png")
            case 14:
                self.image = pygame.image.load("images/black-rook.png")
            case 15:
                self.image = pygame.image.load("images/black-bishop.png")
            case 16:
                self.image = pygame.image.load("images/black-knight.png")

            case _:
                self.image = pygame.image.load("images/white-pawn.png")

    def select(self):
        # Selecting own square
        self.game.board[self.index] += 100

        # Getting the legal moves and selecting all of them
        self.get_legal_moves(True, self.game.board)
        for move in self.legal_moves:
            self.game.board[move] += 100

    def capture(self):
        # Deleting the piece from the board
        self.game.board[self.index] = 100
        self.game.pieces[self.index] = None

    def check_bounds(self, index):
        # Allowing the move as long as it's in the list, and it's no more than four columns away
        if 0 <= index < self.game.num_of_squares and abs((self.index % self.game.num_of_rows) - (index % self.game.num_of_rows)) < 4:
            return True
        return False

    def check_moving(self, index):
        # Allowing the move if the space is empty or the piece is of the other color
        if self.game.pieces[index] is None:
            return True
        if self.game.board[index] == 0 or self.game.pieces[index].color != self.color:
            return True
        return False

    def check_check(self, move):
        # Simulating the move
        pieces = self.game.swap_in_list(self.game.pieces, move, self.index)
        board = self.game.swap_in_list(self.game.board, move, self.index)

        # Simulating taking the piece if necessary
        if pieces[self.index] is not None and board[self.index] != 0:
            pieces[self.index] = None
            board[self.index] = 0

        # Getting the attacks in the simulated position and checking if the relevant king is in check
        attacks = self.game.reset_attacks(pieces, board)[self.color]
        if attacks[self.game.board.index(2 + 10 * self.color)] == 0:
            return True

        return False

    def check_checks(self):
        # Emptying the moves that need to be removed
        removed_moves = []

        # Going through every move, checking it and removing if necessary
        for move in self.legal_moves:
            if not self.check_check(move):
                 removed_moves.append(move)
        for move in removed_moves:
            self.legal_moves.remove(move)

    def get_straight(self, end, step, board):
        has_hit_king = False
        for i in range(self.index, end, step):
            if i == self.index:
                continue

            if not self.check_moving(i):
                self.attacks.append(i)
                break

            if not has_hit_king:
                self.legal_moves.append(i)
            self.attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and self.game.pieces[i].color != self.color:
                    has_hit_king = True
                else:
                    break

    def get_diagonal_right(self, end, step, board):
        has_hit_king = False
        for i in range(self.index, end, step):
            if i == self.index:
                continue

            if i % self.game.num_of_rows < self.index % self.game.num_of_rows:
                break

            if not self.check_moving(i):
                self.attacks.append(i)
                break

            if not has_hit_king:
                self.legal_moves.append(i)
            self.attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and self.game.pieces[i].color != self.color:
                    has_hit_king = True
                else:
                    break

    def get_diagonal_left(self, end, step, board):
        has_hit_king = False
        for i in range(self.index, end, step):
            if i == self.index:
                continue

            if i % self.game.num_of_rows > self.index % self.game.num_of_rows:
                break

            if not self.check_moving(i):
                self.attacks.append(i)
                break

            if not has_hit_king:
                self.legal_moves.append(i)
            self.attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and self.game.pieces[i].color != self.color:
                    has_hit_king = True
                else:
                    break