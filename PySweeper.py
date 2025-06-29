# File: PySweeper.py
# Author: Quinn Leonard
#
# PySweeper runnable file.
# This file contains the main gameplay loop for PySweeper

import pygame
import PySweeperUtils
import NewGame
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

        if (width not in range(1, 101)) or (height not in range(1, 101)) or (bombs not in range(0, width*height)):
            width, height, bombs = NewGame.get_board_parameters()
    except:
        width, height, bombs = NewGame.get_board_parameters()
else:
    width, height, bombs = NewGame.get_board_parameters()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((width * PySweeperUtils.TILESIZE, (height + 2) * PySweeperUtils.TILESIZE))
pygame.display.set_caption("PySweeper")
clock = pygame.time.Clock()
running = True
game = PySweeperUtils.Game(width, height, bombs)
loss = win = False

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game.gameOver:
                # Left clicking (digging)
                if event.button == 1: 
                    loss = game.click(event.pos[0] // PySweeperUtils.TILESIZE, event.pos[1] // PySweeperUtils.TILESIZE)
                    win = game.check_for_win()

                # Right clicking (flagging)
                if event.button == 3:
                    game.flag(event.pos[0] // PySweeperUtils.TILESIZE, event.pos[1] // PySweeperUtils.TILESIZE)
            else:
                # Left clicking (reset with new parameters)
                if event.button == 1:
                    pygame.display.quit()
                    width, height, bombs = NewGame.get_board_parameters()
                    screen = pygame.display.set_mode((width * PySweeperUtils.TILESIZE, (height + 2) * PySweeperUtils.TILESIZE))
                    pygame.display.set_caption("PySweeper")
                    game = PySweeperUtils.Game(width, height, bombs)
                    game.time = pygame.time.get_ticks()
                    loss = win = False
                    

                # Right clicking (reset with same parameters)
                if event.button == 3:
                    pygame.display.set_caption("PySweeper")
                    game = PySweeperUtils.Game(width, height, bombs)
                    game.time = pygame.time.get_ticks()
                    loss = win = False

    # Render frame to screen
    game.draw(screen, valueFont, scoreFont)
    if loss: pygame.display.set_caption("Game Over!")
    if win: pygame.display.set_caption("You Win!")
    pygame.display.flip()

    # Increment timer
    if not game.gameOver: game.elapsed_time = (pygame.time.get_ticks() - game.start_ticks)
    
    # Limit FPS to 60
    clock.tick(60)

pygame.quit()