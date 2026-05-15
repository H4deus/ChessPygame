import pygame

class Piece:
    def __init__(self, game, graphics_index, index, value, y_offset):
        self.game = game
        self.num_of_rows = game.num_of_rows
        self.num_of_squares = game.num_of_squares

        self.color = value // 10

        self.piece = value % 10
        self.index = index
        self.value = value

        match value:
            case 1:
                image = pygame.image.load("images/white-pawn.png")
            case 2:
                image = pygame.image.load("images/white-king.png")
            case 3:
                image = pygame.image.load("images/white-queen.png")
            case 4:
                image = pygame.image.load("images/white-rook.png")
            case 5:
                image = pygame.image.load("images/white-bishop.png")
            case 6:
                image = pygame.image.load("images/white-knight.png")

            case 11:
                image = pygame.image.load("images/black-pawn.png")
            case 12:
                image = pygame.image.load("images/black-king.png")
            case 13:
                image = pygame.image.load("images/black-queen.png")
            case 14:
                image = pygame.image.load("images/black-rook.png")
            case 15:
                image = pygame.image.load("images/black-bishop.png")
            case 16:
                image = pygame.image.load("images/black-knight.png")

            case _:
                image = pygame.image.load("images/white-pawn.png")

        x = graphics_index % self.num_of_rows * game.square_size + game.square_size // 2 - image.get_rect().width // 2
        y = graphics_index // self.num_of_rows * game.square_size + game.square_size // 2 - image.get_rect().height // 2 + y_offset

        self.game.screen.blit(image, (x, y))

    def get_legal_moves(self, index, color, board, pieces, last_move=0, can_en_passant=False, can_short_castle=False, can_long_castle=False):
        if index < 0:
            index = self.index
        if color < 0:
            color = self.color
        match self.piece:
            case 1:
                return self.get_pawn_legal_moves_and_attacks(index, color, True, board, pieces, last_move, can_en_passant)[0]
            case 2:
                return self.get_king_legal_moves_and_attacks(index, color, True, board, pieces, can_short_castle, can_long_castle)[0]
            case 3:
                return self.get_queen_legal_moves_and_attacks(index, color, True, board, pieces)[0]
            case 4:
                return self.get_rook_legal_moves_and_attacks(index, color, True, board, pieces)[0]
            case 5:
                return self.get_bishop_legal_moves_and_attacks(index, color, True, board, pieces)[0]
            case 6:
                return self.get_knight_legal_moves_and_attacks(index, color, True, board, pieces)[0]

            case _:
                return []

    def get_attacks(self, index, color, board, pieces, last_move=0, can_en_passant=False, can_short_castle=False, can_long_castle=False):
        if index < 0:
            index = self.index
        if color < 0:
            color = self.color
        match self.piece:
            case 1:
                return self.get_pawn_legal_moves_and_attacks(index, color, False, board, pieces, last_move, can_en_passant)[1]
            case 2:
                return self.get_king_legal_moves_and_attacks(index, color, False, board, pieces, can_short_castle, can_long_castle)[1]
            case 3:
                return self.get_queen_legal_moves_and_attacks(index, color, False, board, pieces)[1]
            case 4:
                return self.get_rook_legal_moves_and_attacks(index, color, False, board, pieces)[1]
            case 5:
                return self.get_bishop_legal_moves_and_attacks(index, color, False, board, pieces)[1]
            case 6:
                return self.get_knight_legal_moves_and_attacks(index, color, False, board, pieces)[1]

            case _:
                return []

    def check_bounds(self, index, start_index):
        # Allowing the move as long as it's in the list, and it's no more than four columns away
        if 0 <= index < self.num_of_squares and abs((start_index % self.num_of_rows) - (index % self.num_of_rows)) < 4:
            return True
        return False

    def check_moving(self, index, color, board, pieces):
        # Allowing the move if the space is empty or the piece is of the other color
        if pieces[index] is None:
            return True
        if board[index] == 0 or pieces[index].color != color:
            return True
        return False

    def check_check(self, move, index, color, board, pieces):
        # Simulating the move
        pieces = self.game.swap_in_list(pieces, move, index)
        board = self.game.swap_in_list(board, move, index)

        # Simulating taking the piece if necessary
        if pieces[index] is not None and board[index] != 0:
            pieces[index] = None
            board[index] = 0

        # Getting the attacks in the simulated position and checking if the relevant king is in check
        attacks = self.game.reset_attacks(pieces, board)[color]
        if attacks[board.index(2 + 10 * color)] == 0:
            return True

        return False

    def get_removed_moves(self, legal_moves, index, color, board, pieces):
        # Emptying the moves that need to be removed
        removed_moves = []

        # Going through every move, checking it and removing if necessary
        for move in legal_moves:
            if not self.check_check(move, index, color, board, pieces):
                 removed_moves.append(move)
        return removed_moves

    def get_orthogonal(self, index, color, end, step, board, pieces):
        legal_moves = []
        attacks = []
        has_hit_king = False
        for i in range(index, end, step):
            if i == index:
                continue

            if not self.check_moving(i, color, board, pieces):
                attacks.append(i)
                break

            if not has_hit_king:
                legal_moves.append(i)
            attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and pieces[i].color != color:
                    has_hit_king = True
                else:
                    break
        
        return legal_moves, attacks

    def get_diagonal_right(self, index, color, end, step, board, pieces):
        legal_moves = []
        attacks = []
        has_hit_king = False
        for i in range(index, end, step):
            if i == index:
                continue

            if i % self.num_of_rows < index % self.num_of_rows:
                break

            if not self.check_moving(i, color, board, pieces):
                attacks.append(i)
                break

            if not has_hit_king:
                legal_moves.append(i)
            attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and pieces[i].color != color:
                    has_hit_king = True
                else:
                    break
        
        return legal_moves, attacks

    def get_diagonal_left(self, index, color, end, step, board, pieces):
        legal_moves = []
        attacks = []
        has_hit_king = False
        for i in range(index, end, step):
            if i == index:
                continue

            if i % self.num_of_rows > index % self.num_of_rows:
                break

            if not self.check_moving(i, color, board, pieces):
                attacks.append(i)
                break

            if not has_hit_king:
                legal_moves.append(i)
            attacks.append(i)

            if board[i] != 0:
                if board[i] % 10 == 2 and pieces[i].color != color:
                    has_hit_king = True
                else:
                    break
        
        return legal_moves, attacks

    def get_rook_legal_moves_and_attacks(self, index, color, check_checks, board, pieces):
        legal_moves = []
        attacks = []

        left, left_attacks = self.get_orthogonal(index, color, self.num_of_rows * (index // self.num_of_rows) - 1, -1, board, pieces)
        right, right_attacks = self.get_orthogonal(index, color, self.num_of_rows * ((index + self.num_of_rows) // self.num_of_rows), 1, board, pieces)
        up, up_attacks = self.get_orthogonal(index, color, -1, -self.num_of_rows, board, pieces)
        down, down_attacks = self.get_orthogonal(index, color, self.num_of_squares, self.num_of_rows, board, pieces)
        
        for move in left:
            legal_moves.append(move)
        for move in right:
            legal_moves.append(move)
        for move in up:
            legal_moves.append(move)
        for move in down:
            legal_moves.append(move)
        
        for attack in left_attacks:
            attacks.append(attack)
        for attack in right_attacks:
            attacks.append(attack)
        for attack in up_attacks:
            attacks.append(attack)
        for attack in down_attacks:
            attacks.append(attack)
        
        if check_checks:
            removed_moves = self.get_removed_moves(legal_moves, index, color, board, pieces)
            for move in removed_moves:
                legal_moves.remove(move)
        
        return legal_moves, attacks

    def get_bishop_legal_moves_and_attacks(self, index, color, check_checks, board, pieces):
        legal_moves = []
        attacks = []

        top_left, top_left_attacks = self.get_diagonal_left(index, color, -1, -self.num_of_rows - 1, board, pieces)
        bottom_left, bottom_left_attacks = self.get_diagonal_left(index, color, self.num_of_squares, self.num_of_rows - 1, board, pieces)

        top_right, top_right_attacks = self.get_diagonal_right(index, color, -1, -self.num_of_rows + 1, board, pieces)
        bottom_right, bottom_right_attacks = self.get_diagonal_right(index, color, self.num_of_squares, self.num_of_rows + 1, board, pieces)
        
        for move in top_left:
            legal_moves.append(move)
        for move in bottom_left:
            legal_moves.append(move)
        for move in top_right:
            legal_moves.append(move)
        for move in bottom_right:
            legal_moves.append(move)
        
        for attack in top_left_attacks:
            attacks.append(attack)
        for attack in bottom_left_attacks:
            attacks.append(attack)
        for attack in top_right_attacks:
            attacks.append(attack)
        for attack in bottom_right_attacks:
            attacks.append(attack)

        if check_checks:
            removed_moves = self.get_removed_moves(legal_moves, index, color, board, pieces)
            for move in removed_moves:
                legal_moves.remove(move)
        
        return legal_moves, attacks

    def get_queen_legal_moves_and_attacks(self, index, color, check_checks, board, pieces):
        legal_moves = []
        attacks = []

        left, left_attacks = self.get_orthogonal(index, color, self.num_of_rows * (index // self.num_of_rows) - 1, -1, board, pieces)
        right, right_attacks = self.get_orthogonal(index, color, self.num_of_rows * ((index + self.num_of_rows) // self.num_of_rows), 1, board, pieces)
        up, up_attacks = self.get_orthogonal(index, color, -1, -self.num_of_rows, board, pieces)
        down, down_attacks = self.get_orthogonal(index, color, self.num_of_squares, self.num_of_rows, board, pieces)

        top_left, top_left_attacks = self.get_diagonal_left(index, color, -1, -self.num_of_rows - 1, board, pieces)
        bottom_left, bottom_left_attacks = self.get_diagonal_left(index, color, self.num_of_squares, self.num_of_rows - 1, board, pieces)

        top_right, top_right_attacks = self.get_diagonal_right(index, color, -1, -self.num_of_rows + 1, board, pieces)
        bottom_right, bottom_right_attacks = self.get_diagonal_right(index, color, self.num_of_squares, self.num_of_rows + 1, board, pieces)
        
        for move in left:
            legal_moves.append(move)
        for move in right:
            legal_moves.append(move)
        for move in up:
            legal_moves.append(move)
        for move in down:
            legal_moves.append(move)
        
        for move in top_left:
            legal_moves.append(move)
        for move in bottom_left:
            legal_moves.append(move)
        for move in top_right:
            legal_moves.append(move)
        for move in bottom_right:
            legal_moves.append(move)
        
        for attack in left_attacks:
            attacks.append(attack)
        for attack in right_attacks:
            attacks.append(attack)
        for attack in up_attacks:
            attacks.append(attack)
        for attack in down_attacks:
            attacks.append(attack)
        
        for attack in top_left_attacks:
            attacks.append(attack)
        for attack in bottom_left_attacks:
            attacks.append(attack)
        for attack in top_right_attacks:
            attacks.append(attack)
        for attack in bottom_right_attacks:
            attacks.append(attack)

        if check_checks:
            removed_moves = self.get_removed_moves(legal_moves, index, color, board, pieces)
            for move in removed_moves:
                legal_moves.remove(move)
        
        return legal_moves, attacks

    def get_king_legal_moves_and_attacks(self, index, color, check_checks, board, pieces, can_short_castle, can_long_castle):
        legal_moves = []
        attacks = []

        possible_moves = [index - self.num_of_rows - 1, index - self.num_of_rows, index - self.num_of_rows + 1,
                          index - 1,                                                                 index + 1,
                          index + self.num_of_rows - 1, index + self.num_of_rows, index + self.num_of_rows + 1]

        if check_checks:
            enemy_attacks = self.game.reset_attacks(pieces, board)[color]
        
        # Castling
            if can_short_castle and self.check_short_castle(index, board, enemy_attacks):
                legal_moves.append(index + 2)

            if can_long_castle and self.check_long_castle(index, board, enemy_attacks):
                legal_moves.append(index - 2)
        
        for move in possible_moves:
            if not self.check_bounds(move, index):
                continue
               
            attacks.append(move)
           
            if not self.check_moving(move, color, board, pieces):
                continue
           
            if check_checks and enemy_attacks[move] == 0:
                legal_moves.append(move)

        return legal_moves, attacks

    def get_knight_legal_moves_and_attacks(self, index, color, check_checks, board, pieces):
        legal_moves = []
        attacks = []

        possible_moves = [index - self.num_of_rows * 2 - 1, index - self.num_of_rows * 2 + 1,
                          index - self.num_of_rows - 2, index - self.num_of_rows + 2,
                          index + self.num_of_rows - 2, index + self.num_of_rows + 2,
                          index + self.num_of_rows * 2 - 1, index + self.num_of_rows * 2 + 1]

        for move in possible_moves:
            if not self.check_bounds(move, index):
                continue
            if self.check_moving(move, color, board, pieces):
                legal_moves.append(move)
            attacks.append(move)

        if check_checks:
            removed_moves = self.get_removed_moves(legal_moves, index, color, board, pieces)
            for move in removed_moves:
                legal_moves.remove(move)

        return legal_moves, attacks

    def get_pawn_legal_moves_and_attacks(self, index, color, check_checks, board, pieces, last_move, can_en_passant):
        legal_moves = []
        attacks = []

        on_left_edge = True if index % self.num_of_rows == 0 else False
        on_right_edge = True if index % self.num_of_rows == 7 else False

        # White
        if color == 0:
            # Getting the moves forward
            if board[index - self.num_of_rows] == 0:
                if index in range(48, 56) and board[index - self.num_of_rows * 2] == 0:
                    legal_moves.append(index - self.num_of_rows * 2)
                legal_moves.append(index - self.num_of_rows)

            # Getting the captures
            if not on_left_edge:
                if ((board[index - self.num_of_rows - 1] // 10 == 1) or # Normal capture
                        (board[index - 1] == 11 and index - 1 == last_move and can_en_passant)): # En passant
                    legal_moves.append(index - self.num_of_rows - 1)
                attacks.append(index - self.num_of_rows - 1)

            if not on_right_edge:
                if ((board[index - self.num_of_rows + 1] // 10 == 1) or # Normal capture
                        (board[index + 1] == 11 and index + 1 == last_move and can_en_passant)): # En passant
                    legal_moves.append(index - self.num_of_rows + 1)
                attacks.append(index - self.num_of_rows + 1)

        # Black
        elif color == 1:
            # Getting the moves forward
            if board[index + self.num_of_rows] == 0:
                if index in range(8, 16) and board[index + self.num_of_rows * 2] == 0:
                    legal_moves.append(index + self.num_of_rows * 2)
                legal_moves.append(index + self.num_of_rows)

            # Getting the captures
            if not on_left_edge:
                if ((board[index + self.num_of_rows - 1] // 10 != 1 and board[index + self.num_of_rows - 1] != 0) # Normal capture
                        or (board[index - 1] == 1 and index - 1 == last_move and can_en_passant)): # En passant
                    legal_moves.append(index + self.num_of_rows - 1)
                attacks.append(index + self.num_of_rows - 1)

            if not on_right_edge:
                if ((board[index + self.num_of_rows + 1] // 10 != 1 and board[index + self.num_of_rows + 1] != 0) # Normal capture
                        or (board[index + 1] == 1 and index + 1 == last_move and can_en_passant)): # En passant
                    legal_moves.append(index + self.num_of_rows + 1)
                attacks.append(index + self.num_of_rows + 1)

        if check_checks:
            removed_moves = self.get_removed_moves(legal_moves, index, color, board, pieces)
            for move in removed_moves:
                legal_moves.remove(move)
        
        return legal_moves, attacks

    def check_short_castle(self, index, board, attacks):
        can_short_castle = True
        for i in range(1, 3):
            if board[index + i] == 0 and attacks[index + i] == 0:
                continue
            can_short_castle = False
        return can_short_castle

    def check_long_castle(self, index, board, attacks):
        can_long_castle = True
        for i in range(1, 4):
            if board[index - i] == 0 and attacks[index - i] == 0:
                continue
            can_long_castle = False
        return can_long_castle