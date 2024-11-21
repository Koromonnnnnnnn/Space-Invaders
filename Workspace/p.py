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
shootCooldown = 20
cooldownTimer = 0
numAliensAlive = alienCols * alienRows

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (102, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders - Rise of Eminem")
clock = pygame.time.Clock()
gameOver = False

# Initialize joystick
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

# Game Variables
xpos = 365
ypos = 750
moveLeft = False
moveRight = False
shoot = False

shootSFX = pygame.mixer.Sound("shoot.wav")
music = pygame.mixer.music.load('01.mp3')
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

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
        self.alien = pygame.image.load('alien.png')
        self.alien = pygame.transform.scale(self.alien, (40, 40))

    def draw(self):
        screen.blit(self.alien, (self.xpos, self.ypos, alienWidth, alienHeight))

    def move(self):
        self.move_counter += 1
        if self.move_counter % 800 == 0:
            self.ypos += 40
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
        pygame.draw.rect(screen, WHITE, (self.xpos, self.ypos, 3, 20))


class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0

    def draw(self):
        colors = [(250, 250, 20), (150, 150, 10), (50, 50, 0)]
        if self.numHits < 3:
            pygame.draw.rect(screen, colors[self.numHits], (self.xpos, self.ypos, 30, 30))

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
        pygame.draw.rect(screen, WHITE, (self.xpos, self.ypos, 3, 20))


for row in range(alienRows):
    for col in range(alienCols):
        armada.append(Alien(col * 60 + 50, row * 50 + 50))

for k in range(4):
    for i in range(2):
        for j in range(3):
            walls.append(Wall(j * 30 + 200 * k + 50, i * 30 + 600))

while not gameOver:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    if lives == 0 or numAliensAlive == 0:
        gameOver = True

    # Keyboard input
    keys = pygame.key.get_pressed()
    moveLeft = keys[pygame.K_LEFT]
    moveRight = keys[pygame.K_RIGHT]
    if keys[pygame.K_SPACE] and cooldownTimer <= 0:
        shoot = True
        cooldownTimer = shootCooldown
        pygame.mixer.Sound.play(shootSFX)
    else:
        shoot = False

    # Controller input
    if joystick:
        axis_x = joystick.get_axis(0)
        if axis_x < -0.5:
            moveLeft = True
            moveRight = False
        elif axis_x > 0.5:
            moveRight = True
            moveLeft = False
        else:
            moveLeft = moveRight = False

        if joystick.get_button(0) and cooldownTimer <= 0:  # Assuming button 0 is the shoot button
            shoot = True
            cooldownTimer = shootCooldown
            pygame.mixer.Sound.play(shootSFX)

    if cooldownTimer > 0:
        cooldownTimer -= 1

    # Player movement
    if moveLeft and xpos > 0:
        xpos -= 5
    if moveRight and xpos < width - 60:
        xpos += 5

    # Bullet shooting
    if shoot:
        bullets.append(Bullet(xpos + 28, ypos))

    # Update game objects
    for bullet in bullets:
        bullet.move()

    for alien in armada:
        alien.move()
        for bullet in bullets:
            alien.check_collision(bullet)

    for wall in walls:
        for bullet in bullets:
            wall.check_collision(bullet)

    for wall in walls:
        for missile in missiles:
            wall.check_collision(missile)

    for missile in missiles:
        missile.move()

    chance = random.randrange(100)
    if chance < missile_frequency:
        pick = random.randrange(len(armada))
        if armada[pick].isAlive:
            missile = missileConstructor()
            missile.isAlive = True
            missile.xpos = armada[pick].xpos + 5
            missile.ypos = armada[pick].ypos
            missiles.append(missile)

    # Check collisions
    for missile in missiles:
        if missile.isAlive and xpos < missile.xpos < xpos + 40 and ypos < missile.ypos < ypos + 40:
            lives -= 1
            xpos, ypos = 365, 750

    for alien in armada:
        if alien.isAlive and xpos < alien.xpos < xpos + 40 and ypos < alien.ypos < ypos + 40:
            gameOver = True

    # Render Section
    screen.fill(BLACK)

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

    pygame.draw.rect(screen, GREEN, (xpos, ypos, 60, 20))
    pygame.draw.rect(screen, GREEN, (xpos + 20, ypos - 10, 20, 10))

    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES: ' + str(lives), False, WHITE)
    screen.blit(text_surface, (0, 0))

    pygame.display.flip()

if gameOver:
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(800 // 2, 800 // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    pygame.time.delay(2000)

pygame.quit()
