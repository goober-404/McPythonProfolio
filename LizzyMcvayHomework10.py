import pygame, sys
import time
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Hammer of Justice.mp3') #from deltarune chapter 4
pygame.mixer.music.play(loops=-1)

font = pygame.font.SysFont(None, 50)

screenW = 1000
screenY = 1000

playerX = 100
playerY = 259
playerW = 50
playerH = 50

victoryScreen = pygame.image.load('goodjob (thumbsup).png')
victoryRect = victoryScreen.get_rect()
faliureScreen = pygame.image.load('sad-tired.png')
faliureRect = faliureScreen.get_rect()


def updownleftright():
    global playerX,playerY
    if key[pygame.K_LEFT]:
        playerX-=1
    if key[pygame.K_RIGHT]:
        playerX+=1
    if key[pygame.K_UP]:
        playerY-=1
    if key[pygame.K_DOWN]:
        playerY+=1
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
pygame.display.set_caption("Alternate universe Saint Thomas More where he's fleeing from his execution")

backgroundColor = (175, 175, 175)
colorBrown = (166, 126, 73)
colorGrey = (107, 107, 107)
colorYellow = (251, 244, 127)
colorGreen = (146, 251, 127)
BLACK = (0, 0, 0)
running = True
while running == True:
    screen.fill(backgroundColor)
    text = font.render(f"You're saint thomas more. You chose to not ", True, (colorGrey))
    text2 = font.render(f"vow your life to the newly establish Church of England", True, (colorGrey))
    text3 = font.render(f"started by King Henry VII. Your on the run from him and", True, (colorGrey))
    text4 = font.render(f"his guards to avoid execution.", True, (colorGrey))
    screen.blit(text,(50,50))
    screen.blit(text2,(50,100))
    screen.blit(text3,(50,150))
    screen.blit(text4, (50,200))
    key = pygame.key.get_pressed()

    updownleftright()
    
    boundaries()
    
    fRect = pygame.Rect((421, 620, 60, 60))
    sRect = pygame.Rect((622, 323, 60, 60))
    aRect = pygame.Rect((110, 723, 60, 60))
    
    dRect = pygame.Rect((400, 600, 100, 100))
    rRect = pygame.Rect((600, 300, 100, 100))
    eRect = pygame.Rect((90, 700, 100, 100))
    tRect = pygame.Rect((0,900,1000,100))
    playerRect = pygame.Rect((playerX,playerY,playerW,playerH))


    pygame.draw.rect(screen, colorYellow, dRect)
    pygame.draw.rect(screen, colorYellow, rRect)
    pygame.draw.rect(screen, colorYellow, eRect)

    pygame.draw.rect(screen, colorGrey, aRect)
    pygame.draw.rect(screen, colorGrey, fRect)
    pygame.draw.rect(screen, colorGrey, sRect)
    
    pygame.draw.rect(screen, colorGreen, tRect)
    pygame.draw.rect(screen, colorBrown, playerRect)

    if playerRect.colliderect(dRect):
        playerX = 100
        playerY = 259
        while True:
            pygame.mixer.music.load("Roblox Death Sound (Oof).mp3")
            pygame.mixer.music.play()
            screen.blit(faliureScreen, (300, 300), faliureRect)
            pygame.display.flip()
            time.sleep(2)
            break
        pygame.mixer.music.load('Hammer of Justice.mp3')
        pygame.mixer.music.play(loops=-1)
    if playerRect.colliderect(eRect):
        playerX = 100
        playerY = 259
        while True:
            pygame.mixer.music.load("Roblox Death Sound (Oof).mp3")
            pygame.mixer.music.play()
            screen.blit(faliureScreen, (300, 300), faliureRect)
            pygame.display.flip()
            time.sleep(2)
            break
        pygame.mixer.music.load('Hammer of Justice.mp3')
        pygame.mixer.music.play(loops=-1)

    if playerRect.colliderect(rRect):
        playerX = 100
        playerY = 259
        while True:
            pygame.mixer.music.load("Roblox Death Sound (Oof).mp3")
            pygame.mixer.music.play()
            screen.blit(faliureScreen, (300, 300), faliureRect)
            pygame.display.flip()
            time.sleep(2)
            break
        pygame.mixer.music.load('Hammer of Justice.mp3')
        pygame.mixer.music.play(loops=-1)

    if playerRect.colliderect(tRect):
        playerX = 100
        playerY = 259
        pygame.mixer.music.load("Windows 98 Sound_ Tada.mp3")
        pygame.mixer.music.play()
        
        while True:
            screen.blit(victoryScreen, (280, 300), victoryRect)
            pygame.display.flip()
            time.sleep(3)
            break
        screen.blit(victoryScreen, (-100, 0))
        pygame.mixer.music.load('Hammer of Justice.mp3')
        pygame.mixer.music.play(loops=-1)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()
