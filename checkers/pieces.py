import pygame
from .constant import Cons

class Piece:
    def __init__(self, piece_type, row, col):
        self.type = piece_type
        self.row = row
        self.col = col
        
    def draw(self, screen):
        
        center = (self.col * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2,
                  self.row * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2)
        
        radius = Cons.SQUARE_SIZE // 2 - 10

        

        # Draw main piece
        if self.type == Cons.WOLF:
            pygame.draw.circle(screen, Cons.WOLF_COLOR, 
                             center , radius)
            # Wolf marking
            pygame.draw.circle(screen, Cons.BLACK, 
                             center, radius, 3)
        elif self.type == Cons.SHEEP:
            pygame.draw.circle(screen, Cons.SHEEP_COLOR, 
                             center, radius)
            # Sheep marking
            pygame.draw.circle(screen, Cons.BLACK, 
                             center, radius, 2)
            
    # Get legal moves based on piece type and position
    def get_legal_moves(self, board):
        moves = []
        if self.type == Cons.WOLF:
            for dcol in [-1, 1]:
                nrow, ncol = self.row + 1, self.col + dcol
                if (0 <= nrow < Cons.ROWS and 0 <= ncol < Cons.COLS and 
                    board[nrow][ncol] is None and (nrow + ncol) % 2 == 1):
                    moves.append((nrow, ncol))
        elif self.type == Cons.SHEEP:
            for drow in [-1, 1]:
                for dcol in [-1, 1]:
                    nrow, ncol = self.row + drow, self.col + dcol
                    if (0 <= nrow < Cons.ROWS and 0 <= ncol < Cons.COLS and 
                        board[nrow][ncol] is None and (nrow + ncol) % 2 == 1):
                        moves.append((nrow, ncol))
        return moves
    
    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
    