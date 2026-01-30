#heh, can you tell im a fan of the undertale/deltarune games?

import pygame, sys
import time
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Undertale Ghost Fight.mp3')
pygame.mixer.music.play(loops=-1)

screenW = 500
screenY = 500

playerX = 100
playerY = 2
playerW = 62
playerH = 62

playerSprite = pygame.image.load('DeltaruneHeart.png')

def updownleftright():
    global playerX,playerY
    if key[pygame.K_a]:
        playerX-=0.5
    if key[pygame.K_d]:
        playerX+=0.5
    if key[pygame.K_w]:
        playerY-=0.5
    if key[pygame.K_s]:
        playerY+=0.5
        
    if key[pygame.K_LEFT]:
        playerX-=0.5
    if key[pygame.K_RIGHT]:
        playerX+=0.5
    if key[pygame.K_UP]:
        playerY-=0.5
    if key[pygame.K_DOWN]:
        playerY+=0.5
def boundaries():
    global playerX,playerY
    if playerX<0:
        playerX=0
    if playerY<0:
        playerY=0
    if playerX >screenW-playerW:
        playerX=screenW-playerW
    if playerY >screenY-playerH:
        playerY=screenY-playerH

    

screen = pygame.display.set_mode((screenW, screenY))
pygame.display.set_caption("Undertale Encounter")

BLACK = (0, 0, 0)
running = True
while running == True:
    screen.fill(BLACK)
    
    key = pygame.key.get_pressed()

    screen.blit(playerSprite, (playerX,playerY))

    updownleftright()

    boundaries()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()
