import tkinter as tk

class TetrisGame:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=400, height=600)
        self.canvas.pack()

        self.board_size = 10
        self.field_width = 200
        self.field_height = int(0.7 * self.field_width / self.board_size)

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.game_over_label = tk.Label(self.root, text="")
        self.game_over_label.pack()

        self.field = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                row.append(0)
            self.field.append(row)

        self.figure = {
            "I": [[1, 1], [2, 2]],
            "J": [[1, 2, 3], [4]],
            "L": [[1, 2, 3], [4]],
            "O": [[1, 1], [2, 2]],
            "S": [[1, 2], [3, 4]],
            "T": [[1, 2, 3], [4]],
            "Z": [[1, 2], [3, 4]]
        }

        self.figure_name = random.choice(list(self.figure.keys()))
        self.figure_coords = self.figure[self.figure_name]

        self.draw_field()
        self.update()

    def draw_field(self):
        self.canvas.delete("all")
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.field[i][j] == 1:
                    self.canvas.create_rectangle(j * self.field_width / self.board_size,
                                                  i * self.field_height / self.board_size,
                                                  (j + 1) * self.field_width / self.board_size,
                                                  (i + 1) * self.field_height / self.board_size, fill="#000000")
        for i in range(len(self.figure_coords)):
            for j in range(len(self.figure_coords[i])):
                if self.figure_coords[i][j] == 1:
                    x = (self.figure_name == "I" and j) or ((self.figure_name == "J" or self.figure_name == "L" or self.figure_name == "T") and i) or (
                            self.figure_name == "O" and len(self.figure_coords) // 2 + i == j) or (
                                (self.figure_name == "S" or self.figure_name == "Z") and i < len(self.figure_coords) // 2)
                    y = (self.figure_name == "I" and j) or ((self.figure_name == "J" or self.figure_name == "L" or self.figure_name == "T") and i) or (
                            self.figure_name == "O" and len(self.figure_coords[i]) - j == len(self.figure_coords) // 2) or (
                                (self.figure_name == "S" or self.figure_name == "Z") and j < len(self.figure_coords) // 2)
                    self.canvas.create_rectangle(x * self.field_width / self.board_size,
                                                  y * self.field_height / self.board_size,
                                                  (x + 1) * self.field_width / self.board_size,
                                                  (y + 1) * self.field_height / self.board_size, fill="#0000ff")
        self.score_label.config(text=f"Score: {self.get_score()}")

    def update(self):
        self.root.after(1000, self.drop_figure)

    def drop_figure(self):
        for i in range(len(self.figure_coords)):
            if self.figure_name == "I":
                x = len(self.figure_coords) // 2 + random.randint(-1, 1)
                y = int(len(self.figure_coords) / 2) - 1
                while self.field[y][x] != 0:
                    y += 1
                for j in range(i):
                    self.field[y - i + j][self.figure_name == "I" and x or (i == len(self.figure_coords) // 2)] = 1
            elif self.figure_name == "J":
                x = len(self.figure_coords) // 2 + random.randint(-1, 0)
                y = int(len(self.figure_coords)) - i
                while self.field[y][x] != 0:
                    y += 1
                for j in range(i):
                    self.field[y - i + j][self.figure_name == "J" and x or (j < len(self.figure_coords) // 2)] = 1
            elif self.figure_name == "L":
                x = len(self.figure_coords) // 2 + random.randint(-1, 0)
                y = int(len(self.figure_coords)) - i
                while self.field[y][x] !=
