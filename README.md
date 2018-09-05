# HueDrops Solver
## What is it?
This is a solution for a challenge posted on [/r/dailyprogrammer](https://www.reddit.com/r/dailyprogrammer/comments/7riu6p/20180119_challenge_347_hard_hue_drops_puzzle/).

> The puzzle opens with a group of tiles of six random colors. 
The tile in the upper left remains wild for you to change. 
Tile colors change by flooding from the start tile to directly connected tiles 
in the four cardinal directions (not diagonals). 
Directly connected tiles convert to the new color, allowing you to extend 
the size of the block. 
The puzzle challenges you to sequentially change the color of the root tile
 until you grow the block of tiles to the target color in 25 moves or fewer.
## How does it work?
Basically, at the very start it begins from the top left point and collects
all the border points of colors different from the original color.

Then it iterates over all of these border elements and recursively walks
all the points which are colored the same as this border element. 
The result is stored in a dict.

The path with most visited points is selected as the best path. All the points
of original color are recolored into the color of the best path and all the points
of the new path are added
to the sets of visited elements and border elements.

If a hue is recolored and its walk results are already stored in the dict, 
it is removed 
for further recalculation (because now it has different set of border elements).

The algorithm continues until the visited elements set contains every single hue.