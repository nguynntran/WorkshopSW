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

        # Enforce mandatory capture
        capturing_moves = []
        for move in moves:
            piece, (new_row, new_col) = move
            if abs(new_row - piece.row) == 2:  
                capturing_moves.append(move)

        if capturing_moves:
            moves_to_consider = capturing_moves
        else:
            moves_to_consider = moves

        best_move = None
        best_score = float("-inf")

        for move in moves_to_consider:
            score = self.evaluate_move(move, board)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    
    
    def evaluate_move(self, move, board):

        if self.leads_to_immediate_win(move, board):
            return 10000
        
        # Evaluate moves
        piece, (new_row, new_col) = move
        score = 0
        
        # STRATEGY 1: Try to be captured 
        if self.can_be_captured_after_move(board, new_row, new_col):
            score += 150  # BIG BONUS for being capturable!
        
        # STRATEGY 2: Avoid capturing opponent 
        if abs(new_row - piece.row) == 2:  # capture move
            score -= 100  # PENALTY 
            
            # Extra penalty if the move leaves opponent with very few pieces
            opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
            opponent_pieces = board.get_all_pieces(opponent_type)
            if len(opponent_pieces) <= 3:  # Opponent has few pieces left
                score -= 200  # Huge penalty 
        
        # STRATEGY 3: Move to edges/corners 
        if new_row == 0 or new_row == 7 or new_col == 0 or new_col == 7:
            score += 30  # BONUS for edge positions
        
        # STRATEGY 4: Avoid central control 
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
    def leads_to_immediate_win(self, move, board):

        piece, (new_row, new_col) = move
        old_row, old_col = piece.row, piece.col
        
        # Simulate the move temporarily
        captured = None
        if abs(new_row - old_row) == 2:  # Capture move
            capture_row = (old_row + new_row) // 2
            capture_col = (old_col + new_col) // 2
            captured = board.board[capture_row][capture_col]
            if captured:
                board.board[capture_row][capture_col] = None
        
        # Move piece temporarily
        board.board[old_row][old_col] = None
        board.board[new_row][new_col] = piece
        piece.row, piece.col = new_row, new_col
        
        # Check win conditions
        my_pieces = board.get_all_pieces(self.piece_type)
        no_pieces = len(my_pieces) == 0
        no_moves = not any(p.get_legals_moves(board.board) for p in my_pieces)
        is_win = no_pieces or no_moves
        
        # Undo the move
        board.board[new_row][new_col] = None
        board.board[old_row][old_col] = piece
        piece.row, piece.col = old_row, old_col
        if captured:
            capture_row = (old_row + new_row) // 2
            capture_col = (old_col + new_col) // 2
            board.board[capture_row][capture_col] = captured
        
        return is_win
