import numpy as np
import sys
import pygame
import math


Yellow = (255, 255, 0)
Red = (255, 0, 0)
Black = (0, 0, 0)
Blue = (0, 0, 255)

row_count = 6
column_count = 7


def create_board():
    """
    Creates an empty board with all cells initialized to 0.

    Returns:
        np.ndarray: An empty board with dimensions (row_count, column_count) and data type np.int64.
    """
    board = np.zeros((row_count, column_count))
    return board


def drop_piece(board, row, col, piece):
    """
    Drops a piece into the board at the specified location.

    Args:
        board (np.ndarray): The game board.
        row (int): The row index of the drop location.
        col (int): The column index of the drop location.
        piece (int): The value of the piece to be dropped (1 for player 1, 2 for player 2).

    Returns:
        None: None.

    Raises:
        ValueError: If the specified location is not a valid drop location.

"""
    board[row][col] = piece


def is_valid_location(board, col):
    """
    Checks if the specified column is a valid location to drop a piece.

    Args:
        board (np.ndarray): The game board.
        col (int): The column index of the location to be checked.

    Returns:
        bool: True if the specified column is a valid location, False otherwise.

    """
    return board[row_count-1][col] == 0


def get_next_open_row(board, col):
    """
    Returns the index of the next open row in the specified column,
    starting from the bottom of the board.

    Args:
        board (np.ndarray): The game board.
        col (int): The column index of the location to be checked.

    Returns:
        int: The index of the next open row in the specified column, or -1 if no open row exists.

    """
    for r in range(row_count):
        if board[r][col] == 0:
            return r


def print_board(board):
    """
    Prints the board to the console.

    Args:
        board (np.ndarray): The tic tac toe board to be printed.

    Returns:
        None: None.

    """
    print(np.flip(board, 0))


def winning_move(board, piece):
    """
    Checks if the specified board contains a winning move for the specified player.

    Args:
        board (np.ndarray): The game board.
        piece (int): The value of the player's piece (1 for player 1, 2 for player 2).

    Returns:
        bool: True if the specified player has a winning move, False otherwise.

    """
    #Check horizontal locations for win
    for c in range(column_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    
    #Check vertical locations for win
    for c in range(column_count):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            

    #Check positively sloped diagonal locations for win
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            

    #Check negatively sloped diagonal locations for wins
    for c in range(column_count-3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    """
    Draws the board on the screen.

    Args:
        board (np.ndarray): The tic tac toe board to be drawn.

    Returns:
        None: None.

    """
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, Blue, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, Black, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), radius)

    
    for c in range(column_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, Red, (int(c*SQUARESIZE+SQUARESIZE/2), height -int(r*SQUARESIZE+SQUARESIZE/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, Yellow, (int(c*SQUARESIZE+SQUARESIZE/2), height -int(r*SQUARESIZE+SQUARESIZE/2)), radius)

    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0


pygame.init()

SQUARESIZE = 100

width = column_count *SQUARESIZE
height = (row_count+1) * SQUARESIZE

size = (width, height)

radius = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

the_font = pygame.font.SysFont("chicago", 85)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            
            if turn == 0:
                pygame.draw.circle(screen, Red, (posx, int(SQUARESIZE/2)), radius)
            else:
                pygame.draw.circle(screen, Yellow, (posx, int(SQUARESIZE/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0, 0, width, SQUARESIZE))

            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = the_font.render("\t\tPlayer 1 wins!!!\t\t", 1, Red)
                        screen.blit(label, (40,10))
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2) 

                    if winning_move(board, 2):
                        label = the_font.render("\t\tPlayer 2 wins!!!\t\t", 1, Yellow)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn+=1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)