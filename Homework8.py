#I've been watching a lot of Spy X Family recently, I've been having this meme live rent free in my head for way too long... 

import pygame, sys
from pygame.locals import *
pygame.init()

screenW=800
screenH=800
screen=pygame.display.set_mode((screenW, screenH))

pygame.display.set_caption("episode of Spy X Family (!!!!!!REAL!!!!!!)")

colorMagenta = (245, 210, 255)

pX = 100
pY = 100
pW=0.4
pH=pW

loadimage = pygame.image.load('LizzyMcVayHomeworkSpriteSheet.png')
loadimage.set_colorkey(colorMagenta)

imageW = 5760
numberOfImages = 9
step = imageW/numberOfImages
imageH = 640
imageX = 0
imageY = 0
counter = 0

running = True

while running == True:
        
    screen.fill(colorMagenta)
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        pX-=1.5
    if key[pygame.K_RIGHT]:
        pX+=1.5
    if key[pygame.K_UP]:
        pY-=1.5
    if key[pygame.K_DOWN]:
        pY+=1.5

    pRect = pygame.Rect((pX, pY, pW, pH))
    
    screen.blit(loadimage, (pX, pY),(imageX, imageY, 1000, 1000))
    counter +=40

    if counter%step == 0:
        imageX=counter
    if counter>=imageW-step:
        counter=0

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()
