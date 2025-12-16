import pygame
from ..base_classes.base_constants import BaseConstants 

class WASCons:
    # Piece types (using numbers)
    WOLF = 1
    SHEEP = 2
    
    # Piece colors
    WOLF_COLOR = BaseConstants.GRAY
    SHEEP_COLOR = BaseConstants.WHITE
    
    # Players (can still use strings for clarity)
    WOLVES_PLAYER = "wolves"
    SHEEP_PLAYER = "sheep"
    
    MAX_MOVES = 100

    # Initial setup positions
    WOLVES_START_ROW = 0
    WOLVES_START_COLS = [1, 3, 5, 7] 
    
    SHEEP_START_ROW = 7
    SHEEP_START_COL = 0  
