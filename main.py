import pygame
from checkers.board import Board
from checkers.constant import Cons

def main():
    pygame.init()
    screen = pygame.display.set_mode((Cons.COLS * Cons.SQUARE_SIZE, Cons.ROWS * Cons.SQUARE_SIZE))
    pygame.display.set_caption("Checkers Game")

    board = Board()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.draw_board(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()