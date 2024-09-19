import random
import pygame
import math
from pygame import mixer

mixer.init()
pygame.init()

mixer.music.load('background.wav')
mixer.music.play(-1)

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invader Game')

# Icon and images setup
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('bg.png')
spaceshipimg = pygame.image.load('arcade.png')
bulletimg = pygame.image.load('bullet.png')

# Enemy setup
enemy = []
enemyx = []
enemyy = []
enemyspeedx = []
enemyspeedy = []

no_of_aliens = 6

for i in range(no_of_aliens):
    enemy.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(30, 120))
    enemyspeedx.append(8)
    enemyspeedy.append(20)

# Variables
spaceshipx = 370
spaceshipy = 480
changex = 0

bullet_x = 385
bullet_y = 480
bullet_speed = 10
bullet_state = "ready"  # "ready" means you can fire, "fire" means bullet is moving
score = 0

# Font setup
font = pygame.font.Font(None, 36)

# Function to detect collision (Simplified)
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Calculate the distance between enemy and bullet using Pythagorean theorem
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    
    # Collision happens if the distance is less than 27 (adjust this based on sizes)
    if distance < 27:
        return True
    else:
        return False

# Display game over
font_gameover = pygame.font.SysFont('Arial', 64, 'bold')

def gameover():
    gameover_display = font_gameover.render('GAME OVER', True, 'red')
    screen.blit(gameover_display, (200, 250))

# Game loop
running = True
while running:

    screen.blit(background, (0, 0))  # Draw the background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changex = -12
            if event.key == pygame.K_RIGHT:
                changex = +12
            if event.key == pygame.K_SPACE:

                if bullet_state == "ready":
                    bullet_state = "fire"
                    explosion_sound = mixer.Sound('laser.wav')
                    explosion_sound.play()
                    bullet_x = spaceshipx + 15  # Align bullet to spaceship position

        if event.type == pygame.KEYUP:
            changex = 0

    spaceshipx += changex
    if spaceshipx <= 0:
        spaceshipx = 0
    if spaceshipx >= 736:
        spaceshipx = 736

    # Enemy movement
    for i in range(no_of_aliens):
        enemyx[i] += enemyspeedx[i]
        if enemyx[i] <= 0:
            enemyspeedx[i] = 8
            enemyy[i] += enemyspeedy[i]
        elif enemyx[i] >= 736:
            enemyspeedx[i] = -8
            enemyy[i] += enemyspeedy[i]
        
        # Game over
        if enemyy[i] > 420:
            for j in range(no_of_aliens):
                enemyy[j] = 2000
            gameover()
            break

        # Collision detection
        collision = is_collision(enemyx[i], enemyy[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(30, 120)

        # Draw enemy
        screen.blit(enemy[i], (enemyx[i], enemyy[i]))

    # Bullet movement
    if bullet_state == "fire":
        screen.blit(bulletimg, (bullet_x, bullet_y))
        bullet_y -= bullet_speed

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Display spaceship
    screen.blit(spaceshipimg, (spaceshipx, spaceshipy))

    # Display score
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

    pygame.display.update()
