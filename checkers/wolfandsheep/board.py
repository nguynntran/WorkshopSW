import pygame
from ..base_classes.base_board import BaseBoard
from ..base_classes.base_constants import BaseConstants as Cons
from .constant import WASCons
from .pieces import WolfPiece, SheepPiece

class Board(BaseBoard):
    def __init__(self):
        super().__init__()
        self.setup_initial_pieces()
    
    def setup_initial_pieces(self):
        """Setup initial pieces for wolves and sheep game"""
        # Place wolves on top row at dark squares
        for col in [1, 3, 5, 7]:
            self.board[0][col] = WolfPiece(0, col)
        
        # Place sheep at bottom-left dark square
        self.board[7][0] = SheepPiece(7, 0)