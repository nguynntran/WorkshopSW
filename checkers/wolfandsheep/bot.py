from ..base_classes.base_bot import BaseBot
from .constant import WASCons

class WolfBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.piece_type = WASCons.WOLF

    def get_best_move(self, board, game_state):
        moves = self.get_all_possible_moves(board, self.piece_type)
        sheep = game_state.find_sheep()
        
        if not sheep or not moves:
            return self.get_random_move(board)
        
        best_move = None
        best_score = float('-inf')
        
        for move in moves:
            score = self.evaluate_move(move, board, sheep)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def evaluate_move(self, move, board, sheep):
        piece, (new_row, new_col) = move
        score = 0
        
        # Get closer to sheep
        distance = abs(new_row - sheep.row) + abs(new_col - sheep.col)
        score -= distance * 2
        
        # Block sheep's path to goal
        if new_row < sheep.row and abs(new_col - sheep.col) <= 1:
            score += 15
        
        # Stay near other wolves to restrict the move of sheep
        wolves_nearby = self.count_wolves_near(board, new_row, new_col)
        score += wolves_nearby * 5
        
        return score
    
    def count_wolves_near(self, board, row, col):
        # Count wolves within 2 squares
        count = 0
        for r in range(max(0, row-2), min(8, row+3)):
            for c in range(max(0, col-2), min(8, col+3)):
                piece = board.get_piece(r, c)
                if piece and piece.type == WASCons.WOLF:
                    count += 1
        return count

    def evaluate_pos(self, board, game_state):
        sheep = game_state.find_sheep()
        return (7 - sheep.row) * 10 if sheep else 1000


class SheepBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.piece_type = WASCons.SHEEP

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
        piece, (new_row, new_col) = move
        score = 0
        
        # Move toward goal (row 0)
        score += (piece.row - new_row) * 50
        
        # Avoid wolves
        wolves_near = self.count_wolves_near(board, new_row, new_col)
        score -= wolves_near * 25
        
        # Avoid edges to have more space (except goal row)
        if new_row > 0 and (new_col == 0 or new_col == 7):
            score -= 10
        
        return score
    
    def count_wolves_near(self, board, row, col):
        # Count wolves within 2 squares
        count = 0
        for r in range(max(0, row-2), min(8, row+3)):
            for c in range(max(0, col-2), min(8, col+3)):
                piece = board.get_piece(r, c)
                if piece and piece.type == WASCons.WOLF:
                    count += 1
        return count

    def evaluate_pos(self, board, game_state):
        sheep = game_state.find_sheep()
        if not sheep:
            return -1000
        if sheep.row == 0:
            return 1000
        return (7 - sheep.row) * 50