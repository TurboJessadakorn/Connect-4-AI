from re import T
from turtle import Screen
import pygame
from tkinter import * 
from tkinter import messagebox
import sys
import os
import numpy as np
import math
import random
from numpy import ndarray
pygame.init()



#set screen sie
screen_h = 800
screen_w = 700
screen = pygame.display.set_mode([screen_w, screen_h], vsync=1)

#set front and BG
font = pygame.font.Font('Font.ttf', 80)
BG = pygame.image.load("Background.JPG")

#define color
red = [255,0,0]
yellow = [255,255,0]
green = [0,255,0]
blue = [0,0,255]
white = [255,255,255]
black = [0,0,0]

#variable
turn = 2    #player = 1, ai = 2
a = np.zeros((6,7), dtype= int)
x = 0 #cursor position
y = np.zeros((7))
y = y.astype(int)


#import key
from pygame.locals import (
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)
    #draw grid----------------------------------------------------------------------------------
def grid(turn) :
    
    pygame.draw.rect(screen,black,(0,0,700,100))
    pygame.draw.rect(screen,blue,(0,200,700,600))

    
    if turn == 2 :
        pygame.draw.circle(screen,yellow,(50,50),47)
        text = font.render("AI turn", True, white)
    else :
        pygame.draw.circle(screen,red,(50,50),47)      
        text = font.render("Your turn", True, white)
    screen.blit(text,(100,20))

    for i in range(6):
        for j in range(7):
            pygame.draw.circle(screen,white,(((j)*100)+50,(i*100)+250),45)
    pcir()
    pygame.display.flip() 
#--------------------------------------------------------------------------------------------
def aniM(posi,turn) : 
    screen.fill(white)
    #print("posi {}".format(posi))
    
    if turn == 2 :
        pygame.draw.circle(screen,yellow,((posi*100)+50,150),45)
    else :       
        pygame.draw.circle(screen,red,((posi*100)+50,150),45)
    grid(turn)
#--------------------------------------------------------------------------------------------
def aniD(posi,turn) :
    screen.fill(white)   
    #print("posi {}".format(posi))
    #print("y pos {}".format(y[posi]))
    for i in range(6-y[posi]):
        #print("i {}".format(i))
        grid(turn)
        if turn == 2 :
            pygame.draw.circle(screen,yellow,((posi*100)+50,(i*100)+250),45)
            #print("y {}".format((i*50)+125))
        else :       
            pygame.draw.circle(screen,red,((posi*100)+50,(i*100)+250),45)
            #print("y {}".format((i*50)+125))
        pygame.display.flip()
        pygame.time.wait(100)
    if turn == 2 :
        a[5 - y[posi]][posi] = 2
    else:
        a[5 - y[posi]][posi] = 1
    y[posi] += 1
#-------------------------------------------------------------------------------------------
def pcir():
    for xp in range(7):
        for yp in range(6):
            if a[yp][xp] == 1:
                pygame.draw.circle(screen,red,((xp*100)+50,((yp)*100)+250),45)
            elif a[yp][xp] == 2:
                pygame.draw.circle(screen,yellow,((xp*100)+50,((yp)*100)+250),45)   
