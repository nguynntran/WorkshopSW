import pygame
from ..base_classes.base_pieces import BasePiece
from ..base_classes.base_constants import BaseConstants as Cons
from .constant import WASCons

class WolfPiece(BasePiece):
    def __init__(self, row, col):
        super().__init__(WASCons.WOLF, row, col, WASCons.WOLF_COLOR)
    
    def draw(self, screen):
        center = self.get_center()
        radius = Cons.SQUARE_SIZE // 2 - 10
        
        pygame.draw.circle(screen, Cons.BLACK, (center[0] + 3, center[1] + 3), radius)
        pygame.draw.circle(screen, self.color, center, radius)
        pygame.draw.circle(screen, Cons.BLACK, center, radius, 3)
    
    def get_legals_moves(self, board):
        return self._get_moves_in_directions(board, [(1, -1), (1, 1)])

class SheepPiece(BasePiece):
    def __init__(self, row, col):
        super().__init__(WASCons.SHEEP, row, col, WASCons.SHEEP_COLOR)
    
    def draw(self, screen):
        center = self.get_center()
        radius = Cons.SQUARE_SIZE // 2 - 10
        
        pygame.draw.circle(screen, Cons.BLACK, (center[0] + 3, center[1] + 3), radius)
        pygame.draw.circle(screen, self.color, center, radius)
        pygame.draw.circle(screen, Cons.BLACK, center, radius, 2)
    
    def get_legals_moves(self, board):
        return self._get_moves_in_directions(board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])