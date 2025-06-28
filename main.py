import pygame
import sys
import numpy
import utils

# Constants
WIDTH = 10
HEIGHT = 10
BOMBS = 10
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

# Font Setup
pygame.font.init()
valueFont = pygame.font.SysFont('Comic Sans MS', 16)    # Font for tile numbers
scoreFont = pygame.font.SysFont('Comic Sans MS', 18)    # Font for score values

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
    def draw(self, surface):
        
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
                    valueSurface = valueFont.render(str(self.value), False, NUMBERCOLOURS[self.value - 1])
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
            
# Command line arguments
if len(sys.argv) == 4:
    WIDTH = int(sys.argv[1])
    HEIGHT = int(sys.argv[2])
    BOMBS = int(sys.argv[3])
    
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * TILESIZE, (HEIGHT + 2) * TILESIZE))
pygame.display.set_caption("PySweeper")
clock = pygame.time.Clock()
time = 0
running = True
gameOver = False

# Generate map
map = utils.generate_map(WIDTH, HEIGHT, BOMBS)
tiles = [[None] * WIDTH for i in range(HEIGHT)]
remainingBombs = BOMBS
for i in range(HEIGHT):
    for j in range(WIDTH):
        tiles[i][j] = Tile(j, i, map[i][j])

hoveredTile = None

def click(x, y):
    tile = tiles[y][x]
    if tile.clicked:
        return False
    elif tile.value == -1:
        tile.clicked = True
        pygame.display.set_caption("Game Over!")
        for row in tiles:
            for tile in row:
                tile.visible = True
        return True
    elif tile.value > 0:
        tile.clicked = True
        return False
    else:
        tile.clicked = True
        if y > 0:
            if (x > 0): click(x-1, y-1)
            click(x, y-1)
            if (x < (WIDTH - 1)): click(x+1, y-1)
                    
        if (x > 0): click(x-1, y)
        if (x < (WIDTH - 1)): click(x+1, y)
                
        if y < (HEIGHT - 1):
            if (x > 0): click(x-1, y+1)
            click(x, y+1)
            if (x < (WIDTH - 1)): click(x+1, y+1)
        return False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (0 < mouse_x) and (mouse_x < (WIDTH) * TILESIZE) and (0 < mouse_y) and (mouse_y < (HEIGHT) * TILESIZE):
        hoveredTile = tiles[mouse_y // TILESIZE][mouse_x // TILESIZE]
    else: hoveredTile = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (not gameOver) and hoveredTile and (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.button == 1) and (not hoveredTile.flagged): gameOver = click(event.pos[0] // TILESIZE, event.pos[1] // TILESIZE)
            if (event.button == 3):
                if hoveredTile.flagged:
                    remainingBombs += 1
                    hoveredTile.flagged = False
                elif remainingBombs > 0:
                    remainingBombs -= 1
                    hoveredTile.flagged = True
                    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("azure4")

    # RENDER YOUR GAME HERE
        
    scoreRect = pygame.Rect(0, HEIGHT * TILESIZE, WIDTH * TILESIZE, TILESIZE * 2)
    
    if not gameOver: time += clock.get_time()
    pygame.draw.rect(screen, pygame.Color("white"), scoreRect)
    scoreSurface = scoreFont.render("Remaining Bombs: " + str(remainingBombs), False, pygame.Color("black"))
    timeSurface = scoreFont.render("Time: " + str(time // 1000), False, pygame.Color("black"))
    screen.blit(scoreSurface, (TILESIZE // 4, HEIGHT * TILESIZE))
    screen.blit(timeSurface, (TILESIZE // 4, (HEIGHT + 1) * TILESIZE))
        
    if gameOver: hoveredTile = None
    coveredSafeTiles = 0
    for row in tiles:
        for tile in row:
            if (tile.clicked == False) and (tile.value > -1): coveredSafeTiles += 1
            if pygame.mouse.get_focused() and (tile == hoveredTile):
                tile.hovered = True
            else:
                tile.hovered = False
            tile.draw(screen)
    if coveredSafeTiles == 0:
        pygame.display.set_caption("You Win!")
        gameOver = True

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()