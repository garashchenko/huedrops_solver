# HueDrops Solver
## What is it?
This is a solution for a challenge posted on [/r/dailyprogrammer](https://www.reddit.com/r/dailyprogrammer/comments/7riu6p/20180119_challenge_347_hard_hue_drops_puzzle/).

> The puzzle opens with a group of tiles of six random colors. The tile in the upper left remains wild for you to change. Tile colors change by flooding from the start tile to directly connected tiles in the four cardinal directions (not diagonals). Directly connected tiles convert to the new color, allowing you to extend the size of the block. The puzzle challenges you to sequentially change the color of the root tile until you grow the block of tiles to the target color in 25 moves or fewer.
## How does it work?
Basically, it starts from the top left point of the puzzle grid and walks all the other points of the same color to collect all the possible border points of other colors to later choose from.
Then it iterates over all of these border elements and uses the same method to walk all the points of a certain color. The result is stored in a dict. 
Now all we have to do is choose a path with the biggest count of visited elements!