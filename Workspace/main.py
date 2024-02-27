import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (200, 200, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
game_over = False

# Game Variables
xpos = 400
ypos = 750
moveLeft = False

while not game_over:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
    # Physics section
    
    if moveLeft == True:
        vx =- 3
    else:
        vx = 0
        
    xpos += vx
    
    # Render Section
    
    screen.fill((BLACK)) # wipe screen
    pygame.draw.rect(screen, (GREEN), (400, 750, 60, 20)) # draw player
    pygame.display.flip()

pygame.quit()
