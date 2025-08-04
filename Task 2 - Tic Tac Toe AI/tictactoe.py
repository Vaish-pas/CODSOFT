import tkinter as tk
from tkinter import messagebox

# Creating the main window
root = tk.Tk()
root.title("Tic Tac Toe - AI vs You")
root.geometry("350x300")
root.resizable(False, False)

# Board and Buttons
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

# Checking Winner or Draw
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    for row in board:
        for cell in row:
            if cell == "":
                return None
    return "Draw"

# Minimax algorithm for AI logic
def minimax(is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

# AI move using Minimax
def ai_turn():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move:
        i, j = move
        board[i][j] = "O"
        buttons[i][j].config(text="O", state="disabled", disabledforeground="red")

# End the game with popup message
def end_game(winner):
    if winner == "X":
        messagebox.showinfo("Game Over", "🎉 Yay!! You Win!! Smarter than AI 😎")
    elif winner == "O":
        messagebox.showinfo("Game Over", "🤖 Oops!! AI Wins — Better luck next time!")
    else:
        messagebox.showinfo("Game Over", "🤝 It's a Draw!")
    root.quit()

# Player move (X)
def player_turn(row, col):
    if board[row][col] == "":
        buttons[row][col].config(text="X", state="disabled", disabledforeground="blue")
        board[row][col] = "X"
        result = check_winner()
        if result:
            end_game(result)
            return
        ai_turn()
        result = check_winner()
        if result:
            end_game(result)

# Create 3x3 button grid
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", width=10, height=4,
                                  font=("Helvetica", 14),
                                  command=lambda row=i, col=j: player_turn(row, col))
        buttons[i][j].grid(row=i, column=j)

# Start the game
root.mainloop()
