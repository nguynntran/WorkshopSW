# checkers/base_classes/base_bot.py
from abc import ABC, abstractmethod
import random

class BaseBot(ABC):
    def __init__(self):
        self.piece_type = None  
    
    @abstractmethod
    def get_best_move(self, board, game_state):
        pass
    
    @abstractmethod
    def evaluate_pos(self, board, game_state):
        pass

    def get_all_possible_moves(self, board, piece_type):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.type == piece_type:
                    legal_moves = piece.get_legals_moves(board.board)
                    for move in legal_moves:
                        moves.append((piece, move))
        return moves
    
    def get_random_move(self, board):
        """Get a random valid move - common utility for all bots"""
        moves = self.get_all_possible_moves(board, self.piece_type)
        return random.choice(moves) if moves else None