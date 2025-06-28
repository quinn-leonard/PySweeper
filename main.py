import pygame
import sys

WIDTH = 10
HEIGHT = 10

if len(sys.argv) == 3:
    WIDTH = int(sys.argv[1])
    HEIGHT = int(sys.argv[2])
    
# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * 50, HEIGHT * 50))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()