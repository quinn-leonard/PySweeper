import pygame
import numpy

# Constants
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

    # draw(self, surface)
    # Method for drawing a tile to the screen
    #
    # Arguments:
    #   surface: Surface to draw the tile to
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

class Game():
    def __init__(self, width, height, bombs):
        self.width = width
        self.height = height
        self.remainingBombs = bombs
        self.time = 0
        self.hoveredTile = None
        self.gameOver = False

        valueMap = numpy.zeros((height, width), dtype=int)
        for i in range(bombs):
            valueMap[i // width][i % width] = -1
        numpy.random.seed()
        numpy.random.shuffle(valueMap.ravel())

        self.map = [[None] * width for i in range(height)]
        for i in range(height):
            for j in range(width):
                if valueMap[i][j] > -1:
                    if i > 0:
                        if (j > 0) and (valueMap[i-1][j-1] == -1): valueMap[i][j] += 1
                        if (valueMap[i-1][j] == -1): valueMap[i][j] += 1
                        if (j < (width - 1)) and (valueMap[i-1][j+1] == -1): valueMap[i][j] += 1
                        
                    if (j > 0) and (valueMap[i][j-1] == -1): valueMap[i][j] += 1
                    if (j < (width - 1)) and (valueMap[i][j+1] == -1): valueMap[i][j] += 1
                    
                    if i < (height - 1):
                        if (j > 0) and (valueMap[i+1][j-1] == -1): valueMap[i][j] += 1
                        if (valueMap[i+1][j] == -1): valueMap[i][j] += 1
                        if (j < (width - 1)) and (valueMap[i+1][j+1] == -1): valueMap[i][j] += 1
                
                self.map[i][j] = Tile(j, i, valueMap[i][j])

    def draw(self, surface, tileFont, scoreFont):
        # Render score in footer
        scoreRect = pygame.Rect(0, self.height * TILESIZE, self.width * TILESIZE, TILESIZE * 2)
        pygame.draw.rect(surface, pygame.Color("white"), scoreRect)
        scoreSurface = scoreFont.render("Remaining Bombs: " + str(self.remainingBombs), False, pygame.Color("black"))
        timeSurface = scoreFont.render("Time: " + str(self.time // 1000), False, pygame.Color("black"))
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
        
    # click(x, y)
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
    
    def flag(self, x_index, y_index):
        if (x_index > 0) and (x_index < self.width) and (y_index > 0) and (y_index < self.height):
            tile = self.map[y_index][x_index]
            if not tile.clicked:
                if tile.flagged:
                    self.remainingBombs += 1
                    tile.flagged = False
                elif self.remainingBombs > 0:
                    self.remainingBombs -= 1
                    tile.flagged = True
    
    def hover(self, x_index, y_index):
        if (x_index > 0) and (x_index < self.width) and (y_index > 0) and (y_index < self.height) and (not self.gameOver):
            self.hoveredTile = self.map[y_index][x_index]
        else:
            self.hoveredTile = None
    
    def check_for_win(self):
        coveredSafeTiles = 0
        for row in self.map:
            for tile in row:
                if (tile.value > -1) and (not tile.clicked): coveredSafeTiles += 1
        
        if coveredSafeTiles == 0:
            self.gameOver = True
            return True
        else:
            return False