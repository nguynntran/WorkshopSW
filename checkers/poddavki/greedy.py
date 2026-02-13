import sys
import os
import random

from checkers.poddavki.opt_bot import OptimizedPoddavkiBot
from checkers.poddavki.constant import PoddavkiCons
from checkers.poddavki.board import Board

class ParameterOptimizer:
    def __init__(self):
        self.param_ranges = {
            "capture_bonus": [80, 100, 120, 140, 160, 180, 200, 220],
            "capture_penalty": [-40, -60, -80, -100, -120, -140, -160],
            "edge_bonus": [15, 20, 25, 30, 35, 40, 45, 50, 55],
            "center_bonus": [2, 4, 6, 8, 10, 12, 14],
            "mobility_penalty": [-5, -8, -10, -12, -14, -16, -18, -20, -25],
            "proximity_bonus": [5, 8, 10, 12, 14, 16, 18, 20],
            "sacrifice_bonus": [30, 40, 50, 60, 70, 80, 90, 100],
            "endgame_bonus": [30, 40, 50, 60, 70, 80, 90],
            "trapped_bonus": [15, 20, 25, 30, 35, 40, 45, 50],
            "win_score": [10000]
        }
        
        self.baseline_weights = {
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
        
        self.population = []
    
    def genetic_search(self, population_size=8, generations=10, games_per_match=10):
        print("Genetic Optimization")
        
        # Create initial population
        self.population = [self.baseline_weights.copy()]
        
        for i in range(population_size - 1):
            individual = {}
            for param, values in self.param_ranges.items():
                individual[param] = random.choice(values)
            self.population.append(individual)
        
        best_overall = self.baseline_weights.copy()
        best_score = 0
        
        # Evolution loop
        for gen in range(generations):
            print(f"\nGen {gen + 1}/{generations}")
            
            # Test each bot
            scores = []
            for i, bot in enumerate(self.population):
                wins = 0
                for _ in range(3):
                    opp_idx = random.choice([j for j in range(len(self.population)) if j != i])
                    wins += self.run_matches(bot, self.population[opp_idx], games_per_match)
                
                score = wins / (3 * games_per_match)
                scores.append((i, score, bot))
                print(f"  Bot {i+1}: {score:.0%}")
            
            # Sort best to worst
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Update champion
            if scores[0][1] > best_score:
                best_overall = scores[0][2].copy()
                best_score = scores[0][1]
                print(f"  ✓ New best: {best_score:.0%}")
            
            # Keep top half
            survivors = [bot for _, _, bot in scores[:population_size//2]]
            
            # Create new generation
            new_pop = survivors.copy()
            
            while len(new_pop) < population_size:
                p1 = random.choice(survivors)
                p2 = random.choice(survivors)
                child = self.crossover(p1, p2)
                
                if random.random() < 0.3:
                    child = self.mutate(child)
                
                new_pop.append(child)
            
            self.population = new_pop
        
        # Print results
        print("\n" + "=" * 40)
        print("BEST WEIGHTS:")
        for param, value in best_overall.items():
            baseline = self.baseline_weights[param]
            if value != baseline:
                print(f"  {param}: {baseline} → {value}")
        
        return best_overall
    
    def crossover(self, p1, p2):
        child = {}
        for param in p1.keys():
            child[param] = p1[param] if random.random() < 0.5 else p2[param]
        return child
    
    def mutate(self, bot):
        mutant = bot.copy()
        param = random.choice([p for p in self.param_ranges.keys() if p != "win_score"])
        mutant[param] = random.choice(self.param_ranges[param])
        return mutant
    
    def run_matches(self, w1, w2, num_games):
        wins = 0
        
        for game in range(num_games):
            if game % 2 == 0:
                winner = self.play_game(w1, w2)
                if winner == PoddavkiCons.BLACK_PIECE:
                    wins += 1
                elif winner is None:
                    wins += 0.5
            else:
                winner = self.play_game(w2, w1)
                if winner == PoddavkiCons.RED_PIECE:
                    wins += 1
                elif winner is None:
                    wins += 0.5
        
        return wins
    
    def play_game(self, red_w, black_w, max_moves=200):
        # Create bots
        class RedBot(OptimizedPoddavkiBot):
            def __init__(self):
                super().__init__(PoddavkiCons.RED_PIECE)
                self.weights = red_w
        
        class BlackBot(OptimizedPoddavkiBot):
            def __init__(self):
                super().__init__(PoddavkiCons.BLACK_PIECE)
                self.weights = black_w
        
        board = Board()
        red = RedBot()
        black = BlackBot()
        turn = PoddavkiCons.RED_PIECE
        moves = []
        
        for _ in range(max_moves):
            bot = red if turn == PoddavkiCons.RED_PIECE else black
            move = bot.get_best_move(board, None)
            
            if not move:
                return turn
            
            piece, (nr, nc) = move
            or_, oc = piece.row, piece.col
            
            # Track for loops
            moves.append((or_, oc, nr, nc, turn))
            if len(moves) > 10:
                moves.pop(0)
            
            # Check loop
            if len(moves) >= 6:
                if (moves[-1] == moves[-3] == moves[-5] and
                    moves[-2] == moves[-4] == moves[-6]):
                    return None
            
            # Execute move
            if abs(nr - or_) == 2:
                mr = (or_ + nr) // 2
                mc = (oc + nc) // 2
                board.board[mr][mc] = None
            
            board.board[or_][oc] = None
            board.board[nr][nc] = piece
            piece.row = nr
            piece.col = nc
            
            # King promotion
            if not piece.is_king:
                if (piece.type == PoddavkiCons.RED_PIECE and nr == 0) or \
                   (piece.type == PoddavkiCons.BLACK_PIECE and nr == 7):
                    piece.is_king = True
            
            # Check win
            red_p = board.get_all_pieces(PoddavkiCons.RED_PIECE)
            black_p = board.get_all_pieces(PoddavkiCons.BLACK_PIECE)
            
            if len(red_p) == 0 or not any(p.get_legals_moves(board.board) for p in red_p):
                return PoddavkiCons.RED_PIECE
            if len(black_p) == 0 or not any(p.get_legals_moves(board.board) for p in black_p):
                return PoddavkiCons.BLACK_PIECE
            
            turn = PoddavkiCons.BLACK_PIECE if turn == PoddavkiCons.RED_PIECE else PoddavkiCons.RED_PIECE
        
        return None


if __name__ == "__main__":
    opt = ParameterOptimizer()
    
    best = opt.genetic_search(population_size=8, generations=5, games_per_match=10)
    
    # Save to file
    with open("best_weights.txt", 'w') as f:
        for param, value in best.items():
            f.write(f'"{param}": {value},\n')
    
    print("\n✓ Saved to best_weights.txt")