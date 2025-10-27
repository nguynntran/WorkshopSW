import pygame
from ..base_classes.base_game import BaseGame
from ..base_classes.base_constants import BaseConstants as Cons
from .board import Board
from .constant import WASCons

class WolfAndSheepGame(BaseGame):
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.current_player = WASCons.WOLVES_PLAYER  # Wolves move first
        self.selected_piece = None
        self.valid_moves = []
    
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
        self.selected_piece = piece
        self.board.selected_piece = (row, col)
        self.valid_moves = self.get_valid_moves(piece)
        self.board.highlight = self.valid_moves
    
    def move_piece(self, new_row, new_col):
        # Move selected piece to new position 
        old_row, old_col = self.selected_piece.row, self.selected_piece.col
        
        # Move piece
        self.board.move_piece(old_row, old_col, new_row, new_col)
        
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
    
    def is_current_player_piece(self, piece):
        # Check if piece belongs to current player 
        if self.current_player == WASCons.WOLVES_PLAYER:
            return piece.type == WASCons.WOLF  # Using numeric constant 1
        else:
            return piece.type == WASCons.SHEEP  # Using numeric constant 2
    
    def get_valid_moves(self, piece):
        # Get valid moves for a piece
        return piece.get_legals_moves(self.board.board)
    
    def switch_player(self):
        # Switch between wolves and sheep players
        if self.current_player == WASCons.WOLVES_PLAYER:
            self.current_player = WASCons.SHEEP_PLAYER
        else:
            self.current_player = WASCons.WOLVES_PLAYER
    
    def check_win_condition(self):
        # Check win conditions 
        # Check if sheep reached top row (sheep wins)
        for col in range(Cons.COLS):
            piece = self.board.get_piece(0, col)
            if piece and piece.type == WASCons.SHEEP:  # Using numeric constant 2
                self.game_over = True
                self.winner = WASCons.SHEEP_PLAYER
                return
        
        # Check if sheep has no legal moves (wolves win)
        if self.current_player == WASCons.SHEEP_PLAYER:
            sheep_piece = self.find_sheep()
            if sheep_piece and len(self.get_valid_moves(sheep_piece)) == 0:
                self.game_over = True
                self.winner = WASCons.WOLVES_PLAYER
    
    def find_sheep(self):
        # Find the sheep piece on the board using numeric type"""
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                piece = self.board.get_piece(row, col)
                if piece and piece.type == WASCons.SHEEP:  # Using numeric constant 2
                    return piece
        return None
    
    def get_mouse_position(self, pos):
        # Convert mouse position to board coordinates
        x, y = pos
        col = x // Cons.SQUARE_SIZE
        row = y // Cons.SQUARE_SIZE
        return row, col
    
    def draw(self, screen):
        # Draw game state
        super().draw(screen)
        self.draw_game_status(screen)
    
    def draw_game_status(self, screen):
        # Draw current player and game status
        font = pygame.font.Font(None, Cons.FONT_SIZE)
        
        if self.game_over:
            if self.winner == WASCons.SHEEP_PLAYER:
                text = "Sheep Wins!"
            else:
                text = "Wolves Win!"
        else:
            if self.current_player == WASCons.WOLVES_PLAYER:
                text = "Wolves' Turn"
            else:
                text = "Sheep's Turn"
        
        text_surface = font.render(text, True, Cons.WHITE)
        screen.blit(text_surface, (10, 10))