
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
        """Get legal moves - captures are mandatory if available"""
        # First check for captures (mandatory if available)
        captures = self.get_capture_moves(board)
        if captures:
            return captures
        
        # If no captures, return regular moves
        return self.get_regular_moves(board)
    
    def get_regular_moves(self, board):
        """Get non-capturing moves"""
        moves = []
        
        if self.is_king:
            # Kings: one square in any diagonal direction
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for drow, dcol in directions:
                new_row = self.row + drow
                new_col = self.col + dcol
                
                if self._is_valid_position(new_row, new_col) and board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
        else:
            # Regular pieces move 1 square diagonally forward
            directions = self.get_move_directions()
            for drow, dcol in directions:
                new_row = self.row + drow
                new_col = self.col + dcol
                
                if self._is_valid_position(new_row, new_col) and board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_capture_moves(self, board):
        """Get all possible capture moves"""
        captures = []
        
        if self.is_king:
            # Kings: capture by jumping one adjacent opponent in any diagonal direction
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Regular pieces capture forward only
            directions = self.get_move_directions()
        
        for drow, dcol in directions:
            capture_row = self.row + drow
            capture_col = self.col + dcol
            
            if not self._is_valid_position(capture_row, capture_col):
                continue
            
            piece_to_capture = board[capture_row][capture_col]
            
            # Must be opponent piece
            if not (piece_to_capture and piece_to_capture.type != self.type):
                continue
            
            land_row = capture_row + drow
            land_col = capture_col + dcol
            
            if self._is_valid_position(land_row, land_col) and board[land_row][land_col] is None:
                captures.append((land_row, land_col))
        
        return captures
    
    def get_move_directions(self):
        """Get movement directions based on piece type and king status"""
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # All directions
        else:
            if self.type == PoddavkiCons.RED_PIECE:
                return [(-1, -1), (-1, 1)]  # Red moves up
            else:
                return [(1, -1), (1, 1)]    # Black moves down
    
    def _is_valid_position(self, row, col):
        """Check if position is valid and within bounds"""
        return 0 <= row < Cons.ROWS and 0 <= col < Cons.COLS
    
    def make_king(self):
        """Make piece a king"""
        self.is_king = True
    
    def should_be_king(self):
        """Check if piece should be crowned"""
        if self.type == PoddavkiCons.RED_PIECE and self.row == 0:
            return True
        elif self.type == PoddavkiCons.BLACK_PIECE and self.row == 7:
            return True
        return False