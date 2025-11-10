import pygame
from ..base_classes.base_game import BaseGame
from ..base_classes.base_constants import BaseConstants as Cons
from .board import Board
from .constant import WASCons

class WolfAndSheepGame(BaseGame):
    def __init__(self, wolves_bot=None, sheep_bot=None):
        super().__init__()
        self.board = Board()
        self.current_player = WASCons.WOLVES_PLAYER  # Wolves move first
        self.selected_piece = None
        self.valid_moves = []
        
        # Bot support
        self.wolves_bot = wolves_bot
        self.sheep_bot = sheep_bot
        self.bot_move_timer = 0
        self.bot_move_delay = 1000  # 1 second delay for bot moves
    
    def handle_click(self, pos):
        # Don't allow manual moves when it's bot's turn
        if self.is_bot_turn():
            return
            
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
    
    def update(self, dt):
        # Call this in main game loop to handle bot moves
        if not self.game_over and self.is_bot_turn():
            self.bot_move_timer += dt
            if self.bot_move_timer >= self.bot_move_delay:
                self.handle_bot_turn()
                self.bot_move_timer = 0
    
    def is_bot_turn(self):
        # Check if it's currently a bot's turn
        if self.current_player == WASCons.WOLVES_PLAYER and self.wolves_bot:
            return True
        elif self.current_player == WASCons.SHEEP_PLAYER and self.sheep_bot:
            return True
        return False
    
    def handle_bot_turn(self):
        # Handle bot's turn
        bot = None
        if self.current_player == WASCons.WOLVES_PLAYER and self.wolves_bot:
            bot = self.wolves_bot
        elif self.current_player == WASCons.SHEEP_PLAYER and self.sheep_bot:
            bot = self.sheep_bot
        
        if bot:
            move = bot.get_best_move(self.board, self)
            if move:
                piece, (new_row, new_col) = move
                self.selected_piece = piece
                self.move_piece(new_row, new_col)
            else:
                # No valid moves available - this should trigger win condition
                print(f"No moves available for {self.current_player}")
                self.check_win_condition()
    
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
        
        # Check win conditions BEFORE switching players
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
            return piece.type == WASCons.WOLF
        else:
            return piece.type == WASCons.SHEEP
    
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
        
        # First check if sheep reached top row (sheep wins)
        for col in range(Cons.COLS):
            piece = self.board.get_piece(0, col)
            if piece and piece.type == WASCons.SHEEP:
                self.game_over = True
                self.winner = WASCons.SHEEP_PLAYER
                print("Sheep wins by reaching the top row!")
                return
        
        # Check if sheep has no legal moves (wolves win)
        sheep_piece = self.find_sheep()
        if sheep_piece:
            sheep_moves = self.get_valid_moves(sheep_piece)
            if len(sheep_moves) == 0:
                self.game_over = True
                self.winner = WASCons.WOLVES_PLAYER
                print("Wolves win! Sheep has no legal moves.")
                return
        else:
            # No sheep found (shouldn't happen, but just in case)
            self.game_over = True
            self.winner = WASCons.WOLVES_PLAYER
            print("Wolves win! No sheep on board.")
            return
    
    def find_sheep(self):
        # Find the sheep piece on the board
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                piece = self.board.get_piece(row, col)
                if piece and piece.type == WASCons.SHEEP:
                    return piece
        return None
    
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
            # Show current player and if it's a bot
            if self.current_player == WASCons.WOLVES_PLAYER:
                player_text = "Wolves"
                if self.wolves_bot:
                    player_text += " (Bot)"
            else:
                player_text = "Sheep"
                if self.sheep_bot:
                    player_text += " (Bot)"
            
            text = f"{player_text}'s Turn"
        
        text_surface = font.render(text, True, Cons.WHITE)
        screen.blit(text_surface, (10, 10))
    
    def is_game_over(self):
        # Required by BaseGame
        return self.game_over
    
    def get_winner(self):
        # Required by BaseGame
        return self.winner