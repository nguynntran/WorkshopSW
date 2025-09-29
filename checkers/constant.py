import pygame

class Cons:
    # Board dimensions
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQUARE_SIZE = 80
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GRAY = (128, 128, 128)
    SELECT = (0, 255, 255)  # Cyan for selection
    
    # Piece types
    WOLF = "wolf"
    SHEEP = "sheep"
    
    # Piece colors
    WOLF_COLOR = GRAY
    SHEEP_COLOR = WHITE
    
    # Game settings
    FPS = 60