import random
import tkinter as tk
from tkinter import messagebox

class Minesweeper:
    def __init__(self, root, size=10, mines=10):
        self.root = root
        self.size = size
        self.mines = mines
        self.buttons = {}
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()
        self.game_over = False

        self.init_board()
        self.place_mines()
        self.calculate_numbers()

    def init_board(self):
        for x in range(self.size):
            for y in range(self.size):
                btn = tk.Button(self.root, width=2, height=1, command=lambda x=x, y=y: self.on_click(x, y))
                btn.grid(row=x, column=y)
                self.buttons[(x, y)] = btn

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) not in self.mine_positions:
                self.mine_positions.add((x, y))
                self.board[x][y] = -1

    def calculate_numbers(self):
        for x, y in self.mine_positions:
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if self.board[i][j] != -1:
                        self.board[i][j] += 1

    def on_click(self, x, y):
        if self.game_over:
            return

        if (x, y) in self.mine_positions:
            self.game_over = True
            self.reveal_board()
            messagebox.showinfo("Game Over", "You hit a mine!")
        else:
            self.reveal_tile(x, y)
            if self.check_win():
                self.game_over = True
                self.reveal_board()
                messagebox.showinfo("Congratulations", "You won!")

    def reveal_tile(self, x, y):
        if self.buttons[(x, y)]["state"] == "disabled":
            return

        self.buttons[(x, y)].config(text=str(self.board[x][y]) if self.board[x][y] > 0 else "", state="disabled")

        if self.board[x][y] == 0:
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if (i, j) != (x, y):
                        self.reveal_tile(i, j)

    def reveal_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) in self.mine_positions:
                    self.buttons[(x, y)].config(text="*", bg="red")
                else:
                    self.buttons[(x, y)].config(text=str(self.board[x][y]) if self.board[x][y] > 0 else "", state="disabled")

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) not in self.mine_positions and self.buttons[(x, y)]["state"] != "disabled":
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root, size=10, mines=15)
    root.mainloop()
