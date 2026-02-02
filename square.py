class Square:
    def __init__(self, game, size, index, value):
        self.game = game

        self.size = size

        self.index = index
        self.value = value

        self.x = self.index % self.game.num_of_rows * self.size
        self.y = self.index // self.game.num_of_rows * self.size

        self.get_color()
        self.draw()

    def draw(self):
        self.square = self.game.canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill = self.color)

    def get_color(self):
        if self.value >= 100:
            self.color = "lightblue"
            return

        if self.index % 2 == 0 and self.index // self.game.num_of_rows % 2 == 1 or self.index % 2 == 1 and self.index // self.game.num_of_rows % 2 == 0:
            self.color = "grey"
        else:
            self.color = "white"