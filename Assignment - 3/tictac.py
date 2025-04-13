from tkinter import *
import numpy as np

size_of_board = 800
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'
bg_color = 'black'


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg=bg_color)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        self.winning_line_coords = None

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        self.canvas.delete("all")
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0,
                                    (i + 1) * size_of_board / 3, size_of_board,
                                    fill="white")
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3,
                                    size_of_board, (i + 1) * size_of_board / 3,
                                    fill="white")

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        self.winning_line_coords = None
        self.X_wins = self.O_wins = self.tie = self.reset_board = False

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)

    def draw_winning_line(self):
        if self.winning_line_coords:
            start_logical, end_logical = self.winning_line_coords
            start_pixel = self.convert_logical_to_grid_position(start_logical)
            end_pixel = self.convert_logical_to_grid_position(end_logical)
            color = symbol_X_color if self.X_wins else symbol_O_color
            self.canvas.create_line(start_pixel[0], start_pixel[1],
                                    end_pixel[0], end_pixel[1],
                                    fill=color, width=symbol_thickness // 2)

    def draw_board_symbols(self):
        for i in range(3):
            for j in range(3):
                if self.board_status[i][j] == -1:
                    self.draw_X((i, j))
                elif self.board_status[i][j] == 1:
                    self.draw_O((i, j))

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        value = -1 if player == 'X' else 1

        for i in range(3):
            if all(self.board_status[i, :] == value):
                self.winning_line_coords = ((i, 0), (i, 2))
                return True
            if all(self.board_status[:, i] == value):
                self.winning_line_coords = ((0, i), (2, i))
                return True

        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == value:
            self.winning_line_coords = ((0, 0), (2, 2))
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == value:
            self.winning_line_coords = ((0, 2), (2, 0))
            return True

        return False

    def is_tie(self):
        return not np.any(self.board_status == 0)

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')
        if not self.O_wins:
            self.tie = self.is_tie()
        return self.X_wins or self.O_wins or self.tie

    def display_gameover(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.draw_board_symbols()
        self.draw_winning_line()
        self.canvas.update()
        self.window.after(2000, self.show_final_result)

    def show_final_result(self):
        self.canvas.delete("all")
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'It\'s a tie'
            color = 'gray'

        self.canvas.create_text(size_of_board / 2, size_of_board / 3,
                                font="cmr 60 bold", fill=color, text=text)

        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8,
                                font="cmr 40 bold", fill="white", text='Scores')

        score_text = f'Player 1 (X) : {self.X_score}\n'
        score_text += f'Player 2 (O): {self.O_score}\n'
        score_text += f'Tie                    : {self.tie_score}'

        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4,
                                font="cmr 30 bold", fill=Green_color, text=score_text)

        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16,
                                font="cmr 20 bold", fill="gray",
                                text='Click anywhere to play again')

        self.reset_board = True

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if not self.is_grid_occupied(logical_position):
                if self.player_X_turns:
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                else:
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                self.player_X_turns = not self.player_X_turns

                if self.is_gameover():
                    self.display_gameover()
        else:
            self.play_again()


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
