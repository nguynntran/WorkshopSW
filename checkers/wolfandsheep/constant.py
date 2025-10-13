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