from ..base_classes.base_bot import BaseBot
from .constant import PoddavkiCons

class OptimizedPoddavkiBot(BaseBot):
    def __init__(self, piece_type):
        super().__init__()
        self.piece_type = piece_type

        # Scoring weights
        self.weights = {
            "capture_bonus": 220,
            "capture_penalty": -100,
            "edge_bonus": 55,
            "center_bonus": 12,
            "mobility_penalty": -25,
            "proximity_bonus": 20,
            "sacrifice_bonus": 30,
            "endgame_bonus": 60,
            "trapped_bonus": 15,
            "win_score": 10000,
        }

    def get_best_move(self, board, game_state):
        moves = self.get_all_possible_moves(board, self.piece_type)
        
        if not moves:
            return None

        # Enforce mandatory capture
        capturing_moves = []
        for move in moves:
            piece, (new_row, new_col) = move
            if self.is_capture_move(piece, new_row, new_col, board):
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

    def is_capture_move(self, piece, new_row, new_col, board):
        # Check if this move is a capture
        old_row, old_col = piece.row, piece.col
        
        # Must be diagonal move
        if abs(new_row - old_row) != abs(new_col - old_col):
            return False
        
        # Must move at least 2 squares for a capture
        if abs(new_row - old_row) < 2:
            return False
        
        # Calculate direction
        row_dir = 1 if new_row > old_row else -1
        col_dir = 1 if new_col > old_col else -1
        
        # Check path for exactly one opponent piece
        captured_pieces = 0
        current_row = old_row + row_dir
        current_col = old_col + col_dir
        
        while current_row != new_row and current_col != new_col:
            piece_at_pos = board.get_piece(current_row, current_col)
            if piece_at_pos:
                if piece_at_pos.type != self.piece_type:
                    captured_pieces += 1
                else:
                    return False
            current_row += row_dir
            current_col += col_dir
        
        return captured_pieces == 1

    def evaluate_move(self, move, board):
        # Score a move for Poddavki
        if self.move_leads_to_win(move, board):
            return self.weights["win_score"]

        piece, (new_row, new_col) = move
        score = 0

        # Be easy to capture
        threats = self.count_immediate_captures(board, new_row, new_col)
        score += threats * self.weights["capture_bonus"]

        # Avoid capturing opponent
        if self.is_capture_move(piece, new_row, new_col, board):
            if self.capture_move_wins(move, board):
                return self.weights["win_score"] - 100
            score += self.weights["capture_penalty"]

        # Prefer edges/corners
        edge_value = self.edge_value(new_row, new_col)
        score += edge_value * self.weights["edge_bonus"]

        # Avoid center
        center_dist = abs(new_row - 3.5) + abs(new_col - 3.5)
        score += center_dist * self.weights["center_bonus"]

        # Reduce future mobility
        mobility = self.future_mobility(piece, new_row, new_col, board)
        score += mobility * self.weights["mobility_penalty"]

        # Stay close to opponent
        proximity = self.opponent_proximity(board, new_row, new_col)
        score += proximity * self.weights["proximity_bonus"]

        # Sacrifice value
        sacrifice_val = self.sacrifice_value(board, new_row, new_col)
        score += sacrifice_val * self.weights["sacrifice_bonus"]

        # Endgame awareness
        my_pieces = board.get_all_pieces(self.piece_type)
        if len(my_pieces) <= 5:
            endgame_val = self.endgame_value(len(my_pieces))
            score += endgame_val * self.weights["endgame_bonus"]

        # Prefer trapped
        trapped_val = self.trapped_value(board, new_row, new_col)
        score += trapped_val * self.weights["trapped_bonus"]

        return score

    def move_leads_to_win(self, move, board):
        # Check if after this move we immediately win
        piece, (new_row, new_col) = move
        old_row, old_col = piece.row, piece.col

        captured_piece = self.simulate_move(piece, new_row, new_col, board)

        my_pieces = board.get_all_pieces(self.piece_type)
        no_pieces = len(my_pieces) == 0
        no_moves = not any(p.get_legals_moves(board.board) for p in my_pieces)
        is_win = no_pieces or no_moves

        self.undo_move(piece, old_row, old_col, new_row, new_col, captured_piece, board)
        return is_win

    def capture_move_wins(self, move, board):
        # Only relevant for capture moves
        piece, (new_row, _) = move
        if not self.is_capture_move(piece, new_row, _, board):
            return False
        return self.move_leads_to_win(move, board)

    def simulate_move(self, piece, new_row, new_col, board):
        # Apply move on board; return captured piece
        old_row, old_col = piece.row, piece.col
        captured_piece = None

        if self.is_capture_move(piece, new_row, new_col, board):
            row_dir = 1 if new_row > old_row else -1
            col_dir = 1 if new_col > old_col else -1
            
            current_row = old_row + row_dir
            current_col = old_col + col_dir
            
            while current_row != new_row and current_col != new_col:
                piece_at_pos = board.board[current_row][current_col]
                if piece_at_pos and piece_at_pos.type != self.piece_type:
                    captured_piece = piece_at_pos
                    board.board[current_row][current_col] = None
                    break
                current_row += row_dir
                current_col += col_dir

        board.board[old_row][old_col] = None
        board.board[new_row][new_col] = piece
        piece.row, piece.col = new_row, new_col

        return captured_piece

    def undo_move(self, piece, old_row, old_col, new_row, new_col, captured_piece, board):
        # Undo a simulated move
        board.board[new_row][new_col] = None
        board.board[old_row][old_col] = piece
        piece.row, piece.col = old_row, old_col

        if captured_piece:
            # Find where to restore the captured piece
            row_dir = 1 if new_row > old_row else -1
            col_dir = 1 if new_col > old_col else -1
            
            current_row = old_row + row_dir
            current_col = old_col + col_dir
            
            while current_row != new_row and current_col != new_col:
                if board.board[current_row][current_col] is None:
                    board.board[current_row][current_col] = captured_piece
                    break
                current_row += row_dir
                current_col += col_dir

    def count_immediate_captures(self, board, row, col):
        # How many ways can opponent capture 
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        count = 0
        
        for drow, dcol in directions:
            distance = 1
            while distance < 8:
                attacker_row = row - (drow * distance)
                attacker_col = col - (dcol * distance)
                
                if not (0 <= attacker_row < 8 and 0 <= attacker_col < 8):
                    break
                
                attacker = board.get_piece(attacker_row, attacker_col)
                
                if attacker:
                    if attacker.type == opponent_type:
                        if self.can_piece_capture_position(attacker, row, col, board):
                            count += 1
                    break
                
                distance += 1
        
        return count

    def can_piece_capture_position(self, attacker, target_row, target_col, board):
        # Check if a piece can capture the target position
        row_diff = target_row - attacker.row
        col_diff = target_col - attacker.col
        
        if abs(row_diff) != abs(col_diff):
            return False
        
        distance = abs(row_diff)
        is_king = getattr(attacker, 'is_king', False)
        
        # Men can only capture adjacent pieces
        if not is_king and distance != 1:
            return False
        
        # Kings: check for clear path
        if distance > 1:
            row_step = 1 if row_diff > 0 else -1
            col_step = 1 if col_diff > 0 else -1
            
            for i in range(1, distance):
                check_row = attacker.row + (row_step * i)
                check_col = attacker.col + (col_step * i)
                if board.get_piece(check_row, check_col) is not None:
                    return False
        
        # Check if there's a landing spot after capture
        landing_row = target_row + (1 if row_diff > 0 else -1)
        landing_col = target_col + (1 if col_diff > 0 else -1)
        
        if not (0 <= landing_row < 8 and 0 <= landing_col < 8):
            return False
        
        landing_spot = board.get_piece(landing_row, landing_col)
        return landing_spot is None

    def edge_value(self, row, col):
        # Calculate edge/corner value
        if (row, col) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            return 3  # corner
        if row == 0 or row == 7 or col == 0 or col == 7:
            return 2  # edge
        if row in (1, 6) or col in (1, 6):
            return 1  # near edge
        return 0

    def future_mobility(self, piece, new_row, new_col, board):
        # Number of future moves after moving here
        old_row, old_col = piece.row, piece.col
        piece.row, piece.col = new_row, new_col
        moves = piece.get_legals_moves(board.board)
        piece.row, piece.col = old_row, old_col
        return len(moves)

    def opponent_proximity(self, board, row, col):
        # Aggregate closeness to opponent pieces
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        opp_pieces = board.get_all_pieces(opponent_type)

        prox = 0
        for p in opp_pieces:
            d = abs(row - p.row) + abs(col - p.col)
            if d == 1:
                prox += 5
            elif d == 2:
                prox += 3
            elif d == 3:
                prox += 1
        return prox

    def sacrifice_value(self, board, row, col):
        # Extra value for being multiple capture 
        threats = self.count_immediate_captures(board, row, col)
        if threats >= 2:
            return 3
        if threats == 1:
            return 2
        return 0

    def endgame_value(self, my_count):
        # Simple tiered endgame aggression
        if my_count <= 2:
            return 3
        if my_count <= 3:
            return 2
        return 1

    def trapped_value(self, board, row, col):
        # Fewer escape squares = better
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        escapes = 0

        for drow, dcol in dirs:
            nr, nc = row + drow, col + dcol
            if 0 <= nr < 8 and 0 <= nc < 8 and board.get_piece(nr, nc) is None:
                escapes += 1

        return max(0, 4 - escapes)

    def evaluate_pos(self, board, game_state):
        
        my_pieces = board.get_all_pieces(self.piece_type)
        opponent_type = PoddavkiCons.BLACK_PIECE if self.piece_type == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        opp_pieces = board.get_all_pieces(opponent_type)

        score = 0

        # Fewer own pieces is good
        score -= len(my_pieces) * 100

        # Keep opponent pieces on board
        score += len(opp_pieces) * 50

        # Less mobility is better
        my_mob = sum(len(p.get_legals_moves(board.board)) for p in my_pieces)
        score -= my_mob * 15

        # Close to win
        if len(my_pieces) <= 3:
            score += 800
        if my_mob <= 2:
            score += 1500

        return score