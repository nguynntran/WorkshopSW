import pygame
from .constant import Cons
from .pieces import Piece

class Board:
    def __init__(self):
        self.board = [[None for _ in range(Cons.COLS)] for _ in range(Cons.ROWS)]
    
        # Place wolves on top row
        for col in [1, 3, 5, 7]:
            self.board[0][col] = Piece(Cons.WOLF, 0, col)
        # Place sheep on bottom row
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
                
                # Draw pieces
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(screen)
    
    def get_piece(self, row, col):
        """Get piece at specified position"""
        if 0 <= row < Cons.ROWS and 0 <= col < Cons.COLS:
            return self.board[row][col]
        return None
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < Cons.ROWS and 0 <= col < Cons.COLS
    
    def is_empty(self, row, col):
        """Check if position is empty"""
        return self.is_valid_position(row, col) and self.board[row][col] is None