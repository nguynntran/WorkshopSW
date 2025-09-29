import pygame
from .constant import Cons

class Piece:
    def __init__(self, piece_type, row, col):
        self.type = piece_type
        self.row = row
        self.col = col
        self.x = col * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2
        self.y = row * Cons.SQUARE_SIZE + Cons.SQUARE_SIZE // 2
        self.radius = Cons.SQUARE_SIZE // 2 - 10
        
    def draw(self, screen):
        """Draw the piece on the screen"""
        # Draw piece shadow
        pygame.draw.circle(screen, Cons.BLACK, 
                         (self.x + 3, self.y + 3), self.radius)
        
        # Draw main piece
        if self.type == Cons.WOLF:
            pygame.draw.circle(screen, Cons.WOLF_COLOR, 
                             (self.x, self.y), self.radius)
            # Add wolf marking
            pygame.draw.circle(screen, Cons.BLACK, 
                             (self.x, self.y), self.radius, 3)
        elif self.type == Cons.SHEEP:
            pygame.draw.circle(screen, Cons.SHEEP_COLOR, 
                             (self.x, self.y), self.radius)
            # Add sheep marking
            pygame.draw.circle(screen, Cons.BLACK, 
                             (self.x, self.y), self.radius, 2)
    
    def get_position(self):
        """Get current position as tuple"""
        return (self.row, self.col)
    
    def __str__(self):
        return f"{self.type.capitalize()} at ({self.row}, {self.col})"