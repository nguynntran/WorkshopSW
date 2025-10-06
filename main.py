import pygame
from checkers.board import Board
from checkers.constant import Cons

FPS = 60
screen = pygame.display.set_mode((Cons.COLS * Cons.SQUARE_SIZE, Cons.ROWS * Cons.SQUARE_SIZE))
pygame.display.set_caption("WOLFS AND SHEEP")

def main():
    pygame.init()
    
    board = Board()
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.draw_board(screen)
        pygame.display.flip()
        

    pygame.quit()

if __name__ == "__main__":
    main()