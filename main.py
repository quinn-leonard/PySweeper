import pygame
import sys
import numpy
import utils

# Font Setup
pygame.font.init()
valueFont = pygame.font.SysFont('Comic Sans MS', 16)    # Font for tile numbers
scoreFont = pygame.font.SysFont('Comic Sans MS', 18)    # Font for score values
    
width = 10
height = 10
bombs = 10

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((width * utils.TILESIZE, (height + 2) * utils.TILESIZE))
pygame.display.set_caption("PySweeper")
clock = pygame.time.Clock()
running = True
loss = False
win = False

game = utils.Game(width, height, bombs)

# Gameplay loop
while running:

    # Get mouse position for hovering over tiles
    if (pygame.mouse.get_focused()):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game.hover(mouse_x // utils.TILESIZE, mouse_y // utils.TILESIZE)

    # Poll for events
    for event in pygame.event.get():

        # Quitting
        if event.type == pygame.QUIT:
            running = False

        # Clicking
        if (not game.gameOver) and (event.type == pygame.MOUSEBUTTONDOWN):

            # Left clicking (digging)
            if event.button == 1: 
                loss = game.click(event.pos[0] // utils.TILESIZE, event.pos[1] // utils.TILESIZE)
                win = game.check_for_win()

            # Right clicking (flagging)
            if event.button == 3:
                game.flag(event.pos[0] // utils.TILESIZE, event.pos[1] // utils.TILESIZE)

    # Render frame to screen
    game.draw(screen, valueFont, scoreFont)
    if loss: pygame.display.set_caption("Game Over!")
    if win: pygame.display.set_caption("You Win!")
    pygame.display.flip()

    # Increment timer
    if not game.gameOver: game.time += clock.get_time()
    
    # Limit FPS to 60
    clock.tick(60)

pygame.quit()