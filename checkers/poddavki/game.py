import pygame
from ..base_classes.base_game import BaseGame
from ..base_classes.base_constants import BaseConstants as Cons
from .board import Board
from .constant import PoddavkiCons

class PoddavkiGame(BaseGame):
    def __init__(self, red_bot=None, black_bot=None):
        super().__init__()
        self.board = Board()
        self.current_player = PoddavkiCons.RED_PLAYER
        self.selected_piece = None
        self.valid_moves = []
        self.must_capture = False
        
        # Bot support
        self.red_bot = red_bot
        self.black_bot = black_bot
        self.bot_move_timer = 0
        self.bot_move_delay = 1000

    def handle_click(self, pos):
        # Don't allow moves when it's bot's turn
        if self.is_bot_turn():
            return
            
        if self.game_over:
            return
        
        row, col = self.get_mouse_position(pos)
        if not self.board.is_valid_position(row, col):
            return
        
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece and not piece and (row, col) in self.valid_moves:
            self.move_piece(row, col)
        elif piece and self.is_current_player_piece(piece):
            self.select_piece(piece, row, col)
        else:
            self.clear_selection()

    def update(self, dt):
        # Handle bot moves 
        if not self.game_over and self.is_bot_turn():
            self.bot_move_timer += dt
            if self.bot_move_timer >= self.bot_move_delay:
                self.handle_bot_turn()
                self.bot_move_timer = 0

    def is_bot_turn(self):
        # Check if it's currently a bot's turn
        if self.current_player == PoddavkiCons.RED_PLAYER and self.red_bot:
            return True
        elif self.current_player == PoddavkiCons.BLACK_PLAYER and self.black_bot:
            return True
        return False

    def handle_bot_turn(self):
        # Handle bot's turn 
        bot = None
        if self.current_player == PoddavkiCons.RED_PLAYER and self.red_bot:
            bot = self.red_bot
        elif self.current_player == PoddavkiCons.BLACK_PLAYER and self.black_bot:
            bot = self.black_bot
        
        if bot:
            move = bot.get_best_move(self.board, self)
            if move:
                piece, (new_row, new_col) = move
                self.selected_piece = piece
                self.move_piece(new_row, new_col)
            else:
                self.check_win_condition()

    def select_piece(self, piece, row, col):
        self.must_capture = self.board.has_captures_available(piece.type)
        
        moves = self.get_valid_moves(piece)
        if moves:
            self.selected_piece = piece
            self.board.selected_piece = (row, col)
            self.valid_moves = moves
            self.board.highlight = self.valid_moves
        else:
            self.clear_selection()

    def move_piece(self, new_row, new_col):
        old_row, old_col = self.selected_piece.row, self.selected_piece.col
        
        capture_occurred = self.board.move_piece(old_row, old_col, new_row, new_col)
        
        if capture_occurred:
            additional_captures = self.selected_piece.get_capture_moves(self.board.board)
            if additional_captures:
                self.valid_moves = additional_captures
                self.board.highlight = self.valid_moves
                return
        
        self.check_win_condition()
        
        if not self.game_over:
            self.switch_player()
        
        self.clear_selection()

    def clear_selection(self):
        self.selected_piece = None
        self.valid_moves = []
        self.board.selected_piece = None
        self.board.highlight = []
        self.must_capture = False

    def is_current_player_piece(self, piece):
        if self.current_player == PoddavkiCons.RED_PLAYER:
            return piece.type == PoddavkiCons.RED_PIECE
        else:
            return piece.type == PoddavkiCons.BLACK_PIECE

    def get_valid_moves(self, piece):
        return piece.get_legals_moves(self.board.board)

    def switch_player(self):
        if self.current_player == PoddavkiCons.RED_PLAYER:
            self.current_player = PoddavkiCons.BLACK_PLAYER
        else:
            self.current_player = PoddavkiCons.RED_PLAYER

    def check_win_condition(self):
        
        red_pieces = self.board.get_all_pieces(PoddavkiCons.RED_PIECE)
        black_pieces = self.board.get_all_pieces(PoddavkiCons.BLACK_PIECE)
        
        # Win condition 1: If a player has no pieces left, they win
        if len(red_pieces) == 0:
            self.game_over = True
            self.winner = PoddavkiCons.RED_PLAYER  # Red wins by losing all pieces
            return
        elif len(black_pieces) == 0:
            self.game_over = True
            self.winner = PoddavkiCons.BLACK_PLAYER  # Black wins by losing all pieces
            return
        
        # Win condition 2: If current player has no legal moves, they win
        current_pieces = red_pieces if self.current_player == PoddavkiCons.RED_PLAYER else black_pieces
        has_moves = any(self.get_valid_moves(piece) for piece in current_pieces)
        
        if not has_moves:
            self.game_over = True
            self.winner = self.current_player  # Current player wins by having no moves

    def draw(self, screen):
        super().draw(screen)
        self.draw_game_status(screen)

    def draw_game_status(self, screen):
        font = pygame.font.Font(None, Cons.FONT_SIZE)
        
        if self.game_over:
            winner_name = "Red" if self.winner == PoddavkiCons.RED_PLAYER else "Black"
            text = f"{winner_name} Wins!"
        else:
            player_name = "Red" if self.current_player == PoddavkiCons.RED_PLAYER else "Black"
            
            if self.current_player == PoddavkiCons.RED_PLAYER and self.red_bot:
                player_name += " (Bot)"
            elif self.current_player == PoddavkiCons.BLACK_PLAYER and self.black_bot:
                player_name += " (Bot)"
            
            capture_text = " (Must Capture!)" if self.must_capture else ""
            text = f"{player_name}'s Turn{capture_text}"
        
        text_surface = font.render(text, True, Cons.WHITE)
        screen.blit(text_surface, (10, 10))

    def is_game_over(self):
        """Required by BaseGame"""
        return self.game_over

    def get_winner(self):
        """Required by BaseGame"""
        return self.winner if self.game_over else None