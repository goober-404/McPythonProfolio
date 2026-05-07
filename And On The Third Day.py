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
enemyWalkingFoward1 = pygame.image.load('DeamonWalking1.png')
enemyWalkingFoward2 = pygame.image.load('DeamonWalking2.png')
enemyWalkingBack1 = pygame.image.load('DeamonWalkingBack1.png')
enemyWalkingBack2 = pygame.image.load('DeamonWalkingBack2.png')
enemyWalkingLeft1 = pygame.image.load('DeamonWalkingLeft1.png')
enemyWalkingLeft2 = pygame.image.load('DeamonWalkingLeft2.png')
enemyWalkingRight1 = pygame.image.load('DeamonWalkingRight1.png')
enemyWalkingRight2 = pygame.image.load('DeamonWalkingRight2.png')

enemySprites = {
    'forward': [enemyWalkingFoward1, enemyWalkingFoward2],
    'back': [enemyWalkingBack1, enemyWalkingBack2],
    'left': [enemyWalkingLeft1, enemyWalkingLeft2],
    'right': [enemyWalkingRight1, enemyWalkingRight2],
}

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

required_kills = 5
kill_count = 0
spawn_timer = 0
spawn_interval = 120
max_active_enemies = 10

controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
}
pause_active = False
pause_selected = 0
pause_menu_items = ['up', 'down', 'left', 'right', 'resume']
rebind_mode = False
rebind_action = None

enemies = []

def create_enemy(position):
    return {
        'rect': enemyWalkingFoward1.get_rect(center=position),
        'vel': Vector2(0, 0),
        'ACCEL': 0.16,
        'FRICTION': 0.90,
        'MAX_SPEED': 3,
        'health': 6,
        'alive': True,
        'target_offset': Vector2(random.uniform(-200, 200), random.uniform(-150, 150)),
        'spawn_side': None,
    }

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

def updateEnemy(enemy):
    global playerSpriteSFrect, enemies
    if not enemy['alive']:
        return

    target = Vector2(playerSpriteSFrect.center) + enemy['target_offset']
    dx = target.x - enemy['rect'].centerx
    dy = target.y - enemy['rect'].centery

    if abs(dx) > 4:
        enemy['vel'].x += enemy['ACCEL'] if dx > 0 else -enemy['ACCEL']
    else:
        enemy['vel'].x *= enemy['FRICTION']

    if abs(dy) > 4:
        enemy['vel'].y += enemy['ACCEL'] if dy > 0 else -enemy['ACCEL']
    else:
        enemy['vel'].y *= enemy['FRICTION']

    for other in enemies:
        if other is enemy or not other['alive']:
            continue
        separation = Vector2(enemy['rect'].center) - Vector2(other['rect'].center)
        if separation.length_squared() > 0 and separation.length() < 90:
            repel = separation.normalize() * 0.12
            enemy['vel'] += repel

    if abs(enemy['vel'].x) > enemy['MAX_SPEED']:
        enemy['vel'].x = enemy['MAX_SPEED'] if enemy['vel'].x > 0 else -enemy['MAX_SPEED']
    if abs(enemy['vel'].y) > enemy['MAX_SPEED']:
        enemy['vel'].y = enemy['MAX_SPEED'] if enemy['vel'].y > 0 else -enemy['MAX_SPEED']

    enemy['rect'].x += int(enemy['vel'].x)
    enemy['rect'].y += int(enemy['vel'].y)


def drawEnemy(enemy):
    if not enemy['alive']:
        return

    dx = playerSpriteSFrect.centerx - enemy['rect'].centerx
    dy = playerSpriteSFrect.centery - enemy['rect'].centery
    if abs(dx) > abs(dy):
        direction = 'right' if dx > 0 else 'left'
    else:
        direction = 'forward' if dy > 0 else 'back'

    walking = enemy['vel'].length_squared() > 0.1
    frame = (pygame.time.get_ticks() // 150) % 2 if walking else 0
    sprite = enemySprites[direction][frame]

    screen.blit(sprite, enemy['rect'])

    bar_width = enemy['rect'].width
    bar_height = 8
    bar_x = enemy['rect'].x
    bar_y = enemy['rect'].y - bar_height - 6
    health_ratio = max(enemy['health'], 0) / 6
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))


def enemyCollisions(enemy):
    global playerSpriteSFrect, knockbackVector
    if not enemy['alive']:
        return
    if enemy['rect'].colliderect(playerSpriteSFrect):
        direction_vector = Vector2(playerSpriteSFrect.center) - Vector2(enemy['rect'].center)
        if direction_vector.length() > 0:
            direction_vector = direction_vector.normalize()
        knockback_strength = 15
        knockbackVector.x = direction_vector.x * knockback_strength
        knockbackVector.y = direction_vector.y * knockback_strength

def spawn_side_enemy():
    side = random.choice(['left', 'right'])
    y = random.randint(100, 800)
    if side == 'left':
        x = -80
    else:
        x = 1580
    enemy = create_enemy((x, y))
    enemy['spawn_side'] = side
    return enemy


