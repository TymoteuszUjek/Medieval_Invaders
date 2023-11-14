import pygame
import random
import math
import os
import sys
from pygame import mixer


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()

score = 0

font_url = resource_path("fonts/Redline.ttf")
font = pygame.font.Font(
    font_url, 32)
textX = 10
textY = 10


def show_score(x, y):
    scoreText = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(scoreText, (x, y))


music_url = resource_path("sounds/background.mp3")
mixer.music.load(music_url)
mixer.music.play(-1)
mixer.music.set_volume(0.85)


screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Medieval Invaders")

icon_url = resource_path("assets/icon.png")
icon = pygame.image.load(icon_url)
pygame.display.set_icon(icon)

playerUrl = resource_path("assets/swordsman.png")
playerImg = pygame.image.load(playerUrl)
playerX = 368
playerY = 480
speedX = 0
speedY = 0
playerSpeedChange = 0.7

enemyImg = []
enemyX = []
enemyY = []
enemyspeedX = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemy_url = resource_path("assets/villager.png")
    enemyImg.append(pygame.image.load(enemy_url))
    enemyX.append(random.randint(1, 735))
    enemyY.append(0)
    enemyspeedX.append(random.choice([0.15, 0.1, 0.05, -0.15, -0.1, -0.05]))

sword_url = resource_path("assets/sword.png")
swordImg = pygame.image.load(sword_url)
swordX = -50
swordY = -50
swordSpeedY = 0.7
swordState = "ready"  # ready/throw


over_font = pygame.font.Font(font_url, 32)
game_state = "play"  # play/over


def game_over():
    global game_state, num_of_enemies, enemyY
    for j in range(num_of_enemies):
        enemyY[j] = 2000
    game_state = "over"
    over_text = over_font.render(
        "GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (240, 250))
    over_text_2 = over_font.render(
        "Press R to Restart", True, (0, 0, 0))
    screen.blit(over_text_2, (240, 280))


def new_game():
    global game_state, score, playerX, playerY
    game_state = "play"
    score = 0
    for i in range(num_of_enemies):
        genEnemy(i)
    playerX = 368
    playerY = 480


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def throw_sword(x, y):
    global swordState
    swordState = "throw"
    screen.blit(swordImg, (x, y))


def is_collision(enemyX, enemyY, swordX, swordY, d):
    distance = math.sqrt(
        (math.pow(enemyX-swordX, 2)+math.pow(enemyY-swordY, 2)))
    if distance < d:
        return True
    else:
        return False


def genEnemy(i):
    global enemyX, enemyY, enemyspeedX
    enemyX[i] = random.randint(1, 735)
    enemyY[i] = 0
    enemyspeedX[i] = random.choice([0.15, 0.1, 0.05, -0.15, -0.1, -0.05])


running = True

throw_url = resource_path(
    "sounds/hit.wav")
death_url = resource_path(
    "sounds/death.wav")


while running:
    screen.fill((211, 229, 180))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if swordState == "ready":
                    throw_sound = mixer.Sound(throw_url)
                    throw_sound.play()
                    swordY = playerY
                    swordX = playerX
                    throw_sword(swordX, swordY)
            if game_state == "over":
                if event.key == pygame.K_r:
                    new_game()

    keys = pygame.key.get_pressed()

    speedX = 0
    speedY = 0
    if game_state == "play":
        if keys[pygame.K_a]:
            speedX = -playerSpeedChange
        elif keys[pygame.K_d]:
            speedX = playerSpeedChange

        if keys[pygame.K_w]:
            speedY = -playerSpeedChange
        elif keys[pygame.K_s]:
            speedY = playerSpeedChange

    playerX += speedX
    playerY += speedY

    # game size for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # game size for enemy
    for i in range(num_of_enemies):

        if enemyY[i] > 536:
            game_over()
            break

        if enemyX[i] <= 0:
            enemyspeedX[i] *= -1
            enemyY[i] += 32
        elif enemyX[i] >= 736:
            enemyspeedX[i] *= -1
            enemyY[i] += 64

        collision = is_collision(enemyX[i], enemyY[i], swordX, swordY, 25)
        if collision:
            death_sound = mixer.Sound(death_url)
            death_sound.play()
            swordState = "ready"
            swordY = -50
            score += 1
            genEnemy(i)

        playerCollision = is_collision(
            enemyX[i], enemyY[i], playerX, playerY, 50)
        if playerCollision:
            game_over()

        enemy(enemyX[i], enemyY[i], i)

        enemyX[i] += enemyspeedX[i]

    if swordY <= -32:
        swordY = -50
        swordState = "ready"

    player(playerX, playerY)

    if swordState == "throw":
        throw_sword(swordX, swordY)
        swordY -= swordSpeedY
    show_score(textX, textY)
    pygame.display.update()