#--------------------------------------------------------------------------------------------
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(7-3):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(7):
        for r in range(6-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(7-3):
        for r in range(6-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(7-3):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
def score_pos(board) :
    score = 0

    center_array = [int(i) for i in list(board[:, 7//2])]
    center_count = center_array.count(2)
    score += center_count * 3

    #Horizontal
    for row in range(6):
        for col in range(4):
            row_ar = np.ndarray.tolist(board[row][col:col+4])
            if row_ar.count(2) == 4:
                score += 100
            elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                score += 5
            elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                score += 2
            if row_ar.count(1) == 3 and row_ar.count(0) == 1:
                score -= 10
            #print("HZ : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
    #vertical
    tp_ar = board.transpose()
    for row in range(7):
        for col in range(3):   
            row_ar = np.ndarray.tolist(tp_ar[row][col:col+4])
            if row_ar.count(2) == 4:
                score += 100
            elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                score += 5
            elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                score += 2
            if row_ar.count(1) == 3 and row_ar.count(0) == 1:
                score -= 10
            #print("VT : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
    #Dia up
    for row in range(5,2,-1):
        for col in range(4):
            row_ar = board[row][col]
            for i in range(1,4):
                row_ar = np.append(row_ar, board[row-i][col+i] )
            row_ar = np.ndarray.tolist(row_ar)
            if row_ar.count(2) == 4:
                score += 100
            elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                score += 5
            elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                score += 2
            if row_ar.count(1) == 3 and row_ar.count(0) == 1:
                score -= 10
            #print("DU : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))

    #Dia down
    for row in range(3):
        for col in range(4):
            row_ar = board[row][col]
            for i in range(1,4):
                row_ar = np.append(row_ar, board[row+i][col+i] )
            row_ar = np.ndarray.tolist(row_ar)
            if row_ar.count(2) == 4:
                score += 100
            elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                score += 5
            elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                score += 2
            if row_ar.count(1) == 3 and row_ar.count(0) == 1:
                score -= 10
            #print("DD : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
    #print("y = {}".format(y))
    return score
def get_valid_locations(board):
    valid_locations = []
    for col in range(7):
        if is_valid_location(board, col):
            valid_locations.append(col)
    #print("col {} validlocation {}".format(col,valid_locations))
    return valid_locations

def is_valid_location(board, col):
    return board[0][col] == 0
# def get_next_open_row(board, col):
#     for r in range(6):
#         if board[r][col] == 0:
#             return r
def score_pos2(board) :
        score = 0

        center_array = [int(i) for i in list(board[:, 7//2])]
        center_count = center_array.count(2)
        score += center_count * 3

        #Horizontal
        for row in range(6):
            for col in range(4):
                row_ar = np.ndarray.tolist(board[row][col:col+4])
                if row_ar.count(2) == 4:
                    score += 100
                elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                    score += 5
                elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                    score += 2
                if row_ar.count(1) == 3 and row_ar.count(2) == 1:
                    score += 50
                print("HZ : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
        #vertical
        tp_ar = board.transpose()
        for row in range(7):
            for col in range(3):   
                row_ar = np.ndarray.tolist(tp_ar[row][col:col+4])
                if row_ar.count(2) == 4:
                    score += 100
                elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                    score += 5
                elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                    score += 2
                if row_ar.count(1) == 3 and row_ar.count(2) == 1:
                    score += 50
                print("VT : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
        #Dia up
        for row in range(5,2,-1):
            for col in range(4):
                row_ar = board[row][col]
                for i in range(1,4):
                    row_ar = np.append(row_ar, board[row-i][col+i] )
                row_ar = np.ndarray.tolist(row_ar)
                if row_ar.count(2) == 4:
                    score += 100
                elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                    score += 5
                elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                    score += 2
                if row_ar.count(1) == 3 and row_ar.count(2) == 1:
                    score += 50
                print("DU : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))

        #Dia down
        for row in range(3):
            for col in range(4):
                row_ar = board[row][col]
                for i in range(1,4):
                    row_ar = np.append(row_ar, board[row+i][col+i] )
                row_ar = np.ndarray.tolist(row_ar)
                if row_ar.count(2) == 4:
                    score += 100
                elif row_ar.count(2) == 3 and row_ar.count(0) == 1:
                    score += 5
                elif row_ar.count(2) == 2 and row_ar.count(0) == 2:
                    score += 2
                if row_ar.count(1) == 3 and row_ar.count(2) == 1:
                    score += 50
                print("DD : row {} col {} count = {} row_ar = {} score = {}".format(row,col,row_ar.count(2),row_ar,score))
        print("y = {}".format(y))
        return score
def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        temp_board = board.copy()
        temp_board[5-y[col]][col] = piece
        #print("temp_board")
        #print(temp_board)
        score = score_pos2(temp_board)
        #print("score = {}".format(score))
        if score > best_score:
            best_score = score
            best_col = col

    return best_col
def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_pos(board))
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = 2
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = 1
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
def get_next_open_row(board, col):
    for r in range(5,-1,-1):
        if board[r][col] == 0:
            return r

def end(board,turn) :
    if winning_move(board,turn) :
        won(turn)
    
#----------------------------------------------------------------------------------
def Normal():
    global turn
    global x
    global y
    print(y)
    print(a)
    running = True
    check = True
    logic = True
    pos = 0
    screen.fill(white)
    while running and check:
        pos = 0
        grid(turn)
        #print(turn)
        while turn == 2:
            score_pos(a)
            
            x_bot = pick_best_move(a, turn)
            print("r = {}".format(get_next_open_row(a,x_bot)))
            print("x_bot {}".format(x_bot))
            #print("x {}".format(x))
            aniM(x,turn)
            if x < x_bot :
                for i in range(x_bot - x):
                    x += 1
                    #print("x_bot <{}".format(x_bot))
                    #print("x {}".format(x))
                    pygame.time.wait(200)
                    aniM(x,turn)
            if x > x_bot :
                for i in range(x - x_bot):
                    x -= 1
                    #print("x_bot >{}".format(x_bot))
                    #print("x {}".format(x))
                    pygame.time.wait(200)
                    aniM(x,turn)
            pygame.time.wait(400)
            aniD(x,turn)
            end(a,turn)
            turn = 1
        
        print(a)
        print('=====================================================')
    #-----------------------------------------------------------------------------------------------

        while logic and turn != 2:
            pos = 0 
            grid(turn)      
            aniM(x,turn)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logic = False
                    running = False  
                if event.type == KEYDOWN :
                    if event.key == K_LEFT :
                        pos = 1
                    if event.key == K_DOWN :
                        pos = 2
                    if event.key == K_RIGHT :
                        pos = 3
                    if event.type == KEYUP :
                        if pos != 0 :
                            logic = False
            #print("key".format(pos))
            pygame.time.wait(100)
            if pos == 1:
                x = x-1
                if x <= -1 :
                    x = 6
            if pos == 3:
                x = x+1
                if x >= 7 :
                    x = 0
            if pos == 2 and y[x] < 6:
                aniD(x,turn)
                end(a,turn)
                turn = 2
               
        print(a)   





#----------------------------------------------------------------------------------
def Hard():
    global turn
    global x
    global y
    print(y)
    print(a)
    running = True
    check = True
    logic = True
    pos = 0
    screen.fill(white)
    while running and check:
        pos = 0
        grid(turn)
        #print(turn)
        while turn == 2:
            score_pos(a)
            
            x_bot, minimax_score = minimax(a, 5, -math.inf, math.inf, True)
            print("r = {}".format(get_next_open_row(a,x_bot)))
            print("x_bot {}".format(x_bot))
            #print("x {}".format(x))
            aniM(x,turn)
            if x < x_bot :
                for i in range(x_bot - x):
                    x += 1
                    #print("x_bot <{}".format(x_bot))
                    #print("x {}".format(x))
                    pygame.time.wait(200)
                    aniM(x,turn)
            if x > x_bot :
                for i in range(x - x_bot):
                    x -= 1
                    #print("x_bot >{}".format(x_bot))
                    #print("x {}".format(x))
                    pygame.time.wait(200)
                    aniM(x,turn)
            pygame.time.wait(400)
            aniD(x,turn)
            end(a,turn)
            turn = 1
        
        print(a)
        print('=====================================================')
    #-----------------------------------------------------------------------------------------------

        while logic and turn != 2:
            pos = 0 
            grid(turn)      
            aniM(x,turn)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logic = False
                    running = False  
                if event.type == KEYDOWN :
                    if event.key == K_LEFT :
                        pos = 1
                    if event.key == K_DOWN :
                        pos = 2
                    if event.key == K_RIGHT :
                        pos = 3
                    if event.type == KEYUP :
                        if pos != 0 :
                            logic = False
            #print("key".format(pos))
            pygame.time.wait(100)
            if pos == 1:
                x = x-1
                if x <= -1 :
                    x = 6
            if pos == 3:
                x = x+1
                if x >= 7 :
                    x = 0
            if pos == 2 and y[x] < 6 :
                aniD(x,turn)
                end(a,turn)
                turn = 2
                
        
        print(a)   

  
# # Done! Time to quit.
# pygame.quit()
# --------------------------------------------------------------------------------------------------------- \
def won(turn):
    
    while True:
        screen.blit(BG, (0, 0))
        WIN_MOUSE_POS = pygame.mouse.get_pos()
        if turn == 1:
            BACK_TEXT = get_font(160).render("You won!!!", True, "#b68f40")
        if turn == 2:
            BACK_TEXT = get_font(160).render("AI won!!!", True, "#b68f40")
        BACK_RECT = BACK_TEXT.get_rect(center=(350, 300))
        BACK_BUTTON = Button(image=None, pos=(350, 700), 
                            text_input="Back to Main menu", font= get_font(100), base_color="#E6AE17", hovering_color="White")
        screen.blit(BACK_TEXT, BACK_RECT)
        BACK_BUTTON.changeColor(WIN_MOUSE_POS)
        BACK_BUTTON.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(WIN_MOUSE_POS):
                    main_menu()
        pygame.display.update()


# --------------------------------------------------------------------------------------------------------- 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Font_2.ttf", size)

class Button():
  def __init__(self, image, pos, text_input, font, base_color, hovering_color):
    self.image = image
    self.x_pos = pos[0]
    self.y_pos = pos[1]
    self.font = font
    self.base_color, self.hovering_color = base_color, hovering_color
    self.text_input = text_input
    self.text = self.font.render(self.text_input, True, self.base_color)
    if self.image is None:
      self.image = self.text
    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

  def update(self, screen):
    if self.image is not None:
      screen.blit(self.image, self.rect)
    screen.blit(self.text, self.text_rect)

  def checkForInput(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      return True
    return False

  def changeColor(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      self.text = self.font.render(self.text_input, True, self.hovering_color)
    else:
      self.text = self.font.render(self.text_input, True, self.base_color)

# --------------------------------------------------------------------------------------------------------- 
def main_menu():
    global screen
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(160).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 160))

        PLAY_BUTTON = Button(image=None, pos=(350, 400), 
                            text_input="PLAY", font= get_font(120), base_color="#D19E14", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(350, 600), 
                            text_input="QUIT", font= get_font(120), base_color="#D19E14", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Level()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def Level():
    global screen
    global a
    global y
    global turn
    while True:
        screen.blit(BG, (0, 0))

        Level_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(160).render("difficulty", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 160))

        Mid_BUTTON = Button(image=None, pos=(350, 350), 
                            text_input="Normal", font= get_font(120), base_color="#D19E14", hovering_color="White")
        Hard_BUTTON = Button(image=None, pos=(350, 500), 
                            text_input="Hard", font= get_font(120), base_color="#D19E14", hovering_color="White")
        Main_BUTTON = Button(image=None, pos=(350, 725), 
                            text_input="Main menu", font= get_font(120), base_color="#D19E14", hovering_color="White")                    

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [Mid_BUTTON, Hard_BUTTON,Main_BUTTON]:
            button.changeColor(Level_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Mid_BUTTON.checkForInput(Level_MOUSE_POS):
                    a = np.zeros((6,7), dtype= int)
                    y = np.zeros((7), dtype = int)
                    turn = 2
                    print(a)
                    Normal()
                if Hard_BUTTON.checkForInput(Level_MOUSE_POS):
                    a = np.zeros((6,7), dtype= int)
                    y = np.zeros((7), dtype = int)
                    turn = 2
                    print(a)
                    Hard()
                if Main_BUTTON.checkForInput(Level_MOUSE_POS):
                    main_menu()

        pygame.display.update()
main_menu()