import pygame,random,math
from pygame.locals import *
from pygame.math import Vector2
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont(None, 40)

BLUE = (0,0,255)
DARKBLUE = (0,71,171)
WHITE = (255,255,255)
BLACK = (134, 134, 134)
GREEN = (0,255,0)
RED = (255,0,0)
PEACH = (255,176,156)

gameLoop = True
playerSpeed = 10
grounded = False
fallSpeed = 9

playerSpriteSF = pygame.image.load('jesusStillFacingForward.png')
playerSpriteSB = pygame.image.load('jesusStillFacingBackwards.png')
playerSpriteSL = pygame.image.load('jesusStillFacingLeft.png')
playerSpriteSR = pygame.image.load('jesusStillFacingRight.png')
playerSpriteWF = pygame.image.load('jesusWalkingFacingForward.png')
playerSpriteWB = pygame.image.load('jesusWalkingFacingBackwards.png')
playerSpriteWL = pygame.image.load('jesusWalkingFacingLeft.png')
playerSpriteWR = pygame.image.load('jesusWalkingFacingRight.png')
holyLightBullet = pygame.image.load('HolyBullet.png')
enemyPlaceholder = pygame.image.load('furious-man-with-clenched-fists-and-bared-teeth-exudes-intense-anger-reflecting-frustration-and-tension-with-a-dangerous-presence-free-photo.webp')
playerSpriteSBrect = playerSpriteSB.get_rect()
playerSpriteSBW = 70
playerSpriteSBH = 100
playerSpriteSBX = 0
playerSpriteSBY = 0
playerSpriteSFrect = playerSpriteSF.get_rect()
playerSpriteSFW = 70
playerSpriteSFH = 100
playerSpriteSFX = 0
playerSpriteSFY = 0

boost = 10
boostVector = Vector2(0,0)
knockbackVector = Vector2(0,0)
knockbackDecay = 0.90
acceptingNewVector = True
inRange = False
isWalking = False
holylightBullets = []

tilemap = [
    'B________',
    'B________',
    'B________',
    'B________',
    'B________',
    '____B____'
            ]

FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
w, h = pygame.display.get_surface().get_size()
mousePos = pygame.mouse.get_pos()
offset = pygame.math.Vector2(0,0)
world = pygame.math.Vector2(w/2,h/2)
playerSpriteSFrect = pygame.Rect(world.x,world.y,playerSpriteSFW,playerSpriteSFH)
ground = pygame.Rect(world.x,world.y+100,1000,100)

def enemyAI(enemyRect):
    global playerSpriteSFrect
    direction_vector = Vector2(playerSpriteSFrect.center) - Vector2(enemyRect.center)
    if direction_vector.length() > 0:
        direction_vector = direction_vector.normalize()
    enemyRect.x += int(direction_vector.x * 2)
    enemyRect.y += int(direction_vector.y * 2)

def drawEnemy(enemyRect):
    screen.blit(enemyPlaceholder, enemyRect)

def enemyCollisions(enemyRect):
    global playerSpriteSFrect, knockbackVector, knockbackDecay
    if enemyRect.colliderect(playerSpriteSFrect):
        direction_vector = Vector2(playerSpriteSFrect.center) - Vector2(enemyRect.center)
        if direction_vector.length() > 0:
            direction_vector = direction_vector.normalize()
        knockback_strength = 15
        knockbackVector.x = direction_vector.x * knockback_strength
        knockbackVector.y = direction_vector.y * knockback_strength

def enemyTargetingPlayer(enemyRect):
    global playerSpriteSFrect, playerSpriteSBrect, playerSpriteSLrect, playerSpriteSRrect, playerSprite
    direction_vector = Vector2(playerSpriteSFrect.center) - Vector2(enemyRect.center)
    if direction_vector.length() > 0:
        direction_vector = direction_vector.normalize()
    return direction_vector

def enemyMovement(enemyRect, target_vector):
    enemyRect.x += int(target_vector.x * 2)
    enemyRect.y += int(target_vector.y * 2)

def handleInputs():
    global gameLoop,boost,acceptingNewVector,inRange,knockbackVector,isWalking
    keys = pygame.key.get_pressed()
    isWalking = False
    if keys[pygame.K_w]:
        playerSpriteSFrect.y -= playerSpeed
        isWalking = True
    if keys[pygame.K_s]:
        playerSpriteSFrect.y += playerSpeed
        isWalking = True
    if keys[pygame.K_a]:
        playerSpriteSFrect.x -= playerSpeed
        isWalking = True
    if keys[pygame.K_d]:
        playerSpriteSFrect.x += playerSpeed
        isWalking = True

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Mouse button {event.button} clicked at {event.pos}")
            if event.button == 1:
                click_pos = Vector2(event.pos)
                player_center = Vector2(playerSpriteSFrect.center)
                direction = (click_pos - player_center)
                if direction.length() > 0:
                    direction = direction.normalize()
                    knockback_strength = 9
                    # Set knockback velocity opposite to click direction
                    knockbackVector.x = -direction.x * knockback_strength
                    knockbackVector.y = -direction.y * knockback_strength
                    boost = 0
                    boostVector = Vector2(0,0)
                    acceptingNewVector = False
                    inRange = False

                    shoot_origin = player_center + direction * 100
                    bullet_speed = 14
                    bullet_vel = direction * bullet_speed
                    bullet_angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
                    holylightBullets.append({'pos': shoot_origin, 'vel': bullet_vel, 'angle': bullet_angle})
            elif event.button == 3: 
                if inRange:
                    boost = 40
                    acceptingNewVector = True
                    inRange = False
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameLoop = False

    return isWalking

