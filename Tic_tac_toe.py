from tkinter import *
import numpy as np
import random
layer_deep = 0
current_player = -1 #player code is 1 for "O" and -1 for "X"
players = (" ", "O", "X")
overflow = 0
layer_deep = 0

def tkinter2int(board_tk): #changes a tkinter board into a integer array
    board_int = np.empty((3,3), dtype = int) #places empty interger array
    for i in range(3): #populates integer array
        for j in range(3):
            for player_num in (-1, 0, 1):
                if board_tk[i,j]["text"] == players[player_num]:
                    board_int[i,j] = player_num
    return(board_int)

def if_win(board): #check for wins
    winner = None
    if np.count_nonzero(board == 0) == 0: #If all space is used, winner = 0
        winner = 0
    for i in (0, 1, 2): #cycles through (column, row, diagonal, diagonal) for winner
        if board[i, 0] == board[i, 1] and board[i, 1] == board[i, 2] and board[i, 0] != 0:
            winner = board[i, 0]
        if board[0, i] == board[1, i] and board[1, i] == board[2, i] and board[0, i] != 0:
            winner = board[0, i]
    if board[0, 0] == board[1, 1] and board[1, 1] == board[2, 2] and board[0, 0] != 0:
        winner = board[0, 0]
    if board[2, 0] == board[1, 1] and board[1, 1] == board[0, 2] and board[2, 0] != 0:
        winner = board[2, 0]
    return winner

def next_step(i, j): #determine what to do after a move is played
    global current_player
    board[i, j] = Label(root, text = players[current_player], width = 3)
    board[i, j].grid(row = i, column = j)
    #changed the unoccupied button into an occupied label
    winner = if_win(tkinter2int(board)) #checks for winners using if_win
    if winner == None: #print out the proper display
        display["text"] = players[-current_player] + " Plays"
        win = False
    else:
        if winner in (-1, 1): 
            display["text"] = players[winner] + " Wins"
        elif winner == 0:
            display["text"] = "You Tied"
        for i in range(3): #disables all buttons after a win
            for j in range(3):
                board[i,j]["state"] = "disable"
        win = True
    display.grid(row=3, column=0, columnspan=3)
    return win

def minimax(board, player_now):
    #Uses minimax algorithm to find bot move
    global layer_deep
    best_move = ()
    best_score = -2 * player_now
    winner = if_win(board)
    #print(f"layer:{layer_deep}", "\n")
    global overflow
    overflow += 1
    if overflow > 1000000:
        quit()
    if winner == None: #if no winner is found (tree does not end)
        for i in range(0,3): #cycles through branches
            for j in range(0, 3):
                if board[i, j] == 0:
                    board[i, j] = player_now
                    layer_deep += 1
                    score = minimax(board, -player_now)[0] #look for end in daughter branch
                    layer_deep -= 1
                    board[i, j] = 0
                    if (player_now == 1 and score > best_score) or (player_now == -1 and score < best_score): 
                        #find best move among daughter branches
                        best_score = score
                        best_move = (i, j)
    else: # if winner is found (tree ends)
        best_score = winner
        best_move = None
    return best_score, best_move

def tic_tac_toe(i_player, j_player):
    global current_player
    win = next_step(i_player, j_player)
    current_player = -current_player
    if not win:
        bot_move = minimax(tkinter2int(board), 1)[1]
        next_step(bot_move[0], bot_move[1])
        current_player = -current_player

root = Tk()
board = np.array( #set up the playing board
    [[Button(root, text = " ", command = lambda: tic_tac_toe(0,0)),
    Button(root, text = " ", command = lambda: tic_tac_toe(0,1)),
    Button(root, text = " ", command = lambda: tic_tac_toe(0,2))],
    [Button(root, text = " ", command = lambda: tic_tac_toe(1,0)),
    Button(root, text = " ", command = lambda: tic_tac_toe(1,1)),
    Button(root, text = " ", command = lambda: tic_tac_toe(1,2))],
    [Button(root, text = " ", command = lambda: tic_tac_toe(2,0)),
    Button(root, text = " ", command = lambda: tic_tac_toe(2,1)),
    Button(root, text = " ", command = lambda: tic_tac_toe(2,2))]]
)
display = Label(root, text = players[current_player] + " Plays") #set up the instruction display
display.grid(row=3, column=0, columnspan=3) #place the display
for i in range(3): #place the playing board
    for j in range(3):
        board[i,j].grid(row = i, column = j)
root.mainloop()