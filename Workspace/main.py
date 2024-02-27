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
gameOver = False

# Game Variables
xpos = 800
ypos = 800
moveLeft = False
moveRight = False

while not gameOver:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        moveRight = True
    if keys[pygame.K_LEFT]:
        moveLeft = True
            
    # Physics section
    
    if moveLeft == True:
        vx =- 3
    else:
        vx = 0
        
    if moveRight == True:
        vy += 3
    else:
        vy = 0
        
    xpos += vx
    ypos += vy
    
    # Render Section
    
    screen.fill((BLACK)) # wipe screen
    pygame.draw.rect(screen, (GREEN), (400, 750, 60, 20)) # draw player
    pygame.display.flip()

pygame.quit()
