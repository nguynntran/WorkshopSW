import pygame
from ..base_classes.base_pieces import BasePiece
from ..base_classes.base_constants import BaseConstants as Cons
from .constant import PoddavkiCons

class PoddavkiPiece(BasePiece):
    def __init__(self, piece_type, row, col):
        color = PoddavkiCons.RED_COLOR if piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.BLACK_COLOR
        super().__init__(piece_type, row, col, color)
        self.is_king = False
    
    def draw(self, screen):
        center = self.get_center()
        radius = Cons.SQUARE_SIZE // 2 - 10
        
        # Draw shadow
        pygame.draw.circle(screen, Cons.BLACK, 
                         (center[0] + 2, center[1] + 2), radius)
        
        # Draw main piece
        pygame.draw.circle(screen, self.color, center, radius)
        
        # Draw border
        border_color = Cons.BLACK if self.type == PoddavkiCons.RED_PIECE else Cons.WHITE
        pygame.draw.circle(screen, border_color, center, radius, 2)
        
        # Draw king crown if piece is king
        if self.is_king:
            pygame.draw.circle(screen, PoddavkiCons.KING_COLOR, center, 
                             PoddavkiCons.CROWN_RADIUS)
    
    def get_legals_moves(self, board):
        # Get legal moves and must capture if possible
        # First check for captures
        captures = self.get_capture_moves(board)
        if captures:
            return captures
        
        # If no captures, return regular moves
        return self._get_moves_in_directions(board, self.get_move_directions())
    
    def get_capture_moves(self, board):
        # Get all possible capture moves
        captures = []
        directions = self.get_move_directions()
        
        for drow, dcol in directions:
            # Check for piece to capture
            capture_row = self.row + drow
            capture_col = self.col + dcol
            
            if (0 <= capture_row < Cons.ROWS and 0 <= capture_col < Cons.COLS):
                piece_to_capture = board[capture_row][capture_col]
                
                # If there's an opponent piece
                if (piece_to_capture and 
                    piece_to_capture.type != self.type):
                    
                    # Check landing square
                    land_row = capture_row + drow
                    land_col = capture_col + dcol
                    
                    if self._is_val_pos(board, land_row, land_col):
                        captures.append((land_row, land_col))
        
        return captures
    
    def get_move_directions(self):
        # Get movement directions based on piece type and king status"""
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # All directions
        else:
            if self.type == PoddavkiCons.RED_PIECE:
                return [(-1, -1), (-1, 1)]  # Red moves up
            else:
                return [(1, -1), (1, 1)]    # Black moves down
    
    def make_king(self):
        # Make piece to be a king"""
        self.is_king = True
    
    def should_be_king(self):
        # Check if piece can be a king"""
        if self.type == PoddavkiCons.RED_PIECE and self.row == 0:
            return True
        elif self.type == PoddavkiCons.BLACK_PIECE and self.row == 7:
            return True
        return False