from abc import ABC, abstractmethod
import pygame
from .base_constants import BaseConstants as Cons  

class BaseBoard(ABC):
    
    def __init__(self):
        self.board = [[None for _ in range(Cons.COLS)] for _ in range(Cons.ROWS)]
        self.selected_piece = None
        self.highlight = []
    
    @abstractmethod
    def setup_initial_pieces(self):
        pass
    
    def draw_board(self, screen):
        screen.fill(Cons.BLACK)
        
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                # Draw checkerboard pattern
                if (row + col) % 2 == 1:
                    pygame.draw.rect(screen, Cons.ORANGE, 
                                   (col * Cons.SQUARE_SIZE, row * Cons.SQUARE_SIZE, 
                                    Cons.SQUARE_SIZE, Cons.SQUARE_SIZE))
                
                # Draw highlights
                if (row, col) in self.highlight:
                    pygame.draw.rect(screen, Cons.WHITE, 
                                   (col * Cons.SQUARE_SIZE, row * Cons.SQUARE_SIZE, 
                                    Cons.SQUARE_SIZE, Cons.SQUARE_SIZE))
                
                # Draw selection border
                if self.selected_piece == (row, col):
                    offset = Cons.SELECT_BORDER_OFFSET
                    size = Cons.SQUARE_SIZE - (2 * offset)
                    pygame.draw.rect(screen, Cons.SELECT, 
                                   (col * Cons.SQUARE_SIZE + offset, row * Cons.SQUARE_SIZE + offset, 
                                    Cons.SQUARE_SIZE - size, Cons.SQUARE_SIZE - size), Cons.SELECT_BORDER_WIDTH)
                
                # Draw pieces
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(screen)
    
    def get_piece(self, row, col):
        # Get piece at specified position
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        # Move piece from one position to another
        piece = self.board[from_row][from_col]
        if piece:
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            piece.move_to(to_row, to_col)
            return True
        return False
    
    def is_valid_position(self, row, col):
        # Check if position is within board bound
        return 0 <= row < Cons.ROWS and 0 <= col < Cons.COLS
    
    def is_empty(self, row, col):
        # Check if position is empty
        return self.is_valid_position(row, col) and self.board[row][col] is None
    
    # Highlight helper methods
    def clear_highlights(self):
        # Clear all highlighted squares
        self.highlight = []
    
    def add_highlight(self, row, col):
        # Add a square to highlights if valid
        if self.is_valid_position(row, col):
            if (row, col) not in self.highlight:
                self.highlight.append((row, col))
    
    def set_highlights(self, positions):
        # Set multiple highlights at once
        self.highlight = []
        for row, col in positions:
            self.add_highlight(row, col)
    
    # Selection helper methods
    def select_piece(self, row, col):
        # Select a piece at given position
        if self.is_valid_position(row, col) and self.board[row][col] is not None:
            self.selected_piece = (row, col)
            return True
        return False
    
    def clear_selection(self):
        # Clear piece selection
        self.selected_piece = None
    
    def get_selected_piece(self):
        # Get the currently selected piece
        if self.selected_piece:
            row, col = self.selected_piece
            return self.board[row][col]
        return None