def spawn_enemies(count):
    return [spawn_side_enemy() for _ in range(count)]

def handleInputs():
    global gameLoop, boost, acceptingNewVector, inRange, knockbackVector, boostVector, isWalking
    global pause_active, pause_selected, rebind_mode, rebind_action, controls
    keys = pygame.key.get_pressed()
    isWalking = False

    for event in pygame.event.get():
        if pause_active:
            if event.type == pygame.KEYDOWN:
                if rebind_mode:
                    if event.key == pygame.K_ESCAPE:
                        rebind_mode = False
                        rebind_action = None
                    elif event.key != pygame.K_RETURN and event.key != pygame.K_SPACE:
                        controls[rebind_action] = event.key
                        rebind_mode = False
                        rebind_action = None
                else:
                    if event.key == pygame.K_ESCAPE:
                        pause_active = False
                    elif event.key == pygame.K_UP:
                        pause_selected = (pause_selected - 1) % len(pause_menu_items)
                    elif event.key == pygame.K_DOWN:
                        pause_selected = (pause_selected + 1) % len(pause_menu_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected_action = pause_menu_items[pause_selected]
                        if selected_action == 'resume':
                            pause_active = False
                        else:
                            rebind_mode = True
                            rebind_action = selected_action
            elif event.type == pygame.QUIT:
                gameLoop = False
            continue

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
                pause_active = True

    if not pause_active:
        if keys[controls['up']]:
            playerSpriteSFrect.y -= playerSpeed
            isWalking = True
        if keys[controls['down']]:
            playerSpriteSFrect.y += playerSpeed
            isWalking = True
        if keys[controls['left']]:
            playerSpriteSFrect.x -= playerSpeed
            isWalking = True
        if keys[controls['right']]:
            playerSpriteSFrect.x += playerSpeed
            isWalking = True

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


def get_key_name(keycode):
    return pygame.key.name(keycode).upper()


def draw_pause_menu():
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    title = font.render('PAUSED', True, WHITE)
    screen.blit(title, (w // 2 - title.get_width() // 2, 100))

    for idx, action in enumerate(pause_menu_items):
        if action == 'resume':
            text = 'Resume'
        else:
            text = f"{action.capitalize()}: {get_key_name(controls[action])}"
            if rebind_mode and rebind_action == action:
                text = f"Press new key for {action.capitalize()}"
        color = (255, 200, 0) if idx == pause_selected else WHITE
        item_text = font.render(text, True, color)
        screen.blit(item_text, (w // 2 - item_text.get_width() // 2, 200 + idx * 60))

    hint = 'Use arrow keys to navigate, Enter to rebind, ESC to resume'
    hint_text = font.render(hint, True, (180, 180, 180))
    screen.blit(hint_text, (w // 2 - hint_text.get_width() // 2, h - 100))

# Spawn the required demons for the win goal
if not enemies:
    enemies = spawn_enemies(required_kills)

while gameLoop:
    mousePos = pygame.mouse.get_pos()
    isWalking = handleInputs()
    w, h = pygame.display.get_surface().get_size()
    ground = pygame.Rect(0, h-200, w, 200)

    if pause_active:
        screen.fill(BLACK)
        draw()
        draw_pause_menu()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    spawn_timer += 1
    active_enemies = sum(1 for e in enemies if e['alive'])
    if spawn_timer >= spawn_interval and active_enemies < max_active_enemies:
        enemies.append(spawn_side_enemy())
        spawn_timer = 0

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

    if kill_count >= required_kills:
        victory_text = font.render(f"You win! {kill_count}/{required_kills} demons defeated", True, WHITE)
        screen.blit(victory_text, (w // 2 - victory_text.get_width() // 2, h // 2 - 20))
        pygame.display.flip()
        continue

    for enemy in enemies:
        updateEnemy(enemy)
        drawEnemy(enemy)
        enemyCollisions(enemy)

    for b in holylightBullets:
        b['pos'] += b['vel']

    surviving_bullets = []
    for b in holylightBullets:
        hit_any = False
        for enemy in enemies:
            if enemy['alive'] and enemy['rect'].collidepoint(b['pos']):
                enemy['health'] -= 1
                if enemy['health'] <= 0:
                    enemy['alive'] = False
                    kill_count += 1
                hit_any = True
                break
        if hit_any:
            continue
        if bounds.collidepoint(b['pos']):
            surviving_bullets.append(b)

    holylightBullets = surviving_bullets

    for b in holylightBullets:
        bullet_img = pygame.transform.scale(holyLightBullet, (50, 50))
        rotated_bullet = pygame.transform.rotate(bullet_img, b['angle'])
        rot_rect = rotated_bullet.get_rect(center=(int(b['pos'].x), int(b['pos'].y)))
        screen.blit(rotated_bullet, rot_rect)

    goal_text = font.render(f"Demons defeated: {kill_count}/{required_kills}", True, WHITE)
    screen.blit(goal_text, (20, 20))

    angleCalc()
    pygame.display.flip()

