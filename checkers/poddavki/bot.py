
# # checkers/poddavki/bot.py
# from ..base_classes.base_bot import BaseBot
# from .constant import PoddavkiCons

# class PoddavkiBot(BaseBot):
#     def __init__(self, piece_type):
#         super().__init__()
#         self.piece_type = piece_type

#     def get_best_move(self, board, game_state):
#         moves = self.get_all_possible_moves(board, self.piece_type)
        
#         if not moves:
#             return None
        
#         # # PRIORITY 1: Look for moves that force opponent to lose
#         # winning_move = self.find_winning_move(moves, board)
#         # if winning_move:
#         #     return winning_move
        
#         best_move = None
#         best_score = float('-inf')
        
#         for move in moves:
#             score = self.evaluate_move(move, board)
#             if score > best_score:
#                 best_score = score
#                 best_move = move
        
#         return best_move
    
#     # def find_winning_move(self, moves, board):
#     #     # Find moves that win the game (force opponent to lose)
#     #     opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
#     #     for move in moves:
#     #         piece, (new_row, new_col) = move
            
#     #         # Simulate the move
#     #         old_row, old_col = piece.row, piece.col
#     #         captured_piece = self.simulate_move(piece, new_row, new_col, board)
            
#     #         # Check if opponent has no pieces left (they lose!)
#     #         opponent_pieces = board.get_all_pieces(opponent_type)
#     #         if len(opponent_pieces) == 0:
#     #             # Undo move and return this winning move
#     #             self.undo_move(piece, old_row, old_col, new_row, new_col, captured_piece, board)
#     #             return move
            
#     #         # Check if opponent has no legal moves (they lose!)
#     #         opponent_has_moves = any(op_piece.get_legals_moves(board.board) for op_piece in opponent_pieces)
#     #         if not opponent_has_moves:
#     #             # Undo move and return this winning move
#     #             self.undo_move(piece, old_row, old_col, new_row, new_col, captured_piece, board)
#     #             return move
            
#     #         # Undo the simulation
#     #         self.undo_move(piece, old_row, old_col, new_row, new_col, captured_piece, board)
        
#     #     return None
    
#     def evaluate_move(self, move, board):
#         # Evaluate Poddavki moves
#         piece, (new_row, new_col) = move
#         score = 0
        
#         # STRATEGY 1: Avoid being captured 
#         if self.can_be_captured_after_move(board, new_row, new_col):
#             score -= 100  # Big loss point for being capturable!
        
#         # STRATEGY 2: Force captures when beneficial (to reduce opponent's pieces)
#         if abs(new_row - piece.row) == 2:  # This is a capture move
#             score += 50  # Bonus for capturing opponent
            
#             # Extra bonus if this move make opponent with very few pieces
#             opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
#             opponent_pieces = board.get_all_pieces(opponent_type)
#             if len(opponent_pieces) <= 3:  # Opponent getting low on pieces
#                 score += 100
        
#         # STRATEGY 3: Stay away from edges (harder to be trapped there)
#         if new_row == 0 or new_row == 7 or new_col == 0 or new_col == 7:
#             score -= 20  # Penalty for edge positions (easier to be trapped)
        
#         # STRATEGY 4: Maintain central control
#         center_distance = abs(new_row - 3.5) + abs(new_col - 3.5)
#         score -= center_distance * 3  

#         # STRATEGY 5: Preserve mobility (avoid getting trapped)
#         mobility_score = self.cal_future_mobility(piece, new_row, new_col, board)
#         score += mobility_score * 10  # Bonus for maintaining options
        
#         # STRATEGY 6: Control opponent's movement
#         opponent_control_score = self.cal_opponent_pressure(board, new_row, new_col)
#         score += opponent_control_score * 5
        
#         return score
    
#     def can_be_captured_after_move(self, board, row, col):
#         # Check if we can be captured if we move to this position 
#         opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
#         # Check all diagonal directions where opponent could capture us
#         capture_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        
#         for drow, dcol in capture_directions:
#             attacker_row = row - drow // 2
#             attacker_col = col - dcol // 2
#             landing_row = row + drow // 2
#             landing_col = col + dcol // 2
            
#             # Check bounds
#             if not (0 <= attacker_row < 8 and 0 <= attacker_col < 8 and
#                     0 <= landing_row < 8 and 0 <= landing_col < 8):
#                 continue
            
#             attacker = board.get_piece(attacker_row, attacker_col)
#             landing_spot = board.get_piece(landing_row, landing_col)
            
#             # If there's an opponent piece that can capture us
#             if (attacker and attacker.type == opponent_type and landing_spot is None):
#                 return True
        
#         return False
    
#     def cal_future_mobility(self, piece, new_row, new_col, board):
#         # Calculate how many moves we'll have after this move
#         old_row, old_col = piece.row, piece.col
#         piece.row, piece.col = new_row, new_col
        
#         future_moves = piece.get_legals_moves(board.board)
        
