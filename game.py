from tkinter import *
from pieces.pawn import Pawn
from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from square import Square

class Game:
    def __init__(self):
        # Making the window
        self.tk = Tk()
        self.tk.title("Szachy")
        self.tk.resizable(False, False)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=1000, height=1000, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        # Binding the mouse and keyboard
        self.tk.bind("<Button-1>", self.mouse_button_pressed)
        self.tk.bind("<Escape>", self.quit)

        # Defining constants
        self.num_of_rows = 8
        self.num_of_squares = self.num_of_rows ** 2
        self.square_size = self.canvas.winfo_width() / self.num_of_rows

        # Defining variables
        self.selected_piece = None
        self.whose_turn = True # True - White, False - Black

        # Defining booleans

        self.end_of_game = False

        self.can_en_passant = False

        self.white_can_short_castle = True
        self.white_can_long_castle = True

        self.black_can_short_castle = True
        self.black_can_long_castle = True

        self.white_in_check = False
        self.black_in_check = False

        # Defining lists
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

        self.pieces = []
        self.squares = []

    def main(self):
        while True:
            if self.end_of_game:
                break

            self.tk.update_idletasks()
            self.tk.update()

    def mouse_button_pressed(self, event):
        index = int(event.x // self.square_size + self.num_of_rows * (event.y // self.square_size))
        self.clicked_value = self.board[index]

        if self.selected_piece is None and self.clicked_value == 0:
            return

        # Moving the piece, taking others and castling
        if self.selected_piece is not None and self.clicked_value >= 100 and self.selected_piece.index != index:
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
            self.update_lists(index, self.selected_piece.index)

            # Promoting the pawn into a queen
            if self.board[index] % 100 == 1 and index < self.num_of_rows:
                self.board[index] = 3
            elif self.board[index] % 100 == 11 and index >= self.num_of_squares - self.num_of_rows:
                self.board[index] = 13

            self.selected_piece = None
            self.deselect_all()
            self.draw()
            self.black_attacks, self.white_attacks = self.reset_attacks(self.pieces, self.board)

            # Checking if white is in check
            if self.black_attacks[self.board.index(2)] != 0:
                self.white_in_check = True
            elif self.black_attacks[self.board.index(2)] == 0:
                self.white_in_check = False

            # Checking if black is in check
            elif self.white_attacks[self.board.index(12)] != 0:
                self.black_in_check = True
            elif self.white_attacks[self.board.index(12)] == 0:
                self.black_in_check = False
            return

        # Deselecting the pieces
        if self.pieces[index] is None:
            self.deselect_all()
            self.draw()
            return

        # Selecting the piece
        if self.whose_turn and self.pieces[index].color == 0:
            self.deselect_all()
            self.pieces[index].select()
            self.selected_piece = self.pieces[index]
            self.draw()
        elif not self.whose_turn and self.pieces[index].color == 1:
            self.deselect_all()
            self.pieces[index].select()
            self.selected_piece = self.pieces[index]
            self.draw()

    def swap_in_list(self, list, a, b):
        if a == b: return
        if a > b: a, b = b, a
        return list[:a] + list[b:b+1] + list[a+1:b] + list[a:a+1] + list[b+1:]

    def update_lists(self, a, b):
        self.pieces = self.swap_in_list(self.pieces, a, b)
        self.board = self.swap_in_list(self.board, a, b)

    def draw(self):
        # Deleting the drawings
        self.canvas.delete("all")

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
        for i, v in enumerate(self.board):
            piece = None
            square = Square(self, self.square_size, i, v)
            self.squares.append(square)
            
            match v % 10:
                case 1:
                    piece = Pawn(self, i, v)
                case 2:
                    piece = King(self, i, v)
                case 3:
                    piece = Queen(self, i, v)
                case 4:
                    piece = Rook(self, i, v)
                case 5:
                    piece = Bishop(self, i, v)
                case 6:
                    piece = Knight(self, i, v)

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

    def deselect_all(self):
        for i, v in enumerate(self.board):
            self.board[i] = v % 100

    def quit(self, event):
        self.end_of_game = True