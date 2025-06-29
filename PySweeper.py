# File: PySweeper.py
# Author: Quinn Leonard
#
# PySweeper runnable file.
# This file contains the main gameplay loop for PySweeper

import pygame
import PySweeperUtils
import sys

# Font Setup
pygame.font.init()
valueFont = pygame.font.SysFont('Comic Sans MS', 16)    # Font for tile numbers
scoreFont = pygame.font.SysFont('Comic Sans MS', 18)    # Font for score values

# Default board parameters    
width = 10
height = 10
bombs = 10

# Command line arguments
if len(sys.argv) == 4:
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        bombs = int(sys.argv[3])
    except:
        width = 10
        height = 10
        bombs = 10

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((width * PySweeperUtils.TILESIZE, (height + 2) * PySweeperUtils.TILESIZE))
pygame.display.set_caption("PySweeper")
clock = pygame.time.Clock()
running = True
game = PySweeperUtils.Game(width, height, bombs)
loss = False
win = False

# Gameplay loop
while running:

    # Get mouse position for hovering over tiles
    if (pygame.mouse.get_focused()):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game.hover(mouse_x // PySweeperUtils.TILESIZE, mouse_y // PySweeperUtils.TILESIZE)

    # Poll for events
    for event in pygame.event.get():

        # Quitting
        if event.type == pygame.QUIT:
            running = False

        # Clicking
        if (not game.gameOver) and (event.type == pygame.MOUSEBUTTONDOWN):

            # Left clicking (digging)
            if event.button == 1: 
                loss = game.click(event.pos[0] // PySweeperUtils.TILESIZE, event.pos[1] // PySweeperUtils.TILESIZE)
                win = game.check_for_win()

            # Right clicking (flagging)
            if event.button == 3:
                game.flag(event.pos[0] // PySweeperUtils.TILESIZE, event.pos[1] // PySweeperUtils.TILESIZE)

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