import pygame
import random

pygame.init()

# Constants
width, height = 800, 800
alienWidth, alienHeight = 40, 40
alienRows = 4
AlienCols = 12

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (102, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
gameOver = False

# Game Variables
xpos = 365
ypos = 750
timer = 0
moveLeft = False
moveRight = False


class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isDead = False

    def draw(self):
        pygame.draw.rect(screen, (WHITE), (self.xpos,
                         self.ypos, alienWidth, alienHeight))

    def move(self):
        if timer % 100 == 0:
            self.xpos += 50


armada = []
for row in range(alienRows):
    for col in range(AlienCols):
        armada.append(Alien(col*60+50, row*50+50))

while not gameOver:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        moveRight = True
    else:
        moveRight = False

    if keys[pygame.K_LEFT]:
        moveLeft = True
    else:
        moveLeft = False

    # Physics section
    vx = 0
    vy = 0

    if moveLeft:
        vx = -3

    if moveRight:
        vx = 3

    xpos += vx
    ypos += vy

    # Render Section

    screen.fill((BLACK))  # wipe screen

    for i in range(len(armada)):
        armada[i].draw()

    pygame.draw.rect(screen, (GREEN), (xpos, ypos, 60, 20))  # draw player
    pygame.draw.rect(
        screen, (GREEN), (xpos+20, ypos-10, 20, 10))  # draw player

    pygame.display.flip()

pygame.quit()
