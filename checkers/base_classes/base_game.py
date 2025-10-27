from abc import ABC, abstractmethod
from .base_constants import BaseConstants as Cons
class BaseGame(ABC):
    #Abstract base class for all games
    def __init__(self):
        self.board = None 
        self.current_player = None
        self.game_over = False
        self.winner = None
    
    @abstractmethod
    def handle_click(self, pos):
        pass
    
    @abstractmethod
    def check_win_condition(self):     # Check win conditions 
        pass
    
    @abstractmethod
    def get_valid_moves(self, piece):  # Get valid moves for a piece
        pass
    
    def reset_game(self):              # Reset the game to initial state
        self.__init__()
    
    def switch_player(self):           # Switch to the other player
        pass
    
    def get_mouse_position(self, pos):
        # Convert mouse position to board coordinates
        x, y = pos
        col = x // Cons.SQUARE_SIZE
        row = y // Cons.SQUARE_SIZE
        return row, col
    
    def draw(self, screen):            # Draw the current game state
        self.board.draw_board(screen)
    
    def is_game_over(self):
        return self.game_over
    
    def get_winner(self):
        return self.winner