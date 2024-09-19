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
enemy_bullet_img = pygame.image.load('enemy_bullet.png')

# Enemy setup
enemy = []
enemyx = []
enemyy = []
enemyspeedx = []
enemyspeedy = []
enemy_bullet_list = []

no_of_aliens = 6

for i in range(no_of_aliens):
    enemy.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(30, 120))
    enemyspeedx.append(8)
    enemyspeedy.append(20)
    # Add initial empty bullet for each enemy
    enemy_bullet_list.append({"x": -100, "y": -100, "state": "ready"})

# Variables
spaceshipx = 370
spaceshipy = 480
changex = 0

bullets = []  # List to store multiple bullets shot by spaceship
bullet_speed = 10
score = 0

# Font setup
font = pygame.font.Font(None, 36)

# Function to detect collision (Simplified)
def is_collision(obj_x, obj_y, target_x, target_y, distance_threshold):
    distance = math.sqrt((obj_x - target_x)**2 + (obj_y - target_y)**2)
    return distance < distance_threshold

# Display game over
font_gameover = pygame.font.SysFont('Arial', 64, 'bold')

def gameover():
    gameover_display = font_gameover.render('GAME OVER', True, 'red')
    screen.blit(gameover_display, (200, 250))

# Function to handle enemy shooting bullets
def enemy_shoot_bullet(i):
    if enemy_bullet_list[i]["state"] == "ready":
        enemy_bullet_list[i]["x"] = enemyx[i] + 16  # Align with enemy
        enemy_bullet_list[i]["y"] = enemyy[i]
        enemy_bullet_list[i]["state"] = "fire"

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
                # Shoot multiple bullets
                bullets.append({"x": spaceshipx + 15, "y": spaceshipy, "state": "fire"})
                laser_sound = mixer.Sound('laser.wav')
                laser_sound.play()

        if event.type == pygame.KEYUP:
            changex = 0

    spaceshipx += changex
    if spaceshipx <= 0:
        spaceshipx = 0
    if spaceshipx >= 736:
        spaceshipx = 736

    # Enemy movement and bullet shooting
    for i in range(no_of_aliens):
        enemyx[i] += enemyspeedx[i]
        if enemyx[i] <= 0:
            enemyspeedx[i] = 8
            enemyy[i] += enemyspeedy[i]
        elif enemyx[i] >= 736:
            enemyspeedx[i] = -8
            enemyy[i] += enemyspeedy[i]
        
        # Game over if enemy reaches a certain height
        if enemyy[i] > 420:
            for j in range(no_of_aliens):
                enemyy[j] = 2000
            gameover()
            break

        # Collision detection (spaceship bullets hitting enemy)
        for bullet in bullets:
            collision = is_collision(bullet["x"], bullet["y"], enemyx[i], enemyy[i], 27)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet["y"] = 480
                bullet["state"] = "ready"
                score += 1
                enemyx[i] = random.randint(0, 736)
                enemyy[i] = random.randint(30, 120)

        # Enemy shoots bullet randomly
        if random.randint(0, 100) < 1:  # 1% chance per frame for the enemy to shoot
            enemy_shoot_bullet(i)

        # Draw enemy
        screen.blit(enemy[i], (enemyx[i], enemyy[i]))

    # Spaceship bullets movement
    for bullet in bullets:
        if bullet["state"] == "fire":
            screen.blit(bulletimg, (bullet["x"], bullet["y"]))
            bullet["y"] -= bullet_speed

            if bullet["y"] <= 0:
                bullet["state"] = "ready"
                bullets.remove(bullet)  # Remove bullet if it goes off-screen

    # Enemy bullet movement and collision with spaceship
    for i in range(no_of_aliens):
        if enemy_bullet_list[i]["state"] == "fire":
            screen.blit(enemy_bullet_img, (enemy_bullet_list[i]["x"], enemy_bullet_list[i]["y"]))
            enemy_bullet_list[i]["y"] += 10

            # Collision detection (enemy bullets hitting spaceship)
            if is_collision(enemy_bullet_list[i]["x"], enemy_bullet_list[i]["y"], spaceshipx, spaceshipy, 27):
                gameover()
                running = False  # End the game

            if enemy_bullet_list[i]["y"] > 600:
                enemy_bullet_list[i]["state"] = "ready"  # Reset bullet if it goes off-screen

    # Display spaceship
    screen.blit(spaceshipimg, (spaceshipx, spaceshipy))

    # Display score
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

    pygame.display.update()