#         piece.row, piece.col = old_row, old_col  # Restore position
        
#         return len(future_moves)
    
#     def cal_opponent_pressure(self, board, row, col):
#         # Calculate the pressure this position puts on opponent 
#         opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
#         opponent_pieces = board.get_all_pieces(opponent_type)
        
#         press = 0
#         for op_piece in opponent_pieces:
#             # Calculate distance to opponent pieces (closer = more pressure)
#             dist = abs(row - op_piece.row) + abs(col - op_piece.col)
#             if dist <= 3:  # Close enough to threaten
#                 press += (4 - dist)  # Closer = more pressure
        
#         return press
    
#     # def simulate_move(self, piece, new_row, new_col, board):
#     #     """Simulate a move and return captured piece if any"""
#     #     old_row, old_col = piece.row, piece.col
#     #     captured_piece = None
        
#     #     # Check if it's a capture move
#     #     if abs(new_row - old_row) == 2:
#     #         capture_row = (old_row + new_row) // 2
#     #         capture_col = (old_col + new_col) // 2
#     #         captured_piece = board.board[capture_row][capture_col]
#     #         board.board[capture_row][capture_col] = None
        
#     #     # Move the piece
#     #     board.board[old_row][old_col] = None
#     #     board.board[new_row][new_col] = piece
#     #     piece.row, piece.col = new_row, new_col
        
#     #     return captured_piece
    
#     # def undo_move(self, piece, old_row, old_col, new_row, new_col, captured_piece, board):
#     #     """Undo a simulated move"""
#     #     # Move piece back
#     #     board.board[new_row][new_col] = None
#     #     board.board[old_row][old_col] = piece
#     #     piece.row, piece.col = old_row, old_col
        
#     #     # Restore captured piece if any
#     #     if captured_piece:
#     #         capture_row = (old_row + new_row) // 2
#     #         capture_col = (old_col + new_col) // 2
#     #         board.board[capture_row][capture_col] = captured_piece

#     def evaluate_pos(self, board, game_state):
#         # Evaluate position - more pieces is better, mobility is important"""
#         my_pieces = board.get_all_pieces(self.piece_type)
#         opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
#         opponent_pieces = board.get_all_pieces(opponent_type)
        
#         score = 0
        
#         # More pieces is better (don't want to lose them )
#         score += len(my_pieces) * 100
        
#         # Fewer opponent pieces is better (want them to lose!)
#         score -= len(opponent_pieces) * 100
        
#         # Mobility is crucial (don't want to be trapped!)
#         total_mobility = sum(len(piece.get_legals_moves(board.board)) for piece in my_pieces)
#         score += total_mobility * 10
        
#         # Opponent having low mobility is good
#         opponent_mobility = sum(len(piece.get_legals_moves(board.board)) for piece in opponent_pieces)
#         score -= opponent_mobility * 5
        
#         return score


# checkers/poddavki/bot.py
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
        
        # STRATEGY 1: Avoid being captured 
        if self.can_be_captured_after_move(board, new_row, new_col):
            score -= 100  # Big loss point for being capturable!
        
        # STRATEGY 2: Force captures when beneficial (to reduce opponent's pieces)
        if abs(new_row - piece.row) == 2:  # This is a capture move
            score += 50  # Bonus for capturing opponent
            
            # Extra bonus if this move make opponent with very few pieces
            opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
            opponent_pieces = board.get_all_pieces(opponent_type)
            if len(opponent_pieces) <= 3:  # Opponent getting low on pieces
                score += 100
        
        # STRATEGY 3: Stay away from edges (harder to be trapped there)
        if new_row == 0 or new_row == 7 or new_col == 0 or new_col == 7:
            score -= 20  # Penalty for edge positions (easier to be trapped)
        
        # STRATEGY 4: Maintain central control
        center_distance = abs(new_row - 3.5) + abs(new_col - 3.5)
        score -= center_distance * 3  

        # STRATEGY 5: Preserve mobility (avoid getting trapped)
        mobility_score = self.cal_future_mobility(piece, new_row, new_col, board)
        score += mobility_score * 10  # Bonus for maintaining options
        
        # STRATEGY 6: Control opponent's movement
        opponent_control_score = self.cal_opponent_pressure(board, new_row, new_col)
        score += opponent_control_score * 5
        
        return score
    
    def can_be_captured_after_move(self, board, row, col):
        # Check if we can be captured if we move to this position 
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
        # Check all diagonal directions where opponent could capture us
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
    
    def cal_opponent_pressure(self, board, row, col):
        # Calculate the pressure this position puts on opponent 
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        opponent_pieces = board.get_all_pieces(opponent_type)
        
        press = 0
        for op_piece in opponent_pieces:
            # Calculate distance to opponent pieces (closer = more pressure)
            dist = abs(row - op_piece.row) + abs(col - op_piece.col)
            if dist <= 3:  # Close enough to threaten
                press += (4 - dist)  # Closer = more pressure
        
        return press
    
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