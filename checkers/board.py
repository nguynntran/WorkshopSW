import pygame
from .constant import Cons
from .pieces import Piece

class Board:
    def __init__(self):
        self.board = [[None for _ in range(Cons.COLS)] for _ in range(Cons.ROWS)]
        self.selected_piece = None
        self.highlight = []

        # Place wolves
        for col in [1, 3, 5, 7]:
            self.board[0][col] = Piece(Cons.WOLF, 0, col)
        # Place sheep 
        self.board[7][0] = Piece(Cons.SHEEP, 7, 0)
    
    def draw_board(self, screen):
        screen.fill(Cons.BLACK)
        
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                # Draw dark squares (checkerboard pattern)
                if (row + col) % 2 == 1:
                    pygame.draw.rect(screen, Cons.ORANGE, 
                                   (col * Cons.SQUARE_SIZE, row * Cons.SQUARE_SIZE, 
                                    Cons.SQUARE_SIZE, Cons.SQUARE_SIZE))
                # Highlight for legal moves
                if self.selected_piece == (row, col):
                    pygame.draw.rect(screen, Cons.SELECT, 
                                   (col * Cons.SQUARE_SIZE + 4, row * Cons.SQUARE_SIZE + 4, 
                                    Cons.SQUARE_SIZE - 8, Cons.SQUARE_SIZE - 8), 3)


                if self.selected_piece == (row, col):
                    pygame.draw.rect(screen, Cons.SELECT, 
                                   (col * Cons.SQUARE_SIZE + 4, row * Cons.SQUARE_SIZE + 4, 
                                    Cons.SQUARE_SIZE - 8, Cons.SQUARE_SIZE - 8), 3)


                # Draw pieces
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(screen)
    
    