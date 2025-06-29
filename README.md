# PySweeper
## Author: Quinn Leonard

## Description
This is a simple recreation of Minesweeper developed for the Software Developers of Calgary June 2025 Project Based Mini-Hackathon. This game was mainly created as a way for me to learn the pygame library and as such is fairly rough around the edges, but is still a fully functional recreation of Minesweeper that allows for complete customization of the gameboard dimensions as well as the number of mines present.

## Dependencies
- python (3.12.2)
- pygame (2.6.1)
- numpy (1.26.4)

## Running the Game
Once you have the dependencies installed, navigate to the PySweeper directory and run:

```python PySweeper.py```

Optionally, you can include values the board width, height, and bomb count seperated by spaces following ```PySweeper.py``` in order to bypass the "New Game" window.

## Gameplay
The goal of PySweeper is to dig up every tile that doesn't contain a mine. By left clicking a tile, it will be dug up. So long as you didn't dig up a mine, one or more numbered tiles will be revealed. The numbers on these tiles correspond to the number of mines adjacent to each given mine, either vertically, horizontally, or diagonally. By using these numbers as well as a little deductive reasoning, you should be able to determine which tiles are safe to dig up and which ones lead to certain peril. When you discover a tile that you believe contains a mine, right click it to place a flag. Flagging mines isn't strictly necessary for winning the game, but it can help you keep track of the game and prevent you from accidentally detonating mines.

After completing a game (either successfully or... not...), left click to return to the "New Game" window or right click to start a new game with the same parameters. 