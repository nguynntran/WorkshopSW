import pygame
from ..base_classes.base_game import BaseGame
from ..base_classes.base_constants import BaseConstants as Cons
from .board import Board
from .constant import PoddavkiCons

class PoddavkiGame(BaseGame):
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.current_player = PoddavkiCons.RED_PLAYER  # Red moves first
        self.selected_piece = None
        self.valid_moves = []
        self.must_capture = False
    
    def handle_click(self, pos):
        # Handle mouse click events
        if self.game_over:
            return
        
        row, col = self.get_mouse_position(pos)
        if not self.board.is_valid_position(row, col):
            return
        
        piece = self.board.get_piece(row, col)
        
        # If clicking on empty square with selected piece, try to move
        if self.selected_piece and not piece and (row, col) in self.valid_moves:
            self.move_piece(row, col)
        # If clicking on piece of current player
        elif piece and self.is_current_player_piece(piece):
            self.select_piece(piece, row, col)
        else:
            self.clear_selection()
    
    def select_piece(self, piece, row, col):
        # Select a piece and show valid moves
        # Check if captures are mandatory
        self.must_capture = self.board.has_captures_available(piece.type)
        
        # Only allow selection if piece has valid moves
        moves = self.get_valid_moves(piece)
        if moves:
            self.selected_piece = piece
            self.board.selected_piece = (row, col)
            self.valid_moves = moves
            self.board.highlight = self.valid_moves
        else:
            self.clear_selection()
    
    def move_piece(self, new_row, new_col):
        # Move selected piece to new position
        old_row, old_col = self.selected_piece.row, self.selected_piece.col
        
        # Move piece (returns True if capture occurred)
        capture_occurred = self.board.move_piece(old_row, old_col, new_row, new_col)
        
        # Check for multiple captures
        if capture_occurred:
            # Check if same piece can capture again
            additional_captures = self.selected_piece.get_capture_moves(self.board.board)
            if additional_captures:
                # Continue with same piece
                self.valid_moves = additional_captures
                self.board.highlight = self.valid_moves
                return
        
        # Check win conditions
        self.check_win_condition()
        
        # Switch players if game not over
        if not self.game_over:
            self.switch_player()
        
        self.clear_selection()
    
    def clear_selection(self):
        # Clear current selection
        self.selected_piece = None
        self.valid_moves = []
        self.board.selected_piece = None
        self.board.highlight = []
        self.must_capture = False
    
    def is_current_player_piece(self, piece):
        # Check if piece belongs to current player
        if self.current_player == PoddavkiCons.RED_PLAYER:
            return piece.type == PoddavkiCons.RED_PIECE
        else:
            return piece.type == PoddavkiCons.BLACK_PIECE
    
    def get_valid_moves(self, piece):
        # Get valid moves for a piece
        return piece.get_legals_moves(self.board.board)
    
    def switch_player(self):
        # Switch between red and black players
        if self.current_player == PoddavkiCons.RED_PLAYER:
            self.current_player = PoddavkiCons.BLACK_PLAYER
        else:
            self.current_player = PoddavkiCons.RED_PLAYER
    
    def check_win_condition(self):
        # Check win conditions for Poddavki (reverse of regular checkers)
        red_pieces = self.board.get_all_pieces(PoddavkiCons.RED_PIECE)
        black_pieces = self.board.get_all_pieces(PoddavkiCons.BLACK_PIECE)
        
        # In Poddavki, you WIN by losing all your pieces or having no moves
        if len(red_pieces) == 0:
            self.game_over = True
            self.winner = PoddavkiCons.RED_PLAYER  # Red wins by losing all pieces
        elif len(black_pieces) == 0:
            self.game_over = True
            self.winner = PoddavkiCons.BLACK_PLAYER  # Black wins by losing all pieces
        else:
            # Check if current player has no valid moves (wins in Poddavki)
            current_pieces = red_pieces if self.current_player == PoddavkiCons.RED_PLAYER else black_pieces
            has_moves = any(self.get_valid_moves(piece) for piece in current_pieces)
            
            if not has_moves:
                self.game_over = True
                self.winner = self.current_player  # Current player wins by having no moves
    
    def draw(self, screen):
        # Draw game state
        super().draw(screen)
        self.draw_game_status(screen)
    
    def draw_game_status(self, screen):
        # Draw current player and game status
        font = pygame.font.Font(None, Cons.FONT_SIZE)
        
        if self.game_over:
            winner_name = "Red" if self.winner == PoddavkiCons.RED_PLAYER else "Black"
            text = f"{winner_name} Wins!"
        else:
            player_name = "Red" if self.current_player == PoddavkiCons.RED_PLAYER else "Black"
            capture_text = " (Must Capture!)" if self.must_capture else ""
            text = f"{player_name}'s Turn{capture_text}"
        
        text_surface = font.render(text, True, Cons.WHITE)
        screen.blit(text_surface, (10, 10))