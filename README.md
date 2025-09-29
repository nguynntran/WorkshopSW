# SOFTWAREDEVELOPMENT


## Wolves and Sheep (4 wolves vs 1 sheep) - GUI using Pygame

Rules implemented here :
- Board: 8x8, pieces occupy only dark squares.
- Wolves: 4 pieces, start at the top row on dark squares (row 0, cols 1,3,5,7).
  - Wolves may move only diagonally "forward" 
- Sheep: 1 piece, starts at bottom-left dark square (row 7, col 0).
  - Sheep may move diagonally in any direction by one square.
- No capturing.
- Turns alternate: Wolves (all four controlled by one player) and Sheep (other player).
- Win conditions:
  - Sheep wins if it reaches the top row (row 0).
  - Wolves win if the sheep has no legal moves on sheep's turn.

Controls:
- Click on a piece to select it, then click on a highlighted square to move.
- Wolves move first.