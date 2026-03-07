import pygame, sys
from pygame.locals import *
pygame.init()

screenW = 500
screenY = 500

screen = pygame.display.set_mode((screenW, screenY))
pygame.display.set_caption("E.T. on the Atari.. NOO-")

playerX = screenW/2
playerY = screenY/2
playerW = 50
playerH = 50

colorPurple = (89, 62, 107)
colorBrown = (166, 126, 73)

running = True
while running == True:
    screen.fill(colorPurple)
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        playerX-=0.5
    if key[pygame.K_RIGHT]:
        playerX+=0.5
    if key[pygame.K_UP]:
        playerY-=0.5
    if key[pygame.K_DOWN]:
        playerY+=0.5

    if playerX<0:
        playerX=0
    if playerY<0:
        playerY=0
    if playerX >screenW-playerW:
        playerX=screenW-playerW
    if playerY >screenY-playerH:
        playerY=screenY-playerH
        

    playerRect = pygame.Rect((playerX,playerY,playerW,playerH))
    pygame.draw.rect(screen, colorBrown, playerRect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()
