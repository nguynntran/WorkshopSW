import pygame

class BaseConstants:
    #Base constants shared fors all games
    
    # Board dimensions
    ROWS = 8
    COLS = 8
    SQUARE_SIZE = 80
    WIDTH = COLS * SQUARE_SIZE
    HEIGHT = ROWS * SQUARE_SIZE
    
    # Common colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)
    YELLOW = (255, 255, 0)
    
    # UI colors
    SELECT = (0, 255, 255)  
    HIGHLIGHT = WHITE
    
    # Game settings
    FPS = 60
    FONT_SIZE = 36
    
    # Empty square
    EMP = 0