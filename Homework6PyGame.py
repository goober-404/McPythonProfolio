#I did want to do more with this but I got sick and lost a lot of modivation to work on it. So I just decided to do the bare minumum.
import pygame, sys
import time
import random
from pygame.locals import *

screenW = 700
screenY= 700

screen = pygame.display.set_mode((screenW, screenY))

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Undertale Ghost Fight.mp3')
pygame.mixer.music.play(loops=-1)

size = 20
ATKsize = 20
HEALsize = 20

enemyHP = 400
enemyMaxHP = 400

playerspeed = 6

enemyX=random.randint(0,screenW)
enemyY=0

enemySpeed=4
ATKspeed=4
HEALspeed=4

rects = []

FPS = 60
clock = pygame.time.Clock()

enemyX = random.randint(0,screenW)
enemyY = 0

interval = 40
count = 0
atk_count = 0
Heal_count = 0

playerX = 300
playerY = 300
playerW = 32
playerH = 32

playerSprite = pygame.image.load('DeltaruneHeart.png')
enemySprite = pygame.image.load('teardrop.png')
ATKsprite = pygame.image.load('ATKteardrop.png')
HEALsprite = pygame.image.load('HEALteardrop.png')
howToPlaySprite = pygame.image.load('HowToPlay.png')



playerRect = playerSprite.get_rect(x=(playerX), y=(playerY))
enemyRect = enemySprite.get_rect(x=(enemyX), y=(enemyY))
ATKrect = ATKsprite.get_rect(x=(enemyX), y=(enemyY))
HEALrect = HEALsprite.get_rect(x=(enemyX), y=(enemyY))

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

        
def draw():
    screen.blit(enemySprite, enemyRect)
    screen.blit(ATKsprite, ATKrect)

def spawn():
    global count, interval, atk_count, rects, Heal_count
    count += 1
    atk_count += 1
    Heal_count += 1
    if count >= interval:
        r = pygame.Rect(random.randint(0, screen.get_width() - size), -size, size, size)
        rects.append(('enemy', r))
        count = 0
    if atk_count >= interval * 5:
        r = pygame.Rect(random.randint(0, screen.get_width() - ATKsize), -ATKsize, ATKsize, ATKsize)
        rects.append(('atk', r))
        atk_count = 0
    if Heal_count >= interval * 7:
        r = pygame.Rect(random.randint(0, screen.get_width() - HEALsize), -HEALsize, HEALsize, HEALsize)
        rects.append(('heal', r))
        Heal_count = 0

def fallingRectangles(enemySpeed):
    global playerHP, rects, enemyHP
    for item in rects[:]:
        typ, rect = item
        if typ == 'enemy':
            screen.blit(enemySprite, rect)
            rect.y += enemySpeed
        elif typ == 'atk':
            screen.blit(ATKsprite, rect)
            rect.y += ATKspeed
        elif typ == 'heal':
            screen.blit(HEALsprite, rect)
            rect.y += HEALspeed
        if rect.y > screen.get_height():
            rects.remove(item)
            continue
        if typ == 'enemy' and playerRect.colliderect(rect):
            playerHP -= 20
            if item in rects:
                rects.remove(item)
        if typ == 'atk' and playerRect.colliderect(rect):
            enemyHP -= 15
            if item in rects:
                rects.remove(item)
        if typ == 'heal' and playerRect.colliderect(rect):
            playerHP += 20
            if playerHP > maxHP:
                playerHP = maxHP
            if item in rects:
                rects.remove(item)
        

def HPbar():
    global playerHP, maxHP
    pygame.draw.rect(screen, (255,0,0), (10,10,200,20))
    pygame.draw.rect(screen, (0,255,0), (10,10,(playerHP/maxHP)*200,20))
    font = pygame.font.SysFont(None, 20)
    text = font.render(f'HP: {playerHP}/{maxHP}', True, (0,0,0))
    screen.blit(text, (15, 12))

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
                    playerHP = maxHP
                    enemyHP = enemyMaxHP
                    rects.clear()
                    playerRect.x = playerX
                    playerRect.y = playerY
def mainMenu():
    font = pygame.font.SysFont(None, 50)
    text = font.render('Click to Start', True, (255,255,255))
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
def howToPlay():
    screen.blit(howToPlaySprite, (0,0))
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


def drawCircleTopscreen():
    for i in range(0, screenW, 40):
        pygame.draw.circle(screen, (100, 100, 100), (i, 0), 50)

def enemyHPbar():
    global enemyHP
    pygame.draw.rect(screen, (255,0,0), (370,10,210,20))
    pygame.draw.rect(screen, (0,255,0), (370,10,(enemyHP/enemyMaxHP)*210,20))
    font = pygame.font.SysFont(None, 20)
    text = font.render(f'HP: {enemyHP}/{enemyMaxHP}', True, (0,0,0))
    screen.blit(text, (375, 12))

    if enemyHP <= 0:
        font = pygame.font.SysFont(None, 50)
        text = font.render('You Win! Click to play again.', True, (255,255,255))
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
                    enemyHP = enemyMaxHP
                    playerHP = maxHP
                    rects.clear()
                    playerRect.x = playerX
                    playerRect.y = playerY


screen = pygame.display.set_mode((screenW, screenY))
pygame.display.set_caption("Undertale Encounter")
gameRunning = False
gameActuallyRunning = False

RED = (225, 0, 0)
BLACK = (0, 0, 0)
running = True
while running == True:
    key = pygame.key.get_pressed()

    if gameRunning == False:
        mainMenu()
        gameRunning = True
    
    if gameRunning == True and gameActuallyRunning == False:
        howToPlay()
        gameActuallyRunning = True

    if gameActuallyRunning == True:
        clock.tick(FPS)

        screen.fill(BLACK)

        screen.blit(playerSprite, playerRect)

        updownleftright()

        drawCircleTopscreen()

        boundaries()

        fallingRectangles(enemySpeed)

        spawn()

        enemyHPbar()

        HPbar()




    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    if key[pygame.K_ESCAPE]:
        running=False
pygame.quit()
sys.exit()

# https://jummb.us/#j6N07Unnamedn310s0k0l00e03t1Xa7g0fj07r1O_U00000000i0o321T0v0du00f0000q8C010m70020Oa7d040w5h3E1c0b8T1v0du01f010p700q070Oa7ad080A0F5B3Q4140Pea77R0000E3c061b627638T5v0qud1f0000q0B1820Oa0d230HXzzrrrqiii9998h0E1c0baT4v0puf0f1a0q050Oa1z6666ji8k8k3jSBKSJJAArriiiiii07JCABrzrrrrrrr00YrkqHrsrrrrjr005zrAqzrjzrrqr1jRjrqGGrrzsrsA099ijrABJJJIAzrrtirqrqjqixzsrAjrqjiqaqqysttAJqjikikrizrHtBJJAzArzrIsRCITKSS099ijrAJS____Qg99habbCAYrDzh00E0c0b4zg0000000018M000000004h000000000h400000000p21NHmnMInXSuHJ-m1K4CmCpuhjd7iAczOqgFp5cNtvy1cRZvz6NUC4zkThPN799kPQvnlz5Sft7f2Y3eg4LoCNVjAgAmcpjGXHUKD52yKUKkX7F88000
