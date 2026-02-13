from abc import ABC, abstractmethod
import pygame
from .base_constants import BaseConstants as Cons

class BasePiece(ABC):
    """Abstract base class for all game pieces"""
    
    def __init__(self, piece_type, row, col, color):
        self.type = piece_type
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def get_legals_moves(self, board):
        pass
    
    def move_to(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
    
    def get_position(self):
        return (self.row, self.col)
    
    def get_center(self):
        return (
            self.col * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2,
            self.row * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2
        )
    def _is_val_pos(self, board, row, col):
        # Method to validate position
        return (0 <= row < Cons.ROWS and 
                0 <= col < Cons.COLS and 
                board[row][col] is None and 
                (row + col) % 2 == 1)
    
    def _get_moves_in_directions(self, board, directions):
        # Helper to get moves in specified directions
        moves = []
        for drow, dcol in directions:
            nrow, ncol = self.row + drow, self.col + dcol
            if self._is_val_pos(board, nrow, ncol):
                moves.append((nrow, ncol))
        return moves