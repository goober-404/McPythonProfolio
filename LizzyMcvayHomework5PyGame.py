

import pygame, sys
import time
import random
from pygame.locals import *

screenW = 650
screenY= 600

screen = pygame.display.set_mode((screenW, screenY))

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Undertale Ghost Fight.mp3')
pygame.mixer.music.play(loops=-1)

size = 20

playerspeed = 6

enemyX=random.randint(0,screenW)
enemyY=0

enemySpeed=4

rects = []

FPS = 60
clock = pygame.time.Clock()

enemyX = random.randint(0,screenW)
enemyY = 0

interval = 40
count = 0

playerX = 300
playerY = 300
playerW = 32
playerH = 32

playerSprite = pygame.image.load('DeltaruneHeart.png')
enemySprite = pygame.image.load('teardrop.png')

playerRect = playerSprite.get_rect(x=(playerX), y=(playerY))
enemyRect = enemySprite.get_rect(x=(enemyX), y=(enemyY))

playerHP = 200
maxHP = 200

def updownleftright():
    global playerX,playerY
    if key[pygame.K_a]:
        playerRect.x-=playerspeed
    if key[pygame.K_d]:
        playerRect.x+=playerspeed
    if key[pygame.K_w]:
        playerRect.y-=playerspeed
    if key[pygame.K_s]:
        playerRect.y+=playerspeed
        
    if key[pygame.K_LEFT]:
        playerRect.x-=playerspeed
    if key[pygame.K_RIGHT]:
        playerRect.x+=playerspeed
    if key[pygame.K_UP]:
        playerRect.y-=playerspeed
    if key[pygame.K_DOWN]:
        playerRect.y+=playerspeed

def boundaries():
    if playerRect.x<0:
        playerRect.x=0
    if playerRect.y<0:
        playerRect.y=0
    if playerRect.x >screenW-playerW:
        playerRect.x=screenW-playerW
    if playerRect.y >screenY-playerH:
       playerRect.y=screenY-playerH


def fallingRectangles(enemySpeed):
    global playerHP
    for rectangle in rects:
        screen.blit(enemySprite, rectangle)
        rectangle.y+=enemySpeed
        if rectangle.y>screen.get_height():
            rects.remove(rectangle)
        
        if playerRect.colliderect(rectangle):
            if playerRect.center < rectangle.center:
                playerRect.x -= playerspeed
            else:
                playerRect.x += playerspeed
            playerHP -= 10
        
def draw():
    screen.blit(enemySprite, enemyRect)


def spawn():
    global count, interval
    count += 2
    if count % interval == 0:
        rects.append(pygame.Rect(random.randint(0, screen.get_width()), -size, size, size))
        count = 0
def HPbar():
    global playerHP, maxHP
    pygame.draw.rect(screen, (255,0,0), (10,10,200,20))
    pygame.draw.rect(screen, (0,255,0), (10,10,(playerHP/maxHP)*200,20))

    if playerHP <= 0:
        font = pygame.font.SysFont(None, 50)
        text = font.render('Game Over. Click to try again.', True, (255,255,255))
        screen.blit(text, (screenW//2 - text.get_width()//2, screenY//2 - text.get_height()//2))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    waiting = False
                    playerHP = 200
                    maxHP = 200
                    rects.clear()
                    playerRect.x = playerX
                    playerRect.y = playerY



        
screen = pygame.display.set_mode((screenW, screenY))
pygame.display.set_caption("Undertale Encounter")

RED = (225, 0, 0)
BLACK = (0, 0, 0)
running = True
while running == True:

    clock.tick(FPS)
    
    screen.fill(BLACK)
    
    key = pygame.key.get_pressed()

    screen.blit(playerSprite, playerRect)

    updownleftright()

    boundaries()

    fallingRectangles(enemySpeed)

    spawn()

    HPbar()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()
