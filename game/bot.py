from piece import Piece

class Bot:
    def __init__(self, game):
        self.game = game
        self.num_of_rows = game.num_of_rows
        self.num_of_squares = game.num_of_squares
        self.color = 1 # 0 - white, 1 - black

        self.game_stage = 0 # 0 - opening, 1 - middlegame, 2 - endgame

        self.pawn_stages = [
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.2,  0.2,    0,    0,    0,
                   0,    0,    0,  0.2,  0.2,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0, -0.2, -0.2,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.2,  0.2,    0,    0,    0,
                 0.1,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1,  0.1,
                 0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                 0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,
                 0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,
                 0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,
                   0,    0,    0,    0,    0,    0,    0,    0,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                   0,    0,    0,    0,    0,    0,    0,    0
            ]
        ]

        self.king_stages = [
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                 0.2,  0.2, -0.2, -0.2, -0.2, -0.2,  0.2,  0.2
            ],
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                 0.2,  0.2,  0.1, -0.2, -0.2,  0.1,  0.2,  0.2
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0
            ]
        ]

        self.queen_stages = [
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,  0.1,  0.1,  0.1,  0.1,    0,    0,
                   0,    0,  0.1,  0.1,  0.1,  0.1,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,  0.1,  0.2,  0.2,  0.1,    0,    0,
                   0,    0,  0.1,  0.2,  0.2,  0.1,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,  0.1,  0.2,  0.2,  0.1,    0,    0,
                   0,    0,  0.1,  0.2,  0.2,  0.1,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0
            ]
        ]

        self.rook_stages = [
            [
                -0.3, -0.2,    0,    0,    0,    0, -0.2, -0.3,
                 0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                -0.3, -0.3,    0,  0.1,  0.1,    0, -0.3, -0.3
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                 0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0
            ],
            [
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,  0.1,  0.1,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0,
                   0,    0,    0,    0,    0,    0,    0,    0
            ]
        ]

        self.bishop_stages = [
            [
                -0.2, -0.2, -0.3, -0.2, -0.2, -0.3, -0.2, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2, -0.2, -0.3, -0.2, -0.2, -0.3, -0.2, -0.2
            ],
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ],
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,  0.1,  0.1,  0.2,  0.2,  0.1,  0.1, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,  0.1,    0,    0,    0,    0,  0.1, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ]
        ]

        self.knight_stages = [
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,    0,  0.1,    0,    0,  0.1,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,  0.2,    0,    0,  0.2,    0, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ],
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,    0,  0.1,    0,    0,  0.1,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,  0.1,    0,    0,  0.1,    0, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ],
            [
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2,    0,  0.1,    0,    0,  0.1,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,    0,  0.2,  0.2,    0,    0, -0.2,
                -0.2,    0,  0.1,    0,    0,  0.1,    0, -0.2,
                -0.2,    0,    0,  0.1,  0.1,    0,    0, -0.2,
                -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2
            ]
        ]

    def get_move(self, pieces, board, last_move, can_en_passant, white_can_short_castle, black_can_short_castle, white_can_long_castle, black_can_long_castle):
        best_move = []
        best_move_score = None

        enemy_best_move = []
        enemy_best_move_score = None

        for index, piece in enumerate(pieces):
            if piece is None or piece.color != self.color:
                continue
            
            if self.color == 0:
                legal_moves = piece.get_legal_moves(board, pieces, -1, -1, -1, last_move, can_en_passant, white_can_short_castle, white_can_long_castle)
            else:
                legal_moves = piece.get_legal_moves(board, pieces, -1, -1, -1, last_move, can_en_passant, black_can_short_castle, black_can_long_castle)

            new_white_can_short_castle = white_can_short_castle

            new_white_can_long_castle = white_can_long_castle

            new_black_can_short_castle = black_can_short_castle

            new_black_can_long_castle = black_can_long_castle

            for move in legal_moves:
                temp_board, temp_pieces, new_last_move, new_can_en_passant = self.process_move(board, pieces, piece, index, move, can_en_passant)

                # self.print_board(temp_board)

                # Castling
                # Disallowing if any of the relevant pieces have moved
                if temp_board[63] != 4 or temp_board[60] != 2:
                    new_white_can_short_castle = False

                if temp_board[56] != 4 or temp_board[60] != 2:
                    new_white_can_long_castle = False

                if temp_board[7] != 14 or temp_board[4] != 12:
                    new_black_can_short_castle = False

                if temp_board[0] != 14 or temp_board[4] != 12:
                    new_black_can_long_castle = False

                enemy_made_move = False
                enemy_best_move = []
                enemy_best_move_score = None

                for new_index, new_piece in enumerate(temp_pieces):
                    if new_piece is None or new_piece.color == self.color:
                        continue

                    if self.color == 0:
                        new_legal_moves = new_piece.get_legal_moves(temp_board, temp_pieces, -1, -1, -1, new_last_move, new_can_en_passant, new_black_can_short_castle, new_black_can_long_castle)
                    elif self.color == 1:
                        new_legal_moves = new_piece.get_legal_moves(temp_board, temp_pieces, -1, -1, -1, new_last_move, new_can_en_passant, new_white_can_short_castle, new_white_can_long_castle)

                    for new_move in new_legal_moves:
                        enemy_made_move = True
                        new_temp_board, new_temp_pieces, new_temp_last_move, new_temp_can_en_passant = self.process_move(temp_board, temp_pieces, new_piece, new_index, new_move, new_can_en_passant)

                        if enemy_best_move_score is None or self.evaluate_pos(new_temp_pieces, new_temp_board, True) < enemy_best_move_score:
                            enemy_best_move = [new_index, new_move]
                            enemy_best_move_score = self.evaluate_pos(new_temp_pieces, new_temp_board, True)

                black_attacks, white_attacks = self.game.reset_attacks(temp_pieces, temp_board)

                if 2 in temp_board and black_attacks[temp_board.index(2)] != 0:
                    white_in_check = True
                    print("white checked")
                else:
                    white_in_check = False

                # Checking if black is in check
                if 12 in temp_board and white_attacks[temp_board.index(12)] != 0:
                    black_in_check = True
                    print("black checked")
                else:
                    black_in_check = False

                if index == 59 and move == 31:
                    print(enemy_made_move, index, move, enemy_best_move, enemy_best_move_score)

                if not enemy_made_move:
                    print(index, move)
                    if self.color == 0 and black_in_check:
                        return [index, move]
                    elif self.color == 1 and white_in_check:
                        return [index, move]

                temp_board = self.swap_in_list(temp_board, enemy_best_move[0], enemy_best_move[1])
                temp_pieces = self.swap_in_list(temp_pieces, enemy_best_move[0], enemy_best_move[1])

                if best_move_score is None or self.evaluate_pos(temp_pieces, temp_board, True) > best_move_score:
                    best_move = [index, move]
                    best_move_score = self.evaluate_pos(temp_pieces, temp_board, True)

        # print(best_move, enemy_best_move, best_move_score)
        return best_move

    def swap_in_list(self, list, a, b):
        if a == b: return list
        if a > b: a, b = b, a
        return list[:a] + list[b:b + 1] + list[a + 1:b] + list[a:a + 1] + list[b + 1:]

    def set_color(self, color):
        self.color = color

    def evaluate_pos(self, pieces, board, my_turn):
        score = 0
        my_pawn_attacks, my_king_attacks, my_queen_attacks, my_rook_attacks, my_bishop_attacks, my_knight_attacks = self.get_own_attacks(pieces, board)
        enemy_pawn_attacks, enemy_king_attacks, enemy_queen_attacks, enemy_rook_attacks, enemy_bishop_attacks, enemy_knight_attacks = self.get_enemy_attacks(pieces, board)
        if self.color == 1:
            my_attacks, enemy_attacks = self.game.reset_attacks(pieces, board)
        else:
            enemy_attacks, my_attacks = self.game.reset_attacks(pieces, board)

        best_capture = 0

        changes = []

        for index, piece in enumerate(board):
            if piece == 0:
                continue

            match piece % 10:
                case 1:
                    value = 1
                case 2:
                    value = 0
                case 3:
                    value = 9
                case 4:
                    value = 5
                case 5:
                    value = 3
                case 6:
                    value = 3
                case _:
                    value = 0

            if piece // 10 == self.color:
                score += value

                match piece % 10:
                    case 1:
                        if self.color == 0:
                            score += self.pawn_stages[self.game_stage][index]
                            changes.append(self.pawn_stages[self.game_stage][index])
                        else:
                            score += self.pawn_stages[self.game_stage][63 - index]
                            changes.append(self.pawn_stages[self.game_stage][63-index])
                    case 2:
                        if self.color == 0:
                            score += self.king_stages[self.game_stage][index]
                            changes.append(self.king_stages[self.game_stage][index])
                        else:
                            score += self.king_stages[self.game_stage][63 - index]
                            changes.append(self.king_stages[self.game_stage][63-index])
                    case 3:
                        if self.color == 0:
                            score += self.queen_stages[self.game_stage][index]
                            changes.append(self.queen_stages[self.game_stage][index])
                        else:
                            score += self.queen_stages[self.game_stage][63 - index]
                            changes.append(self.queen_stages[self.game_stage][63-index])
                    case 4:
                        if self.color == 0:
                            score += self.rook_stages[self.game_stage][index]
                            changes.append(self.rook_stages[self.game_stage][index])
                        else:
                            score += self.rook_stages[self.game_stage][63 - index]
                            changes.append(self.rook_stages[self.game_stage][63-index])
                    case 5:
                        if self.color == 0:
                            score += self.bishop_stages[self.game_stage][index]
                            changes.append(self.bishop_stages[self.game_stage][index])
                        else:
                            score += self.bishop_stages[self.game_stage][63 - index]
                            changes.append(self.bishop_stages[self.game_stage][63-index])
                    case 6:
                        if self.color == 0:
                            score += self.knight_stages[self.game_stage][index]
                            changes.append(self.knight_stages[self.game_stage][index])
                        else:
                            score += self.knight_stages[self.game_stage][63 - index]
                            changes.append(self.knight_stages[self.game_stage][63-index])

                if piece % 10 == 2:
                    if enemy_attacks[index] > 0:
                        score -= 0.5
                        changes.append("my check")

                    possible_moves = [index - self.num_of_rows - 1, index - self.num_of_rows, index - self.num_of_rows + 1,
                                      index - 1,                                                                 index + 1,
                                      index + self.num_of_rows - 1, index + self.num_of_rows, index + self.num_of_rows + 1]

                    moves_taken_by_me = 0
                    moves_taken_by_en = 0
                    moves_available = 0
                    moves_unavailable = 0
                    moves_controlled = 0

                    for move in possible_moves:
                        if move < 0 or move > 63:
                            moves_unavailable += 1
                        elif board[move] // 10 == self.color and board[move] != 0:
                            moves_taken_by_me += 1
                        elif board[move] // 10 != self.color and board[move] != 0:
                            moves_taken_by_en += 1
                        elif enemy_attacks[move] > 0:
                            moves_controlled += 1
                        elif board[move] == 0:
                            moves_available += 1

                    if moves_taken_by_me < (8 - moves_unavailable) / 4 or moves_taken_by_me > (8 - moves_unavailable) / 1.5:
                        score -= 0.5
                        changes.append("my moves taken")

                    if moves_taken_by_en > 0:
                        score -= 0.5
                        changes.append("my en move amount")

                    if moves_available < 2:
                        score -= 0.5
                        changes.append("my move amount")

                    if moves_controlled > (8 - moves_unavailable) / 4:
                        score -= 0.5
                        changes.append("my move controlled")

                if enemy_attacks[index] > 0 or my_attacks[index] > 0:
                    my_pawns = my_pawn_attacks[index]
                    my_threes = my_bishop_attacks[index] + my_knight_attacks[index]
                    my_rooks = my_rook_attacks[index]
                    my_queens = my_queen_attacks[index]
                    my_kings = my_king_attacks[index]
                    my_full = my_attacks[index]
                    my_values = my_pawns + my_threes * 3 + my_rooks * 5 + my_queens * 9

                    enemy_pawns = enemy_pawn_attacks[index]
                    enemy_threes = enemy_bishop_attacks[index] + enemy_knight_attacks[index]
                    enemy_rooks = enemy_rook_attacks[index]
                    enemy_queens = enemy_queen_attacks[index]
                    enemy_kings = enemy_king_attacks[index]
                    enemy_full = enemy_attacks[index]
                    enemy_values = enemy_pawns + enemy_threes * 3 + enemy_rooks * 5 + enemy_queens * 9

                    my_vals = []
                    enemy_vals = []

                    for i in range(my_kings):
                        my_vals.append(0)
                    for i in range(my_queens):
                        my_vals.append(9)
                    for i in range(my_rooks):
                        my_vals.append(5)
                    for i in range(my_threes):
                        my_vals.append(3)
                    for i in range(my_pawns):
                        my_vals.append(1)

                    for i in range(enemy_kings):
                        enemy_vals.append(0)
                    for i in range(enemy_queens):
                        enemy_vals.append(9)
                    for i in range(enemy_rooks):
                        enemy_vals.append(5)
                    for i in range(enemy_threes):
                        enemy_vals.append(3)
                    for i in range(enemy_pawns):
                        enemy_vals.append(1)

                    if my_kings > 0 and enemy_full > my_full:
                        my_full -= 1

                    elif enemy_kings > 0 and enemy_full <= my_full:
                        enemy_full -= 1

                    if enemy_full == 0 or my_turn:
                        temp = best_capture

                    elif my_full == 0:
                        temp = -value

                    elif enemy_full > my_full:
                        if my_kings > 0:
                            my_full -= 1

                        temp = 0 - value - my_values + enemy_values

                        for i in range(enemy_full - my_full):
                            if i >= len(enemy_vals):
                                 break
                            temp -= enemy_vals[i]

                    elif enemy_full == my_full:
                        if enemy_kings > 0:
                            enemy_full -= 1

                        temp = 0 - value - my_values + enemy_values

                        temp += my_vals[0]

                    elif enemy_full < my_full:
                        if enemy_kings > 0:
                            enemy_full -= 1

                        temp = 0 - value - my_values + enemy_values

                        for i in range(my_full - enemy_full + 1):
                            if i >= len(my_vals):
                                 break
                            temp += my_vals[i]

                    if temp < best_capture:
                        best_capture = temp
                        changes.append(f"my piece taken {temp}")

            elif piece // 10 != self.color:
                score -= value

                match piece % 10:
                    case 1:
                        if self.color == 0:
                            score -= self.pawn_stages[self.game_stage][63 - index]
                            changes.append(-self.pawn_stages[self.game_stage][63-index])
                        else:
                            score -= self.pawn_stages[self.game_stage][index]
                            changes.append(-self.pawn_stages[self.game_stage][index])
                    case 2:
                        if self.color == 0:
                            score -= self.king_stages[self.game_stage][63 - index]
                            changes.append(-self.king_stages[self.game_stage][63-index])
                        else:
                            score -= self.king_stages[self.game_stage][index]
                            changes.append(-self.king_stages[self.game_stage][index])
                    case 3:
                        if self.color == 0:
                            score -= self.queen_stages[self.game_stage][63 - index]
                            changes.append(-self.queen_stages[self.game_stage][63-index])
                        else:
                            score -= self.queen_stages[self.game_stage][index]
                            changes.append(-self.queen_stages[self.game_stage][index])
                    case 4:
                        if self.color == 0:
                            score -= self.rook_stages[self.game_stage][63 - index]
                            changes.append(-self.rook_stages[self.game_stage][63-index])
                        else:
                            score -= self.rook_stages[self.game_stage][index]
                            changes.append(-self.rook_stages[self.game_stage][index])
                    case 5:
                        if self.color == 0:
                            score -= self.bishop_stages[self.game_stage][63 - index]
                            changes.append(-self.bishop_stages[self.game_stage][63-index])
                        else:
                            score -= self.bishop_stages[self.game_stage][index]
                            changes.append(-self.bishop_stages[self.game_stage][index])
                    case 6:
                        if self.color == 0:
                            score -= self.knight_stages[self.game_stage][63 - index]
                            changes.append(-self.knight_stages[self.game_stage][63-index])
                        else:
                            score -= self.knight_stages[self.game_stage][index]
                            changes.append(-self.knight_stages[self.game_stage][index])

                if piece % 10 == 2:
                    if my_attacks[index] > 0:
                        score += 0.5
                        changes.append("en check")

                    possible_moves = [index - self.num_of_rows - 1, index - self.num_of_rows, index - self.num_of_rows + 1,
                                      index - 1,                                                                 index + 1,
                                      index + self.num_of_rows - 1, index + self.num_of_rows, index + self.num_of_rows + 1]

                    moves_taken_by_me = 0
                    moves_taken_by_en = 0
                    moves_available = 0
                    moves_unavailable = 0
                    moves_controlled = 0

                    for move in possible_moves:
                        if move < 0 or move > 63:
                            moves_unavailable += 1
                        elif board[move] // 10 == self.color and board[move] != 0:
                            moves_taken_by_en += 1
                        elif board[move] // 10 != self.color and board[move] != 0:
                            moves_taken_by_me += 1
                        elif my_attacks[move] > 0:
                            moves_controlled += 1
                        elif board[move] == 0:
                            moves_available += 1

                    if moves_taken_by_me < (8 - moves_unavailable) / 4 or moves_taken_by_me > (8 - moves_unavailable) / 1.5:
                        score += 0.5
                        changes.append("en moves taken")

                    if moves_taken_by_en > 0:
                        score += 0.5
                        changes.append("en my taken")

                    if moves_available < 2:
                        score += 0.5
                        changes.append("en move amount")

                    if moves_controlled > (8 - moves_unavailable) / 4:
                        score += 0.5
                        changes.append("en controlled")

                if enemy_attacks[index] > 0 or my_attacks[index] > 0:
                    my_pawns = my_pawn_attacks[index]
                    my_threes = my_bishop_attacks[index] + my_knight_attacks[index]
                    my_rooks = my_rook_attacks[index]
                    my_queens = my_queen_attacks[index]
                    my_kings = my_king_attacks[index]
                    my_full = my_attacks[index]
                    my_values = my_pawns + my_threes * 3 + my_rooks * 5 + my_queens * 9

                    enemy_pawns = enemy_pawn_attacks[index]
                    enemy_threes = enemy_bishop_attacks[index] + enemy_knight_attacks[index]
                    enemy_rooks = enemy_rook_attacks[index]
                    enemy_queens = enemy_queen_attacks[index]
                    enemy_kings = enemy_king_attacks[index]
                    enemy_full = enemy_attacks[index]
                    enemy_values = enemy_pawns + enemy_threes * 3 + enemy_rooks * 5 + enemy_queens * 9

                    my_vals = []
                    enemy_vals = []

                    for i in range(my_kings):
                        my_vals.append(0)
                    for i in range(my_queens):
                        my_vals.append(9)
                    for i in range(my_rooks):
                        my_vals.append(5)
                    for i in range(my_threes):
                        my_vals.append(3)
                    for i in range(my_pawns):
                        my_vals.append(1)

                    for i in range(enemy_kings):
                        enemy_vals.append(0)
                    for i in range(enemy_queens):
                        enemy_vals.append(9)
                    for i in range(enemy_rooks):
                        enemy_vals.append(5)
                    for i in range(enemy_threes):
                        enemy_vals.append(3)
                    for i in range(enemy_pawns):
                        enemy_vals.append(1)

                    if my_kings > 0 and enemy_full >= my_full:
                        my_full -= 1

                    elif enemy_kings > 0 and enemy_full < my_full:
                        enemy_full -= 1

                    if my_full == 0 or not my_turn:
                        temp = best_capture
                
                    elif enemy_full == 0:
                        temp = value

                    elif enemy_full > my_full:
                        if my_kings > 0:
                            my_full -= 1

                        temp = 0 + value - my_values + enemy_values

                        for i in range(enemy_full - my_full + 1):
                            if i >= len(enemy_vals):
                                 break
                            temp -= enemy_vals[i]

                    elif enemy_full == my_full:
                        if my_kings > 0:
                            my_full -= 1

                        temp = 0 + value - my_values + enemy_values

                        if len(enemy_vals) > 0:
                            temp -= enemy_vals[0]

                    elif enemy_full < my_full:
                        if enemy_kings > 0:
                            enemy_full -= 1

                        temp = 0 + value - my_values + enemy_values

                        for i in range(my_full - enemy_full + 1):
                            if i >= len(my_vals):
                                 break
                            temp += my_vals[i]

                    if temp > best_capture:
                        best_capture = temp
                        changes.append(f"my piece taken {temp}")

        score += best_capture

        # print(changes)
        #
        # print(score)
        return score

    def process_move(self, board, pieces, piece, index, move, can_en_passant):
        temp_board = board.copy()
        temp_pieces = pieces.copy()

        # Taking the piece if possible
        if temp_board[move] != 0:
            temp_board[move] = 0
            temp_pieces[move] = None

        # En passant
        if piece.value % 10 == 1:
            # En passant to the right
            if temp_pieces[piece.index + 1] is not None and piece.color == temp_pieces[piece.index + 1].color:
                pass

            elif can_en_passant and temp_board[piece.index + 1] % 10 == 1 and index == piece.index + 1 - self.num_of_rows:
                temp_board[piece.index + 1] = 0
                temp_pieces[piece.index + 1] = None

            elif can_en_passant and temp_board[piece.index + 1] % 10 == 1 and index == piece.index + 1 + self.num_of_rows:
                temp_board[piece.index + 1] = 0
                temp_pieces[piece.index + 1] = None

            # En passant to the left
            elif temp_pieces[piece.index - 1] is not None and piece.color == temp_pieces[piece.index - 1].color:
                pass

            elif can_en_passant and temp_board[piece.index - 1] % 10 == 1 and index == piece.index - 1 - self.num_of_rows:
                temp_board[piece.index - 1] = 0
                temp_pieces[piece.index - 1] = None

            elif can_en_passant and temp_board[piece.index - 1] % 10 == 1 and index == piece.index - 1 + self.num_of_rows:
                temp_board[piece.index - 1] = 0
                temp_pieces[piece.index - 1] = None

            # Checking if can en passant
            if abs(index - piece.index) == 2 * self.num_of_rows:
                new_can_en_passant = True
            else:
                new_can_en_passant = False
        else:
            new_can_en_passant = False

        # Moving the rook if the king castled
        if piece.value % 10 == 2 and abs(piece.index - move) == 2:
            # White
            if piece.color == 0:
                # Short castle
                if piece.index < move:
                    temp_board = self.swap_in_list(temp_board, piece.index + 1, 63)
                    temp_pieces = self.swap_in_list(temp_pieces, piece.index + 1, 63)
                # Long castle
                if piece.index > move:
                    temp_board = self.swap_in_list(temp_board, piece.index - 1, 56)
                    temp_pieces = self.swap_in_list(temp_pieces, piece.index - 1, 56)
            # Black
            elif piece.color == 1:
                # Short castle
                if piece.index < move:
                    temp_board = self.swap_in_list(temp_board, piece.index + 1, 7)
                    temp_pieces = self.swap_in_list(temp_pieces, piece.index + 1, 7)
                # Long castle
                if piece.index > move:
                    temp_board = self.swap_in_list(temp_board, piece.index - 1, 0)
                    temp_pieces = self.swap_in_list(temp_pieces, piece.index - 1, 0)

        # Promoting the pawn into a queen
        if temp_board[index] == 1 and index < self.num_of_rows:
            temp_board[index] = 3
        elif temp_board[index] == 11 and index >= self.num_of_squares - self.num_of_rows:
            temp_board[index] = 13

        temp_board = self.swap_in_list(temp_board, index, move)
        temp_pieces = self.swap_in_list(temp_pieces, index, move)

        new_last_move = index

        return (temp_board, temp_pieces, new_last_move, new_can_en_passant)

    def get_own_attacks(self, pieces, board):
        pawn_attacks = []
        king_attacks = []
        queen_attacks = []
        rook_attacks = []
        bishop_attacks = []
        knight_attacks = []

        for i in range(64):
            pawn_attacks.append(0)
        for i in range(64):
            king_attacks.append(0)
        for i in range(64):
            queen_attacks.append(0)
        for i in range(64):
            rook_attacks.append(0)
        for i in range(64):
            bishop_attacks.append(0)
        for i in range(64):
            knight_attacks.append(0)

        for index, piece in enumerate(board):
            if piece // 10 != self.color or piece == 0:
                continue
            attacks = pieces[index].get_attacks(board, pieces, -1, -1, -1)
            match piece % 10:
                case 1:
                    for attack in attacks:
                        pawn_attacks[attack] += 1
                case 2:
                    for attack in attacks:
                        king_attacks[attack] += 1
                case 3:
                    for attack in attacks:
                        queen_attacks[attack] += 1
                case 4:
                    for attack in attacks:
                        rook_attacks[attack] += 1
                case 5:
                    for attack in attacks:
                        bishop_attacks[attack] += 1
                case 6:
                    for attack in attacks:
                        knight_attacks[attack] += 1
        return pawn_attacks, king_attacks, queen_attacks, rook_attacks, bishop_attacks, knight_attacks

    def get_enemy_attacks(self, pieces, board):
        pawn_attacks = []
        king_attacks = []
        queen_attacks = []
        rook_attacks = []
        bishop_attacks = []
        knight_attacks = []

        for i in range(64):
            pawn_attacks.append(0)
        for i in range(64):
            king_attacks.append(0)
        for i in range(64):
            queen_attacks.append(0)
        for i in range(64):
            rook_attacks.append(0)
        for i in range(64):
            bishop_attacks.append(0)
        for i in range(64):
            knight_attacks.append(0)

        for index, piece in enumerate(board):
            if piece // 10 == self.color or piece == 0:
                continue
            attacks = pieces[index].get_attacks(board, pieces, -1, -1, -1)
            match piece % 10:
                case 1:
                    for attack in attacks:
                        pawn_attacks[attack] += 1
                case 2:
                    for attack in attacks:
                        king_attacks[attack] += 1
                case 3:
                    for attack in attacks:
                        queen_attacks[attack] += 1
                case 4:
                    for attack in attacks:
                        rook_attacks[attack] += 1
                case 5:
                    for attack in attacks:
                        bishop_attacks[attack] += 1
                case 6:
                    for attack in attacks:
                        knight_attacks[attack] += 1
        return pawn_attacks, king_attacks, queen_attacks, rook_attacks, bishop_attacks, knight_attacks

    def print_board(self, board):
        if self.color == 0:
            board = board[::-1]
        for i, v in enumerate(board):
            if v < 10:
                print(" " + str(v), end=" ")
            else:
                print(v, end=" ")
            if i % 8 == 7:
                print()