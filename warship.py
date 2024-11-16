import math
import random
from pygame.locals import *
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen_width = 1200
screen_height = 857
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.image.load('Bg.jpg')

# Sound
mixer.music.load("Julius Dreisig & Zeus X Crona - Invisible  Trap  NCS - Copyright Free Music.mp3")
mixer.music.play(-1)  # Loop the background music

# Caption and Icon
pygame.display.set_caption("WarShip-Made By Sifat")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Player
playerImg = pygame.image.load('player.png')
player_width = playerImg.get_width()
playerX = screen_width // 2 - player_width // 2
playerY = screen_height - 100
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Create enemies with adjusted speed
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, screen_width - 64))  # Ensuring enemies stay within screen width
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)  # Slower UFO speed
    enemyY_change.append(20)  # Slower movement downward

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def set_background():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

def move_bullet():
    global bulletX, bulletY, bullet_state
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

def game_input():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - player_width:
        playerX = screen_width - player_width

def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1  # Slow UFO speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 64:
            enemyX_change[i] = -1  # Slow UFO speed
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

def collision():
    global score_value, bulletY, bullet_state
    for i in range(num_of_enemies):
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - 64)
            enemyY[i] = random.randint(50, 150)

# Game Loop
running = True
while running:
    set_background()
    game_input()
    enemy_movement()
    collision()
    move_bullet()
    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
