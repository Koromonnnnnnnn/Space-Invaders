import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()

# Constants
width, height = 800, 800
alienWidth, alienHeight = 40, 40
alienRows = 4
alienCols = 12
FPS = 60
lives = 3

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
moveLeft = False
moveRight = False
shoot = False

shootSFX = pygame.mixer.Sound("shoot.wav")

bullets = []
armada = []
walls = []
missiles = []
missile_speed = 5
missile_frequency = 2


class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
        self.move_counter = 0

    def draw(self):
        pygame.draw.rect(screen, (WHITE), (self.xpos,
                                           self.ypos, alienWidth, alienHeight))

    def move(self):
        self.move_counter += 1
        if self.move_counter % 800 == 0:
            self.ypos += 10
            self.direction *= -1
            self.xpos += 10 * self.direction
        elif self.move_counter % 100 == 0:
            self.xpos += 10 * self.direction

        if self.xpos < 0 or self.xpos > width - alienWidth:
            self.direction *= -1

    def check_collision(self, bullet):
        if self.isAlive and bullet.isAlive:
            if self.xpos < bullet.xpos < self.xpos + alienWidth and self.ypos < bullet.ypos < self.ypos + alienHeight:
                self.isAlive = False
                bullet.isAlive = False


class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True

    def move(self):
        if self.isAlive:
            self.ypos -= 5
            if self.ypos < 0:
                self.isAlive = False

    def draw(self):
        pygame.draw.rect(screen, (WHITE), (self.xpos, self.ypos, 3, 20))


class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0

    def draw(self):
        if self.numHits == 0:
            pygame.draw.rect(screen, (250, 250, 20),
                             (self.xpos, self.ypos, 30, 30))
        if self.numHits == 1:
            pygame.draw.rect(screen, (150, 150, 10),
                             (self.xpos, self.ypos, 30, 30))
        if self.numHits == 2:
            pygame.draw.rect(screen, (50, 50, 0),
                             (self.xpos, self.ypos, 30, 30))

    def check_collision(self, bullet):
        if self.numHits < 3 and bullet.isAlive:
            if self.xpos < bullet.xpos < self.xpos + alienWidth and self.ypos < bullet.ypos < self.ypos + alienHeight:
                self.numHits += 1
                bullet.isAlive = False


class missileConstructor:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False

    def move(self):
        if self.isAlive:
            self.ypos += missile_speed
            if self.ypos > height:
                self.isAlive = False

    def draw(self):
        pygame.draw.rect(screen, (WHITE), (self.xpos, self.ypos, 3, 20))


for row in range(alienRows):
    for col in range(alienCols):
        armada.append(Alien(col * 60 + 50, row * 50 + 50))

for k in range(4):
    for i in range(2):
        for j in range(3):
            # Push wall objects into list
            walls.append(Wall(j*30+200*k+50, i*30+600))

while not gameOver:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
    if lives == 0:
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

    if keys[pygame.K_SPACE]:
        shoot = True
        pygame.mixer.Sound.play(shootSFX)
    else:
        shoot = False

    # Player movement
    if moveLeft and xpos > 0:
        xpos -= 5
    if moveRight and xpos < width - 60:
        xpos += 5

    # Bullet shooting
    if shoot:
        bullets.append(Bullet(xpos + 28, ypos))

    # Update bullet positions
    for bullet in bullets:
        bullet.move()

    # Update alien positions
    for alien in armada:
        alien.move()
        for bullet in bullets:
            alien.check_collision(bullet)

    # Update wall
    for wall in walls:
        for bullet in bullets:
            wall.check_collision(bullet)  # check if player bullets hit wall

    for wall in walls:
        for missile in missiles:
            wall.check_collision(missile)  # check if alien bullets hit wall

    # Update missile
    for missile in missiles:
        missile.move()

    chance = random.randrange(100)
    if chance < missile_frequency:
        pick = random.randrange(len(armada))
        if armada[pick].isAlive == True:
            missile = missileConstructor()
            missile.isAlive = True
            missile.xpos = armada[pick].xpos + 5
            missile.ypos = armada[pick].ypos
            missiles.append(missile)

    for i in range(len(missiles)):  # Check if missile hits plater
        if missiles[i].isAlive:
            if missiles[i].xpos > xpos:
                if missiles[i].xpos < xpos + 40:
                    if missiles[i].ypos < ypos + 40:
                        if missiles[i].ypos > ypos:
                            lives -= 1
                            # print(lives)

    for i in range(len(armada)):  # Check if alien hits player
        if armada[i].isAlive:
            if armada[i].xpos > xpos:
                if armada[i].xpos < xpos + 40:
                    if armada[i].ypos < ypos + 40:
                        if armada[i].ypos > ypos:
                            gameOver = True

    # Render Section
    screen.fill((BLACK))

    for alien in armada:
        if alien.isAlive:
            alien.draw()

    for bullet in bullets:
        if bullet.isAlive:
            bullet.draw()

    for missile in missiles:
        if missile.isAlive:
            missile.draw()

    for wall in walls:
        wall.draw()

    pygame.draw.rect(screen, (GREEN), (xpos, ypos, 60, 20))
    pygame.draw.rect(screen, (GREEN), (xpos + 20, ypos - 10, 20, 10))

    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES:', False, (WHITE))

    screen.blit(text_surface, (0, 0))

    pygame.display.flip()

print("Game Over")
pygame.quit()
