from ..base_classes.base_bot import BaseBot
from .constant import PoddavkiCons

class PoddavkiBot(BaseBot):
    def __init__(self, piece_type):
        super().__init__()
        self.piece_type = piece_type

    def get_best_move(self, board, game_state):
        moves = self.get_all_possible_moves(board, self.piece_type)
        
        if not moves:
            return None
        
        
        best_move = None
        best_score = float('-inf')
        
        for move in moves:
            score = self.evaluate_move(move, board)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    
    def evaluate_move(self, move, board):
        # Evaluate Poddavki moves
        piece, (new_row, new_col) = move
        score = 0
        
        # STRATEGY 1: Try to be captured 
        if self.can_be_captured_after_move(board, new_row, new_col):
            score += 150  # BIG BONUS for being capturable!
        
        # STRATEGY 2: Avoid capturing opponent (we don't want them to lose!)
        if abs(new_row - piece.row) == 2:  # This is a capture move
            score -= 100  # PENALTY 
            
            # Extra penalty if the move leaves opponent with very few pieces
            opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
            opponent_pieces = board.get_all_pieces(opponent_type)
            if len(opponent_pieces) <= 3:  # Opponent has few pieces left
                score -= 200  # Huge penalty 
        
        # STRATEGY 3: Move to edges/corners (easier to be captured there)
        if new_row == 0 or new_row == 7 or new_col == 0 or new_col == 7:
            score += 30  # BONUS for edge positions (more vulnerable)
        
        # STRATEGY 4: Avoid central control (we want to be vulnerable)
        center_distance = abs(new_row - 3.5) + abs(new_col - 3.5)
        score += center_distance * 5  # BONUS for being farther from center
        
        # STRATEGY 5: Reduce mobility 
        mobility_score = self.cal_future_mobility(piece, new_row, new_col, board)
        score -= mobility_score * 15  # PENALTY for having too many moves
        
        # STRATEGY 6: Get closer to opponent pieces
        opponent_proximity_score = self.cal_opponent_proximity(board, new_row, new_col)
        score += opponent_proximity_score * 10  
        
        return score
        
    def can_be_captured_after_move(self, board, row, col):
        # Check if we can be captured if we move to this position 
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
        # Check all diagonal directions 
        capture_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        
        for drow, dcol in capture_directions:
            attacker_row = row - drow // 2
            attacker_col = col - dcol // 2
            landing_row = row + drow // 2
            landing_col = col + dcol // 2
            
            # Check bounds
            if not (0 <= attacker_row < 8 and 0 <= attacker_col < 8 and
                    0 <= landing_row < 8 and 0 <= landing_col < 8):
                continue
            
            attacker = board.get_piece(attacker_row, attacker_col)
            landing_spot = board.get_piece(landing_row, landing_col)
            
            # If there's an opponent piece that can capture us
            if (attacker and attacker.type == opponent_type and landing_spot is None):
                return True
        
        return False
    
    def cal_future_mobility(self, piece, new_row, new_col, board):
        # Calculate how many moves we'll have after this move
        old_row, old_col = piece.row, piece.col
        piece.row, piece.col = new_row, new_col
        
        future_moves = piece.get_legals_moves(board.board)
        
        piece.row, piece.col = old_row, old_col  # Restore position
        
        return len(future_moves)
    
    def cal_opponent_proximity(self, board, row, col):
        # Calculate how close we are to opponent pieces 
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        opponent_pieces = board.get_all_pieces(opponent_type)
        
        proximity_score = 0
        for op_piece in opponent_pieces:
            distance = abs(row - op_piece.row) + abs(col - op_piece.col)
            if distance <= 4:  # Close enough to matter
                proximity_score += (5 - distance)  # Closer = higher score
        
        return proximity_score
        
    def evaluate_pos(self, board, game_state):
        my_pieces = board.get_all_pieces(self.piece_type)
        return len(my_pieces) * 100














    # def evaluate_pos(self, board, game_state):
    #     # Evaluate position - more pieces is better, mobility is important"""
    #     my_pieces = board.get_all_pieces(self.piece_type)
    #     opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
    #     opponent_pieces = board.get_all_pieces(opponent_type)
        
    #     score = 0
        
    #     # More pieces is better (don't want to lose them )
    #     score += len(my_pieces) * 100
        
    #     # Fewer opponent pieces is better (want them to lose!)
    #     score -= len(opponent_pieces) * 100
        
    #     # Mobility is crucial (don't want to be trapped!)
    #     total_mobility = sum(len(piece.get_legals_moves(board.board)) for piece in my_pieces)
    #     score += total_mobility * 10
        
    #     # Opponent having low mobility is good
    #     opponent_mobility = sum(len(piece.get_legals_moves(board.board)) for piece in opponent_pieces)
    #     score -= opponent_mobility * 5
        
    #     return score