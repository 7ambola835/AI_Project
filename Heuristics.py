import numpy as np
import tkinter as tk
import pygame
from tkinter import font


pygame.init()

# Sound effects
win_sound = pygame.mixer.Sound("Sounds/win.wav")
lose_sound = pygame.mixer.Sound("Sounds/lose.wav")
move_Player_sound = pygame.mixer.Sound("Sounds/move_player.wav")
move_AI_sound = pygame.mixer.Sound("Sounds/move_ai.wav")
intro_sound = pygame.mixer.Sound("Sounds/intro.wav")
Again_sound = pygame.mixer.Sound("Sounds/again.wav")

# Constants variables for game
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
player_wins = 0
ai_wins = 0

intro_sound.play()

def check_winner(board):
    for row in board:
        if all(cell == PLAYER_X for cell in row):
            return PLAYER_X
        elif all(cell == PLAYER_O for cell in row):
            return PLAYER_O
    for col in np.transpose(board):
        if all(cell == PLAYER_X for cell in col):
            return PLAYER_X
        elif all(cell == PLAYER_O for cell in col):
            return PLAYER_O
    diagonals = [np.diag(board), np.diag(np.fliplr(board))]
    for diagonal in diagonals:
        if all(cell == PLAYER_X for cell in diagonal):
            return PLAYER_X
        elif all(cell == PLAYER_O for cell in diagonal):
            return PLAYER_O
    return None

def check_draw(board):
    return all(cell != EMPTY for row in board for cell in row)

def available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def evaluate_board(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    score = 0
    lines = [
        [board[i][0], board[i][1], board[i][2]] for i in range(3)
    ] + [
        [board[0][i], board[1][i], board[2][i]] for i in range(3)
    ] + [
        [board[i][i] for i in range(3)],
        [board[i][2-i] for i in range(3)]
    ]

    for line in lines:
        if line.count(player) == 2 and line.count(EMPTY) == 1:
            score += 10
        if line.count(opponent) == 2 and line.count(EMPTY) == 1:
            score -= 10

    return score

def minimax(board, depth, maximizing_player):
    winner = check_winner(board)
    if winner is not None:
        return winner * 1000  # Big number for a win/lose
    elif check_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = PLAYER_X
            eval = minimax(board, depth + 1, False)
            board[move[0]][move[1]] = EMPTY
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = PLAYER_O
            eval = minimax(board, depth + 1, True)
            board[move[0]][move[1]] = EMPTY
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    best_eval = float('-inf') if player == PLAYER_X else float('inf')
    best_move = None
    for move in available_moves(board):
        board[move[0]][move[1]] = player
        eval = evaluate_board(board, player) + minimax(board, 0, player == PLAYER_O)
        board[move[0]][move[1]] = EMPTY
        if (player == PLAYER_X and eval > best_eval) or (player == PLAYER_O and eval < best_eval):
            best_eval = eval
            best_move = move
    return best_move

def ai_move():
    move = best_move(board, PLAYER_O)
    board[move[0]][move[1]] = PLAYER_O
    buttons[move[0]][move[1]].config(text="O", state=tk.DISABLED)
    move_AI_sound.play()
    check_game_over()

def player_move(i, j):
    global current_player
    if board[i][j] == EMPTY and not game_over:
        board[i][j] = PLAYER_X
        buttons[i][j].config(text="X", state=tk.DISABLED)
        move_Player_sound.play()
        check_game_over()
        if not game_over:
            ai_move()

def check_game_over():
    global game_over
    winner = check_winner(board)
    if winner is not None:
        game_over = True
        disable_buttons()
        update_status("Player X wins!" if winner == PLAYER_X else "AI wins!")
    elif check_draw(board):
        game_over = True
        disable_buttons()
        update_status("No one won! Try again")

def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)

def update_status(message):
    status_label.config(text=message)

def update_win_history():
    history_window = tk.Toplevel(root)
    history_window.title("Win History")

    #Display player and AI win counts
    player_label = tk.Label(history_window, text=f"Player: {player_wins}", font=('Arial', 12))
    player_label.pack()

    ai_label = tk.Label(history_window, text=f"AI: {ai_wins}", font=('Arial', 12))
    ai_label.pack()
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
# GUI
root = tk.Tk()
root.title("Tic Tac Toe Heuristic")
root.configure(bg='#300000')
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
                        fg='white')
status_label.grid(row=0, columnspan=3, pady=(20, 10))

reset_button = tk.Button(root, text="Reset", font=('Arial', 16), bg='black', fg='white', command=reset_game)
reset_button.grid(row=4, columnspan=3, pady=10)

new_game_button = tk.Button(root, text="New Game", font=('Arial', 16), bg='black', fg='white', command=new_game)
new_game_button.grid(row=0, column=2, pady=(20, 10), padx=10, sticky="e")

history_button = tk.Button(root, text="History", font=('Arial', 16), bg='black', fg='white', command=update_win_history)
history_button.grid(row=0, column=0, pady=(20, 10), padx=10, sticky="w")
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
current_player = PLAYER_X
game_over = False

root.mainloop()
pygame.quit()

