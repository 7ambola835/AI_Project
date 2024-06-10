import numpy as np
import tkinter as tk
from tkinter import font
import ctypes
import pygame
pygame.init()

win_sound = pygame.mixer.Sound("Sounds/win.wav")
lose_sound = pygame.mixer.Sound("Sounds/Lose.wav")
move_Player_sound = pygame.mixer.Sound("Sounds/Move_Player.wav")
move_AI_sound = pygame.mixer.Sound("Sounds/Move_AI.wav")
intro_sound = pygame.mixer.Sound("Sounds/Intro.wav")
Again_sound = pygame.mixer.Sound("Sounds/Again.wav")


# Constants variables for game
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
player_wins = 0
ai_wins = 0

intro_sound.play()

#Logic
def check_winner(board):
    # Check rows
    for row in board:
        if all([cell == PLAYER_X for cell in row]):
            return PLAYER_X
        elif all([cell == PLAYER_O for cell in row]):
            return PLAYER_O
    # check columns
    for col in np.transpose(board):
        if all([cell == PLAYER_X for cell in col]):
            return PLAYER_X
        elif all([cell == PLAYER_O for cell in col]):
            return PLAYER_O
    # check diagonals
    diagonals = [np.diag(board), np.diag(np.fliplr(board))]
    for diagonal in diagonals:
        if all([cell == PLAYER_X for cell in diagonal]):
            return PLAYER_X
        elif all([cell == PLAYER_O for cell in diagonal]):
            return PLAYER_O

    return None


def check_draw(board):
    return all([cell != EMPTY for row in board for cell in row])


def available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]


#Minimax Algorithm
def minimax(board, depth, maximizing_player):
    winner = check_winner(board)
    if winner is not None:
        return winner * (10 - depth)  # Adjust score based on depth
    elif check_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            i, j = move
            board[i][j] = PLAYER_X
            eval = minimax(board, depth + 1, False)
            board[i][j] = EMPTY
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            i, j = move
            board[i][j] = PLAYER_O
            eval = minimax(board, depth + 1, True)
            board[i][j] = EMPTY
            min_eval = min(min_eval, eval)
        return min_eval


def best_move(board):
    best_score = float('-inf')
    best_move = None
    for move in available_moves(board):
        i, j = move
        board[i][j] = PLAYER_X
        score = minimax(board, 0, False)
        board[i][j] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def player_move(row, col):
    global current_player, board, player_wins, ai_wins
    if board[row][col] == EMPTY and not game_over:
        board[row][col] = current_player
        move_Player_sound.play()
        if current_player == PLAYER_X:
            buttons[row][col].config(text="X", state=tk.DISABLED)
            current_player = PLAYER_O
        else:
            buttons[row][col].config(text="O", state=tk.DISABLED)
            current_player = PLAYER_X

        winner = check_winner(board)
        if winner is not None:
            if winner == PLAYER_X:
                status_label.config(text="Player X wins!")
                win_sound.play()

            else:
                status_label.config(text="Player O wins!")
                lose_sound.play()
            disable_buttons()
            update_win_counters(winner)
        elif check_draw(board):
            status_label.config(text="No one won, Try again!")
            Again_sound.play()
            disable_buttons()
        else:
            status_label.config(text="Player " + ("X" if current_player == PLAYER_X else "O") + "'s turn")

        if current_player == PLAYER_O and not game_over:
            ai_move()


def ai_move():
    global current_player, board, player_wins, ai_wins
    if not game_over:
        move = best_move(board)
        row, col = move
        board[row][col] = current_player
        move_AI_sound.play()
        buttons[row][col].config(text="O", state=tk.DISABLED)
        current_player = PLAYER_X
        winner = check_winner(board)
        if winner is not None:
            if winner == PLAYER_X:
                status_label.config(text="Human wins!")
                win_sound.play()
                player_wins+=1
            else:
                status_label.config(text="Ai wins!")
                lose_sound.play()
                ai_wins+=1
            disable_buttons()
        elif check_draw(board):
            status_label.config(text="No one wins, Try again!")
            Again_sound.play()
            disable_buttons()
        else:
            status_label.config(text="Player " + ("X" if current_player == PLAYER_X else "O") + "'s turn")

# Update win counters
def update_win_counters(winner):
    global player_wins, ai_wins
    if winner == PLAYER_X:
        player_wins += 1
    elif winner == PLAYER_O:
        ai_wins += 1

    # Update win history display
    update_win_history()
def update_win_history():
    history_window = tk.Toplevel(root)
    history_window.title("Win History")

    # Display player and AI win counts
    player_label = tk.Label(history_window, text=f"Player: {player_wins}", font=('Arial', 12))
    player_label.pack()

    ai_label = tk.Label(history_window, text=f"AI: {ai_wins}", font=('Arial', 12))
    ai_label.pack()
def disable_buttons():
    global game_over
    game_over = True
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)


def reset_game():
    global board, current_player, game_over
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    current_player = PLAYER_X
    game_over = False
    status_label.config(text="Player X's turn")
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state=tk.NORMAL)
    global player_wins, ai_wins
    player_wins = 0
    ai_wins = 0
    update_win_history()
def new_game():
    global board, current_player, game_over
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    current_player = PLAYER_X
    game_over = False
    status_label.config(text="Player X's turn")
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state=tk.NORMAL)




#GUI
root = tk.Tk()
root.title("Tic Tac Toe Minimax")
root.configure(bg='#002200')
root.geometry("490x640")  # Size of the window

button_font = font.Font(family='Helvetica', size=18)  # Size for buttons

buttons = [[None, None, None],
           [None, None, None],
           [None, None, None]]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, width=10, height=5, font=button_font, bd=0, highlightthickness=0, bg='black',
                                  fg='green',
                                  activebackground='gray15', activeforeground='green',
                                  command=lambda row=i, col=j: player_move(row, col))
        buttons[i][j].grid(row=i + 1, column=j, padx=10, pady=10)

status_label = tk.Label(root, text="Player X's turn", font=('Arial', 18), bg='gray10',
                        fg='white')  #Size for the label
status_label.grid(row=0, columnspan=3, pady=(20, 10))

reset_button = tk.Button(root, text="Reset", font=('Arial', 16), bg='black', fg='white', command=reset_game)
reset_button.grid(row=4, columnspan=3, pady=10)

new_game_button = tk.Button(root, text="New Game", font=('Arial', 16), bg='black', fg='white', command=new_game)
new_game_button.grid(row=0, column=2, pady=(20, 10), padx=10, sticky="e")

history_button = tk.Button(root, text="History", font=('Arial', 16), bg='black', fg='white', command=update_win_history)
history_button.grid(row=0, column=0, pady=(20, 10), padx=10, sticky="w")
# Game variables
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
current_player = PLAYER_X
game_over = False

root.mainloop()
pygame.quit()