def draw():
    global isWalking
    direction_vector = Vector2(mousePos) - playerSpriteSFrect.center
    selected_idle = playerSpriteSF
    selected_walk = playerSpriteWF

    if direction_vector.length() > 0:
        direction = direction_vector.normalize()
        if abs(direction.y) >= abs(direction.x):
            if direction.y < 0:
                selected_idle = playerSpriteSB
                selected_walk = playerSpriteWB
            else:
                selected_idle = playerSpriteSF
                selected_walk = playerSpriteWF
        else:
            if direction.x > 0:
                selected_idle = playerSpriteSR
                selected_walk = playerSpriteWR
            else:
                selected_idle = playerSpriteSL
                selected_walk = playerSpriteWL

    if isWalking:
        frame = (pygame.time.get_ticks() // 150) % 2
        selected_sprite = selected_walk if frame == 0 else selected_idle
    else:
        selected_sprite = selected_idle

    screen.blit(selected_sprite, playerSpriteSFrect, (playerSpriteSFX, playerSpriteSFY, playerSpriteSFW, playerSpriteSFH))

#def collidePlayer(self,player):
#    global grounded,mousePos,inRange
#    if self.contains(mousePos,(1,1)):
#        inRange = True
#    if self.colliderect(player):
#        leftOverlap = player.right - self.left
#        rightOverlap = self.right - player.left
#        topOverlap = player.bottom - self.top
#        bottomOverlap = self.bottom - player.top
#        min_overlap = min(leftOverlap, rightOverlap, topOverlap, bottomOverlap) #Which of these overlaps is smallest?
#        if min_overlap == topOverlap:
#            player.y -= topOverlap
#        elif min_overlap == bottomOverlap:
#            player.y += bottomOverlap
#        elif min_overlap == leftOverlap:
#            player.x -= leftOverlap
#        elif min_overlap == rightOverlap:
#            player.x += rightOverlap

def angleCalc():
    global boost,acceptingNewVector,boostVector,mousePos
    direction_vector = Vector2(mousePos) - playerSpriteSFrect.center
    if direction_vector.length() > 0:
        direction_vector = direction_vector.normalize()
    target_offset = direction_vector * 100
    square_pos = playerSpriteSFrect.center + target_offset

    pygame.draw.circle(screen, (141, 84, 37), (int(square_pos.x), int(square_pos.y)), 18, 0)
    pygame.draw.circle(screen, (235, 193, 135), (int(square_pos.x), int(square_pos.y)), 12, 0)
    
    if acceptingNewVector:
        boostVector = direction_vector
        acceptingNewVector = False
    velocity = boostVector * boost
    playerSpriteSFrect.x += velocity.x
    playerSpriteSFrect.y += velocity.y
    if boost > 0:
        boost -= 1
    pygame.event.pump()

while gameLoop:
    mousePos = pygame.mouse.get_pos()
    isWalking = handleInputs()
    w, h = pygame.display.get_surface().get_size()
    ground = pygame.Rect(0, h-200, w, 200)

    playerSpriteSFrect.x += knockbackVector.x
    playerSpriteSFrect.y += knockbackVector.y
    knockbackVector *= knockbackDecay
    if abs(knockbackVector.x) < 0.05:
        knockbackVector.x = 0
    if abs(knockbackVector.y) < 0.05:
        knockbackVector.y = 0

    bounds = screen.get_rect()
    playerSpriteSFrect.clamp_ip(bounds)

    screen.fill(BLACK)
    clock.tick(FPS)
    draw()

    enemyAI(enemyPlaceholder.get_rect(topleft=(w-200, h-300)))
    enemyCollisions(enemyPlaceholder.get_rect(topleft=(w-200, h-300)))
    drawEnemy(enemyPlaceholder.get_rect(topleft=(w-200, h-300)))

    for b in holylightBullets:
        b['pos'] += b['vel']
    holylightBullets[:] = [b for b in holylightBullets if bounds.collidepoint(b['pos'])]
    for b in holylightBullets:
        bullet_img = pygame.transform.scale(holyLightBullet, (50, 50))
        rotated_bullet = pygame.transform.rotate(bullet_img, b['angle'])
        rot_rect = rotated_bullet.get_rect(center=(int(b['pos'].x), int(b['pos'].y)))
        screen.blit(rotated_bullet, rot_rect)

    angleCalc()
    pygame.display.flip()

