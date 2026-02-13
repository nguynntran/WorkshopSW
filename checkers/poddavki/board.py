from ..base_classes.base_board import BaseBoard
from ..base_classes.base_constants import BaseConstants as Cons
from .constant import PoddavkiCons
from .pieces import PoddavkiPiece

class Board(BaseBoard):
    def __init__(self):
        super().__init__()
        self.setup_initial_pieces()
    
    def setup_initial_pieces(self):
        # Setup initial pieces (regular checkers layout)
        # Place black pieces (top 3 rows)
        for row in range(3):
            for col in range(Cons.COLS):
                if (row + col) % 2 == 1:  # Only on dark squares
                    self.board[row][col] = PoddavkiPiece(PoddavkiCons.BLACK_PIECE, row, col)
        
        # Place red pieces (bottom 3 rows)
        for row in range(5, 8):
            for col in range(Cons.COLS):
                if (row + col) % 2 == 1:  # Only on dark squares
                    self.board[row][col] = PoddavkiPiece(PoddavkiCons.RED_PIECE, row, col)
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        # Move piece and handle captures and king promotion
        piece = self.board[from_row][from_col]
        if not piece:
            return False
        
        # Check if this is a capture move
        captured_piece = None
        if abs(to_row - from_row) == 2:  # Capture move
            capture_row = (from_row + to_row) // 2  # Row of the captured piece
            capture_col = (from_col + to_col) // 2  # Col of the captured piece
            captured_piece = self.board[capture_row][capture_col]
            self.board[capture_row][capture_col] = None
        
        # Move the piece
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        piece.move_to(to_row, to_col)
        
        # Check for king promotion
        if piece.should_be_king():
            piece.make_king()
        
        return captured_piece is not None
    
    def get_all_pieces(self, piece_type):
        # Get all pieces of a specific type
        pieces = []
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                piece = self.board[row][col]
                if piece and piece.type == piece_type:
                    pieces.append(piece)
        return pieces
    
    def has_captures_available(self, piece_type):
        # Check if any piece of given type has captures available
        pieces = self.get_all_pieces(piece_type)
        for piece in pieces:
            if piece.get_capture_moves(self.board):
                return True
        return False