# File: PySweeperUtils.py
# Author: Quinn Leonard
#
# Utilities file for PySweeper
# This file contains a few constants as well as the code for the Tile and Game classes.
# Most of the gameplay logic, such as map generation, win/loss detection, and rendering
# is contained within this file.

import pygame
import numpy

# Side length of each tile in pixels
TILESIZE = 30

# Array of colours for the tile numbers
NUMBERCOLOURS = [pygame.Color("blue"),          # 1
                 pygame.Color("forestgreen"),   # 2 
                 pygame.Color("red"),           # 3
                 pygame.Color("blue4"),         # 4
                 pygame.Color("brown4"),        # 5
                 pygame.Color("cadetblue"),     # 6
                 pygame.Color("black"),         # 7
                 pygame.Color("gold")]          # 8


# Tile
# Class for maintaining an individual tile
# Extends pygame.Rect
#   
# Attributes:
#   x: X-coordinate in the grid
#   y: Y-coordinate in the grid
#   value: Number of mines the tile is touching. Mines have a value of -1
class Tile(pygame.Rect):
    def __init__(self, x, y, value):
        # Define rect dimensions
        super().__init__(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        
        # Initialize attributes
        self.value = value
        self.clicked = False
        self.hovered = False
        self.flagged = False
        self.visible = False
        
        # Define bounding rect for drawing flags and bounding boxes
        self.flagRect = pygame.Rect(x * TILESIZE + (TILESIZE // 4), y * TILESIZE + (TILESIZE // 4), TILESIZE // 2, TILESIZE // 2)

    # draw(self, surface, font)
    # Method for drawing a tile to the screen
    #
    # Arguments:
    #   surface: Surface to draw the tile to
    #   font: Font to use for drawing numbers on clicked tiles
    def draw(self, surface, font):
        
        # Visible tiles
        if (self.clicked == True) or (self.visible == True):
            
            # Mines
            if self.value == -1:
                if self.clicked == True:
                    pygame.draw.rect(surface, pygame.Color("red"), self)
                else:
                    pygame.draw.rect(surface, pygame.Color("azure4"), self)
                pygame.draw.ellipse(surface, pygame.Color("black"), self.flagRect)
                
            # Safe tiles
            else:    
                pygame.draw.rect(surface, pygame.Color("azure4"), self)
                if (self.value > 0):
                    valueSurface = font.render(str(self.value), False, NUMBERCOLOURS[self.value - 1])
                    surface.blit(valueSurface, (self.x + (TILESIZE // 3),self.y))
                    
        # Invisible tiles
        else:
            
            # Plain Tiles
            if (self.hovered == False) or (self.flagged == True):
                pygame.draw.rect(surface, pygame.Color("azure2"), self)
                pygame.draw.rect(surface, pygame.Color("azure3"), self, width=5)
                
            # Hovered Tiles
            else:
                pygame.draw.rect(surface, pygame.Color("azure3"), self)
                
            # Flagged Tiles
            if self.flagged:
                pygame.draw.ellipse(surface, pygame.Color("red"), self.flagRect)

# Game
# Class for maintaining a game board
#   
# Attributes:
#   width: Number of tiles in each row
#   height: Number of tiles in each column
#   remainingBombs: Number of unmarked mines remaining in the board
#   time: Time in seconds since the start of the game
#   hoveredTile: Tile the mouse is currently hovering over
#   gameOver: Boolean representation of whether the game is still in play
#   map: 2D array containing a map of the game tiles
class Game():
    def __init__(self, width, height, bombs):
        # Initialize attributes
        self.width = width
        self.height = height
        self.remainingBombs = bombs
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.hoveredTile = None
        self.gameOver = False
        self.map = [[None] * width for i in range(height)]

        # Define a zero-filled numpy array with the same dimensions of the game map
        valueMap = numpy.zeros((height, width), dtype=int)

        # Place the mines at the start of the value map
        for i in range(bombs):
            valueMap[i // width][i % width] = -1

        # Shuffle the mine placements
        numpy.random.seed()
        numpy.random.shuffle(valueMap.ravel())

        # Iterate through each element in the value map
        for i in range(height):
            for j in range(width):

                # Iterate the value of each non-mine entry for each adjacent mine
                if valueMap[i][j] > -1:

                    # Tiles above
                    if i > 0:
                        if (j > 0) and (valueMap[i-1][j-1] == -1): valueMap[i][j] += 1
                        if (valueMap[i-1][j] == -1): valueMap[i][j] += 1
                        if (j < (width - 1)) and (valueMap[i-1][j+1] == -1): valueMap[i][j] += 1
                    
                    # Lateral tiles
                    if (j > 0) and (valueMap[i][j-1] == -1): valueMap[i][j] += 1
                    if (j < (width - 1)) and (valueMap[i][j+1] == -1): valueMap[i][j] += 1
                    
                    # Tiles below
                    if i < (height - 1):
                        if (j > 0) and (valueMap[i+1][j-1] == -1): valueMap[i][j] += 1
                        if (valueMap[i+1][j] == -1): valueMap[i][j] += 1
                        if (j < (width - 1)) and (valueMap[i+1][j+1] == -1): valueMap[i][j] += 1
                
                # Define a tile with the current value and add it to the map
                self.map[i][j] = Tile(j, i, valueMap[i][j])

    # draw(self, surface, tileFont, scoreFont)
    # Method for rendering the current gamestate to the screen
    #
    # Arguments:
    #   surface: Surface to draw the game on
    #   tileFont: Font to use for drawing numbers on clicked tiles
    #   scoreFont: Font used for drawing the footer values
    def draw(self, surface, tileFont, scoreFont):
        # Render score in footer
        scoreRect = pygame.Rect(0, self.height * TILESIZE, self.width * TILESIZE, TILESIZE * 2)
        pygame.draw.rect(surface, pygame.Color("white"), scoreRect)
        scoreSurface = scoreFont.render("Remaining Bombs: " + str(self.remainingBombs), False, pygame.Color("black"))
        timeSurface = scoreFont.render("Time: " + str(self.elapsed_time // 1000), False, pygame.Color("black"))
        surface.blit(scoreSurface, (TILESIZE // 4, self.height * TILESIZE))
        surface.blit(timeSurface, (TILESIZE // 4, (self.height + 1) * TILESIZE))

        # Render tiles
        for row in self.map:
            for tile in row:
                if pygame.mouse.get_focused() and (tile == self.hoveredTile):
                    tile.hovered = True
                else:
                    tile.hovered = False
                tile.draw(surface, tileFont)
        
    # click(x_index, y_index)
    # Function for digging a tile
    #
    # Arguments:
    #   x_index: X-coordinate of clicked tile
    #   y_index: Y-coordinate of clicked tile
    #
    # Returns a boolean representation of whether the click caused the game to be lost
    def click(self, x_index, y_index):

        # Return false if click out of bounds
        if (x_index < 0) or (x_index >= self.width) or (y_index < 0) or (y_index >= self.height):
            return False

        # Get clicked tile
        tile = self.map[y_index][x_index]

        # Base case: if tile is clicked or flagged already, return false
        if tile.clicked or tile.flagged:
            return False
        
        # Base case: if tile contains mine, reveal board, set game over, and return true
        elif tile.value == -1:
            tile.clicked = True
            for row in self.map:
                for tile in row:
                    tile.visible = True
            self.gameOver = True
            return True
        
        # Base case: if tile is adjacent to a mine(s), mark as clicked and return
        elif tile.value > 0:
            tile.clicked = True
            return False
        
        # Recursive case: if tile isn't adjacent to any mines, mark as clicked and recurse on the surrounding tiles and return false
        else:
            tile.clicked = True

            # Tiles above
            self.click(x_index-1, y_index-1)
            self.click(x_index, y_index-1)
            self.click(x_index+1, y_index-1)

            # Lateral tiles    
            self.click(x_index-1, y_index)
            self.click(x_index+1, y_index)

            # Tiles below
            self.click(x_index-1, y_index+1)
            self.click(x_index, y_index+1)
            self.click(x_index+1, y_index+1)

            return False

    # flag(x_index, y_index)
    # Function for flagging a tile
    #
    # Arguments:
    #   x_index: X-coordinate of flagged tile
    #   y_index: Y-coordinate of flagged tile
    def flag(self, x_index, y_index):
        if (x_index >= 0) and (x_index < self.width) and (y_index >= 0) and (y_index < self.height):
            tile = self.map[y_index][x_index]
            if not tile.clicked:
                if tile.flagged:
                    self.remainingBombs += 1
                    tile.flagged = False
                elif self.remainingBombs > 0:
                    self.remainingBombs -= 1
                    tile.flagged = True

    # hover(x_index, y_index)
    # Function for hovering over a tile
    #
    # Arguments:
    #   x_index: X-coordinate of hovered tile
    #   y_index: Y-coordinate of hovered tile
    def hover(self, x_index, y_index):
        if (x_index >= 0) and (x_index < self.width) and (y_index >= 0) and (y_index < self.height) and (not self.gameOver):
            self.hoveredTile = self.map[y_index][x_index]
        else:
            self.hoveredTile = None
    
    # check_for_win()
    # Function for checking for a win
    #
    # Returns a boolean representation of whether the game has been won
    def check_for_win(self):

        # Iterate through each tile on the board and count how many unclicked non-mine tiles remain
        coveredSafeTiles = 0
        for row in self.map:
            for tile in row:
                if (tile.value > -1) and (not tile.clicked): coveredSafeTiles += 1
        
        # If no more unclicked safe tiles remain, the game has been won
        if coveredSafeTiles == 0:
            self.gameOver = True
            return True
        else:
            return False