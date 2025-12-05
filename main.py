# 

# main.py
import pygame
import sys
from checkers.wolfandsheep.game import WolfAndSheepGame
from checkers.wolfandsheep.bot import WolfBot, SheepBot
from checkers.poddavki.game import PoddavkiGame
from checkers.poddavki.bot import PoddavkiBot
from checkers.poddavki.constant import PoddavkiCons
from checkers.base_classes.base_constants import BaseConstants as Cons

def choose_game():
    print("Choose a game:")
    print("1. Wolves and Sheep")
    print("2. Poddavki (Giveaway Checkers)")
    
    while True:
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            return create_wolf_sheep_game()
        elif choice == "2":
            return create_poddavki_game()  # Now calls create function
        else:
            print("Invalid choice. Please enter 1 or 2.")

def create_wolf_sheep_game():
    print("\nWolves and Sheep Game Setup:")
    print("Choose players:")
    print("1. Human vs Human")
    print("2. Human (Sheep) vs Bot (Wolves)")
    print("3. Human (Wolves) vs Bot (Sheep)")
    print("4. Bot vs Bot")
    
    while True:
        choice = input("Enter 1-4: ")
        
        if choice == "1":
            return WolfAndSheepGame()
        elif choice == "2":
            wolves_bot = WolfBot()  
            return WolfAndSheepGame(wolves_bot=wolves_bot)
        elif choice == "3":
            sheep_bot = SheepBot()  
            return WolfAndSheepGame(sheep_bot=sheep_bot)
        elif choice == "4":
            wolves_bot = WolfBot()
            sheep_bot = SheepBot()
            return WolfAndSheepGame(wolves_bot=wolves_bot, sheep_bot=sheep_bot)
        else:
            print("Invalid choice. Please enter 1-4.")

def create_poddavki_game():
    """NEW: Create Poddavki game with bot options"""
    print("\nPoddavki Game Setup:")
    print("Choose players:")
    print("1. Human vs Human")
    print("2. Human (Red) vs Bot (Black)")
    print("3. Human (Black) vs Bot (Red)")
    print("4. Bot vs Bot")
    
    while True:
        choice = input("Enter 1-4: ")
        
        if choice == "1":
            return PoddavkiGame()
        elif choice == "2":
            black_bot = PoddavkiBot(PoddavkiCons.BLACK_PIECE)
            return PoddavkiGame(black_bot=black_bot)
        elif choice == "3":
            red_bot = PoddavkiBot(PoddavkiCons.RED_PIECE)
            return PoddavkiGame(red_bot=red_bot)
        elif choice == "4":
            red_bot = PoddavkiBot(PoddavkiCons.RED_PIECE)
            black_bot = PoddavkiBot(PoddavkiCons.BLACK_PIECE)
            return PoddavkiGame(red_bot=red_bot, black_bot=black_bot)
        else:
            print("Invalid choice. Please enter 1-4.")

def main():
    pygame.init()
    
    # Choose which game to play
    game = choose_game()
    
    screen = pygame.display.set_mode((Cons.WIDTH, Cons.HEIGHT))
    
    if isinstance(game, WolfAndSheepGame):
        pygame.display.set_caption("Wolves and Sheep")
    else:
        pygame.display.set_caption("Poddavki (Giveaway Checkers)")
    
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(Cons.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.is_game_over():  # Only handle clicks if game not over
                    game.handle_click(event.pos)

        # Update game (handles bot moves) only if game not over
        if hasattr(game, 'update') and not game.is_game_over():
            game.update(dt)

        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()