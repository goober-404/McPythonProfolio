# I will probably work on this game more once I finish this class, but for now I just wanted to get a basic version of the game working with all the core mechanics.
# I have a lot of ideas for this game but little to no time for any of them sooo yeah
# The background is from the game Hades btw, I'm gonna make my own background eventually. The title screen music is the instrumental of "Come little children" and the game music is "Beethovens Virus". I'll also make my own music at some point too.
# Right click to shoot bullets in the direction of the mouse, use WASD to move, E to do an AOE attack, and Shift to dash (unless you decide to rebind them), press ESC to pause and access the pause menu, and you can also save.
# Also if you use a certain cheat code on the main menu...

import pygame,random,math
from pygame.locals import *
from pygame.math import Vector2
import pickle
import os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
font = pygame.font.SysFont(None, 40)
MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.display.set_caption("And On The Third Day")

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

def safe_load_image(path):
    try:
        img = pygame.image.load(path)
        return img.convert_alpha()
    except (pygame.error, Exception):
        img = pygame.image.load(path)
        return img.convert() if path.endswith('.png') else img

playerSpriteSF = safe_load_image('jesusStillFacingForward.png')
playerSpriteSB = safe_load_image('jesusStillFacingBackwards.png')
playerSpriteSL = safe_load_image('jesusStillFacingLeft.png')
playerSpriteSR = safe_load_image('jesusStillFacingRight.png')
playerSpriteWF = safe_load_image('jesusWalkingFacingForward.png')
playerSpriteWB = safe_load_image('jesusWalkingFacingBackwards.png')
playerSpriteWL = safe_load_image('jesusWalkingFacingLeft.png')
playerSpriteWR = safe_load_image('jesusWalkingFacingRight.png')
holyLightBullet = safe_load_image('HolyBullet.png')
enemyWalkingFoward1 = safe_load_image('DeamonWalking1.png')
enemyWalkingFoward2 = safe_load_image('DeamonWalking2.png')
enemyWalkingBack1 = safe_load_image('DeamonWalkingBack1.png')
enemyWalkingBack2 = safe_load_image('DeamonWalkingBack2.png')
enemyWalkingLeft1 = safe_load_image('DeamonWalkingLeft1.png')
enemyWalkingLeft2 = safe_load_image('DeamonWalkingLeft2.png')
enemyWalkingRight1 = safe_load_image('DeamonWalkingRight1.png')
enemyWalkingRight2 = safe_load_image('DeamonWalkingRight2.png')
enemyEasterEgg = safe_load_image('furious-man-with-clenched-fists-and-bared-teeth-exudes-intense-anger.webp')
backgroundImage = safe_load_image('HadesBackground.png')
aoeAttackImage = safe_load_image('Aoe attack.png')
easter_music_file = 'Child Wielding Needle (Easter Egg).mp3'
game_music_file = 'Game Music.mp3'
title_music_file = 'Title Screen Music.mp3'
current_music = None
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

bg_scaled = None
bullet_image_scaled = None
aoe_image_scaled = None
player_sprite_scale = 1.0
scaled_player_sprites = {}
last_scaled_size = (0, 0)

def update_scaled_ui(size):
    global w, h, bg_scaled, font, title_font, small_font, bullet_image_scaled, aoe_image_scaled, player_sprite_scale, scaled_player_sprites, last_scaled_size
    if last_scaled_size == size:
        return
    last_scaled_size = size
    w, h = size
    bg_scaled = pygame.transform.scale(backgroundImage, (w, h))
    ui_scale = min(w, h) / 1000.0
    player_sprite_scale = ui_scale
    font = pygame.font.SysFont(None, max(24, int(40 * ui_scale)))
    title_font = pygame.font.SysFont(None, max(48, int(84 * ui_scale)))
    small_font = pygame.font.SysFont(None, max(18, int(28 * ui_scale)))
    bullet_size = max(24, int(40 * ui_scale))
    bullet_image_scaled = pygame.transform.smoothscale(holyLightBullet, (bullet_size, bullet_size))
    aoe_size = max(80, int(140 * ui_scale))
    aoe_image_scaled = pygame.transform.smoothscale(aoeAttackImage, (aoe_size, aoe_size))
    target_height = max(1, int(100 * ui_scale))

    def scale_player_image(image):
        iw, ih = image.get_size()
        scale = target_height / ih
        return pygame.transform.smoothscale(image, (max(1, int(iw * scale)), target_height))

    scaled_player_sprites = {
        'idle': (scale_player_image(playerSpriteSF),
                 scale_player_image(playerSpriteSB),
                 scale_player_image(playerSpriteSL),
                 scale_player_image(playerSpriteSR)),
        'walk': (scale_player_image(playerSpriteWF),
                 scale_player_image(playerSpriteWB),
                 scale_player_image(playerSpriteWL),
                 scale_player_image(playerSpriteWR))
    }
    if 'idle' in scaled_player_sprites and playerSpriteSFrect:
        new_size = scaled_player_sprites['idle'][0].get_size()
        current_center = playerSpriteSFrect.center
        playerSpriteSFrect.size = new_size
        playerSpriteSFrect.center = current_center


def play_music(track_key):
    global current_music
    if current_music == track_key:
        return
    if track_key == 'title':
        pygame.mixer.music.load(title_music_file)
        pygame.mixer.music.play(-1)
    elif track_key == 'game':
        pygame.mixer.music.load(game_music_file)
        pygame.mixer.music.play(-1)
    elif track_key == 'easter':
        pygame.mixer.music.load(easter_music_file)
        pygame.mixer.music.play()
    current_music = track_key


def pause_music_if_game():
    if current_music == 'game':
        pygame.mixer.music.pause()


def resume_music_if_game():
    if current_music == 'game':
        pygame.mixer.music.unpause()


enemySprites = {
    'forward': [enemyWalkingFoward1, enemyWalkingFoward2],
    'back': [enemyWalkingBack1, enemyWalkingBack2],
    'left': [enemyWalkingLeft1, enemyWalkingLeft2],
    'right': [enemyWalkingRight1, enemyWalkingRight2],
}

playerSpriteSBrect = playerSpriteSB.get_rect()
playerSpriteSBW_BASE = 70
playerSpriteSBH_BASE = 100
playerSpriteSBX = 0
playerSpriteSBY = 0
playerSpriteSFrect = playerSpriteSF.get_rect()
playerSpriteSFW_BASE = 70
playerSpriteSFH_BASE = 100
playerSpriteSFX = 0
playerSpriteSFY = 0

current_stage = 1
total_stages = 10
victory_screen_active = False
game_over_active = False
game_over_selected = 0
end_menu_selected = 0
end_menu_items = ['Continue', 'Save and Continue', 'Save and Return to Title', 'Save and Close Program']
game_over_items = ['Restart from Last Save', 'Return to Title Screen', 'Quit Program']

player_health = 100
player_max_health = 100
last_damage_time = 0
damage_cooldown = 1000

aoe_cooldown = 7000
aoe_last_used = -7000
aoe_attack_effects = []

dash_cooldown = 5000  # 5 seconds
dash_last_used = -5000
dash_speed = 30  # Speed multiplier during dash
dash_duration = 200  # Duration in milliseconds
dash_active = False
dash_start_time = 0

required_kills = current_stage * 5
kill_count = 0
spawn_timer = 0
spawn_interval = 120
max_active_enemies = 10

controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'aoe': pygame.K_e,
    'dash': pygame.K_LSHIFT,
}
pause_active = False
pause_selected = 0
pause_menu_items = ['resume', 'save', 'save_and_return', 'up', 'down', 'left', 'right', 'aoe', 'dash']
rebind_mode = False
rebind_action = None

main_menu_active = True
main_menu_selected = 0
main_menu_items = ['New Game', 'Load Game', 'Quit Program']
easter_egg_active = False
konami_sequence = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a, pygame.K_b, pygame.K_a]
konami_index = 0

save_dir = 'saves'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

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


def stage_required_kills(stage):
    return stage * 5


def start_stage(reset_kills=True):
    global required_kills, kill_count, enemies, spawn_timer, victory_screen_active, end_menu_selected, player_health, last_damage_time, dash_last_used, dash_active
    required_kills = stage_required_kills(current_stage)
    if reset_kills:
        kill_count = 0
    player_health = player_max_health
    last_damage_time = 0
    dash_last_used = -5000
    dash_active = False
    enemies = spawn_enemies(required_kills)
    spawn_timer = 0
    victory_screen_active = False
    end_menu_selected = 0


def next_stage():
    global current_stage
    current_stage += 1
    if current_stage > total_stages:
        current_stage = 1
    start_stage()
    resume_music_if_game()

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
w, h = pygame.display.get_surface().get_size()
update_scaled_ui((w, h))
mousePos = pygame.mouse.get_pos()
offset = pygame.math.Vector2(0,0)
world = pygame.math.Vector2(w / 2, h / 2)
playerSpriteSFW = int(playerSpriteSFW_BASE * player_sprite_scale)
playerSpriteSFH = int(playerSpriteSFH_BASE * player_sprite_scale)
playerSpriteSFrect = pygame.Rect(world.x - playerSpriteSFW // 2, world.y - playerSpriteSFH // 2, playerSpriteSFW, playerSpriteSFH)
ground = pygame.Rect(0, h - 200, w, 200)

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
    global playerSpriteSFrect, knockbackVector, player_health, last_damage_time, damage_cooldown
    if not enemy['alive']:
        return
    if enemy['rect'].colliderect(playerSpriteSFrect):
            direction_vector = Vector2(playerSpriteSFrect.center) - Vector2(enemy['rect'].center)
            if direction_vector.length() > 0:
                direction_vector = direction_vector.normalize()
            knockback_strength = 15
            knockbackVector.x = direction_vector.x * knockback_strength
            knockbackVector.y = direction_vector.y * knockback_strength
            current_time = pygame.time.get_ticks()
            if current_time - last_damage_time > damage_cooldown:
                player_health -= 15
                player_health = max(player_health, 0)
                last_damage_time = current_time
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

def save_game(slot):
    state = {
        'player_rect': playerSpriteSFrect,
        'enemies': enemies,
        'kill_count': kill_count,
        'current_stage': current_stage,
        'player_health': player_health,
        'holylightBullets': holylightBullets,
        'boost': boost,
        'boostVector': boostVector,
        'knockbackVector': knockbackVector,
        'acceptingNewVector': acceptingNewVector,
        'inRange': inRange,
        'isWalking': isWalking,
    }
    with open(os.path.join(save_dir, f'save_{slot}.pkl'), 'wb') as f:
        pickle.dump(state, f)

def load_game(slot):
    try:
        with open(os.path.join(save_dir, f'save_{slot}.pkl'), 'rb') as f:
            state = pickle.load(f)
        global playerSpriteSFrect, enemies, kill_count, holylightBullets, boost, boostVector, knockbackVector, acceptingNewVector, inRange, isWalking, current_stage, required_kills, player_health
        playerSpriteSFrect = state['player_rect']
        enemies = state['enemies']
        kill_count = state['kill_count']
        current_stage = state.get('current_stage', 1)
        player_health = state.get('player_health', player_max_health)
        required_kills = stage_required_kills(current_stage)
        holylightBullets = state['holylightBullets']
        boost = state['boost']
        boostVector = state['boostVector']
        knockbackVector = state['knockbackVector']
        acceptingNewVector = state['acceptingNewVector']
        inRange = state['inRange']
        isWalking = state['isWalking']
        return True
    except:
        return False

def get_save_slots():
    return [f for f in os.listdir(save_dir) if f.startswith('save_') and f.endswith('.pkl')]

def handleInputs():
    global gameLoop, boost, acceptingNewVector, inRange, knockbackVector, boostVector, isWalking, screen
    global pause_active, pause_selected, rebind_mode, rebind_action, controls, victory_screen_active, end_menu_selected, main_menu_active, game_over_active, game_over_selected, aoe_last_used, aoe_attack_effects, dash_last_used, dash_active, dash_start_time
    global playerSpriteSFW, playerSpriteSFH, playerSpriteSFrect
    keys = pygame.key.get_pressed()
    isWalking = False

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            update_scaled_ui((event.w, event.h))
            if 'idle' in scaled_player_sprites:
                playerSpriteSFrect.size = scaled_player_sprites['idle'][0].get_size()
            playerSpriteSFrect.clamp_ip(screen.get_rect())
            continue
        if game_over_active:
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_over_selected = (game_over_selected - 1) % len(game_over_items)
                elif event.key == pygame.K_DOWN:
                    game_over_selected = (game_over_selected + 1) % len(game_over_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = game_over_items[game_over_selected]
                    if choice == 'Restart from Last Save':
                        global current_stage
                        current_stage = 1
                        start_stage()
                        resume_music_if_game()
                        game_over_active = False
                    elif choice == 'Return to Title Screen':
                        main_menu_active = True
                        game_over_active = False
                    elif choice == 'Quit Program':
                        gameLoop = False
            continue
        if victory_screen_active:
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    end_menu_selected = (end_menu_selected - 1) % len(end_menu_items)
                elif event.key == pygame.K_DOWN:
                    end_menu_selected = (end_menu_selected + 1) % len(end_menu_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = end_menu_items[end_menu_selected]
                    if choice == 'Continue':
                        next_stage()
                    elif choice == 'Save and Continue':
                        save_game(1)
                        next_stage()
                    elif choice == 'Save and Return to Title':
                        save_game(1)
                        main_menu_active = True
                        victory_screen_active = False
                    elif choice == 'Save and Close Program':
                        save_game(1)
                        gameLoop = False
            continue

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
                        resume_music_if_game()
                    elif event.key == pygame.K_UP:
                        pause_selected = (pause_selected - 1) % len(pause_menu_items)
                    elif event.key == pygame.K_DOWN:
                        pause_selected = (pause_selected + 1) % len(pause_menu_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected_action = pause_menu_items[pause_selected]
                        if selected_action == 'resume':
                            pause_active = False
                            resume_music_if_game()
                        elif selected_action == 'save':
                            save_game(1)
                            pause_active = False
                            resume_music_if_game()
                        elif selected_action == 'save_and_return':
                            save_game(1)
                            pause_active = False
                            main_menu_active = True
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
            elif event.key == controls['aoe'] and not victory_screen_active and not pause_active and not game_over_active:
                current_time = pygame.time.get_ticks()
                if current_time - aoe_last_used >= aoe_cooldown:
                    player_center = Vector2(playerSpriteSFrect.center)
                    direction = Vector2(mousePos) - player_center
                    if direction.length() == 0:
                        direction = Vector2(0, -1)
                    else:
                        direction = direction.normalize()
                    aoe_angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
                    aoe_attack_effects.append({
                        'pos': Vector2(player_center),
                        'angle': aoe_angle,
                        'start': current_time,
                        'duration': 700,
                        'direction': direction,
                        'speed': 28,
                        'hit_targets': set()
                    })
                    aoe_last_used = current_time

        # Handle dash input
        if keys[controls['dash']] and not dash_active:
            current_time = pygame.time.get_ticks()
            if current_time - dash_last_used >= dash_cooldown:
                dash_active = True
                dash_start_time = current_time
                dash_last_used = current_time

    if not pause_active and not victory_screen_active:
        # Calculate movement speed (increased during dash)
        current_speed = dash_speed if dash_active else playerSpeed
        
        # Check if dash should end
        if dash_active and pygame.time.get_ticks() - dash_start_time >= dash_duration:
            dash_active = False

        if keys[controls['up']]:
            playerSpriteSFrect.y -= current_speed
            isWalking = True
        if keys[controls['down']]:
            playerSpriteSFrect.y += current_speed
            isWalking = True
        if keys[controls['left']]:
            playerSpriteSFrect.x -= current_speed
            isWalking = True
        if keys[controls['right']]:
            playerSpriteSFrect.x += current_speed
            isWalking = True

    return isWalking

def draw():
    global isWalking
    direction_vector = Vector2(mousePos) - playerSpriteSFrect.center
    idle_sprites = scaled_player_sprites.get('idle', (playerSpriteSF, playerSpriteSB, playerSpriteSL, playerSpriteSR))
    walk_sprites = scaled_player_sprites.get('walk', (playerSpriteWF, playerSpriteWB, playerSpriteWL, playerSpriteWR))
    selected_idle_idx = 0
    selected_walk_idx = 0

    if direction_vector.length() > 0:
        direction = direction_vector.normalize()
        if abs(direction.y) >= abs(direction.x):
            if direction.y < 0:
                selected_idle_idx = 1
                selected_walk_idx = 1
            else:
                selected_idle_idx = 0
                selected_walk_idx = 0
        else:
            if direction.x > 0:
                selected_idle_idx = 3
                selected_walk_idx = 3
            else:
                selected_idle_idx = 2
                selected_walk_idx = 2

    if isWalking:
        frame = (pygame.time.get_ticks() // 150) % 2
        selected_sprite = walk_sprites[selected_walk_idx] if frame == 0 else idle_sprites[selected_idle_idx]
    else:
        selected_sprite = idle_sprites[selected_idle_idx]

    screen.blit(selected_sprite, playerSpriteSFrect)
    draw_player_health_bar()


def draw_player_health_bar():
    bar_width = int(playerSpriteSFrect.width * 1.4)
    bar_height = max(8, int(16 * player_sprite_scale))
    bar_x = int(playerSpriteSFrect.centerx - bar_width / 2)
    bar_y = int(playerSpriteSFrect.top - bar_height - max(8, int(12 * player_sprite_scale)))
    health_ratio = max(player_health, 0) / player_max_health
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), max(1, int(2 * player_sprite_scale)))


def draw_aoe_effects():
    if not aoe_attack_effects:
        return
    aoe_image = aoe_image_scaled if aoe_image_scaled else aoeAttackImage
    for effect in aoe_attack_effects:
        rotated = pygame.transform.rotate(aoe_image, effect['angle'])
        rect = rotated.get_rect(center=(int(effect['pos'].x), int(effect['pos'].y)))
        screen.blit(rotated, rect)


def draw_game_over_menu():
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    screen.blit(overlay, (0, 0))
    title = title_font.render('GAME OVER', True, WHITE)
    screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.10)))
    option_start_y = int(h * 0.24)
    option_spacing = max(45, int(h * 0.065))
    for idx, item in enumerate(game_over_items):
        color = GREEN if idx == game_over_selected else WHITE
        item_text = font.render(item, True, color)
        screen.blit(item_text, (w // 2 - item_text.get_width() // 2, option_start_y + idx * option_spacing))
    hint = font.render('Use Up/Down and Enter', True, (180, 180, 180))
    screen.blit(hint, (w // 2 - hint.get_width() // 2, int(h * 0.88)))


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
    screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.10)))

    option_start_y = int(h * 0.22)
    option_spacing = max(40, int(h * 0.06))
    for idx, action in enumerate(pause_menu_items):
        if action == 'resume':
            text = 'Resume'
        elif action == 'save':
            text = 'Save Game'
        elif action == 'save_and_return':
            text = 'Save and Return to Title'
        else:
            text = f"{action.capitalize()}: {get_key_name(controls[action])}"
            if rebind_mode and rebind_action == action:
                text = f"Press new key for {action.capitalize()}"
        color = (255, 200, 0) if idx == pause_selected else WHITE
        item_text = font.render(text, True, color)
        screen.blit(item_text, (w // 2 - item_text.get_width() // 2, option_start_y + idx * option_spacing))

    hint = 'Use arrow keys to navigate, Enter to select, ESC to resume'
    hint_text = font.render(hint, True, (180, 180, 180))
    screen.blit(hint_text, (w // 2 - hint_text.get_width() // 2, int(h * 0.88)))

def draw_victory_menu():
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    screen.blit(overlay, (0, 0))

    if current_stage == total_stages:
        title = title_font.render('Good job on completing the game!', True, WHITE)
        screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.10)))

        subtitle = small_font.render('Game made by.... ME!!! IM THE ONE WHO MADE THIS GAME!!!', True, WHITE)
        screen.blit(subtitle, (w // 2 - subtitle.get_width() // 2, int(h * 0.20)))

        option_start_y = int(h * 0.30)
    else:
        title = font.render(f'Stage {current_stage} Complete!', True, WHITE)
        screen.blit(title, (w // 2 - title.get_width() // 2, int(h * 0.08)))

        summary = font.render(f'{kill_count}/{required_kills} demons defeated', True, WHITE)
        screen.blit(summary, (w // 2 - summary.get_width() // 2, int(h * 0.16)))

        option_start_y = int(h * 0.24)

    option_spacing = max(45, int(h * 0.065))
    for idx, item in enumerate(end_menu_items):
        color = GREEN if idx == end_menu_selected else WHITE
        item_text = font.render(item, True, color)
        screen.blit(item_text, (w // 2 - item_text.get_width() // 2, option_start_y + idx * option_spacing))

    hint = font.render('Use Up/Down and Enter', True, (180, 180, 180))
    screen.blit(hint, (w // 2 - hint.get_width() // 2, int(h * 0.88)))


def draw_main_menu():
    if bg_scaled:
        screen.blit(bg_scaled, (0, 0))
    else:
        screen.fill(BLACK)

    title = title_font.render('And On the Third Day', True, WHITE)
    subtitle = font.render('Main Menu', True, WHITE)

    title_y = int(h * 0.08)
    subtitle_y = title_y + max(50, int(h * 0.08))
    option_start_y = subtitle_y + max(40, int(h * 0.07))
    option_spacing = max(45, int(h * 0.065))

    screen.blit(title, (w // 2 - title.get_width() // 2, title_y))
    screen.blit(subtitle, (w // 2 - subtitle.get_width() // 2, subtitle_y))

    for i, item in enumerate(main_menu_items):
        color = GREEN if i == main_menu_selected else WHITE
        text = font.render(item, True, color)
        screen.blit(text, (w // 2 - text.get_width() // 2, option_start_y + i * option_spacing))

    pygame.display.flip()

def draw_easter_egg():
    screen.fill(BLACK)
    angle = (pygame.time.get_ticks() // 5) % 360  # faster rotation
    egg_size = int(min(w, h) * 0.35)
    scaled = pygame.transform.smoothscale(enemyEasterEgg, (egg_size, egg_size))
    rotated_image = pygame.transform.rotate(scaled, angle)
    rect = rotated_image.get_rect(center=(w // 2, h // 2))
    screen.blit(rotated_image, rect)

    top_text = font.render("You try and use cheats?", True, WHITE)
    bottom_text = font.render("Now you'll have to listen to my favorite song until its done!!! (or press ESC)", True, WHITE)
    screen.blit(top_text, (w // 2 - top_text.get_width() // 2, int(h * 0.08)))
    screen.blit(bottom_text, (w // 2 - bottom_text.get_width() // 2, h - int(h * 0.12)))
    pygame.display.flip()

# Spawn the required demons for the win goal
if not enemies:
    start_stage()

while gameLoop:
    if main_menu_active:
        play_music('title')
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                update_scaled_ui((event.w, event.h))
                continue
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == konami_sequence[konami_index]:
                    konami_index += 1
                    if konami_index == len(konami_sequence):
                        easter_egg_active = True
                        main_menu_active = False
                        play_music('easter')
                        konami_index = 0
                        konami_index = 0
                else:
                    konami_index = 0
                if event.key == pygame.K_UP:
                    main_menu_selected = (main_menu_selected - 1) % len(main_menu_items)
                elif event.key == pygame.K_DOWN:
                    main_menu_selected = (main_menu_selected + 1) % len(main_menu_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if main_menu_items[main_menu_selected] == 'New Game':
                        current_stage = 1
                        start_stage()
                        main_menu_active = False
                        play_music('game')
                    elif main_menu_items[main_menu_selected] == 'Load Game':
                        slots = get_save_slots()
                        if slots:
                            if load_game(1):
                                main_menu_active = False
                                play_music('game')
                            # else show error, but for now skip
                        # else no saves
                    elif main_menu_items[main_menu_selected] == 'Quit Program':
                        gameLoop = False
        clock.tick(FPS)
        continue

    if easter_egg_active:
        draw_easter_egg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    easter_egg_active = False
                    main_menu_active = True
            elif event.type == MUSIC_END_EVENT:
                easter_egg_active = False
                main_menu_active = True
        clock.tick(FPS)
        continue

    mousePos = pygame.mouse.get_pos()
    isWalking = handleInputs()
    w, h = pygame.display.get_surface().get_size()
    update_scaled_ui((w, h))
    ground = pygame.Rect(0, h-200, w, 200)

    if pause_active:
        pause_music_if_game()
        if bg_scaled:
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill(BLACK)
        draw()
        draw_pause_menu()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    if victory_screen_active:
        pause_music_if_game()
        if bg_scaled:
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill(BLACK)
        draw()
        draw_victory_menu()
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

    if bg_scaled:
        screen.blit(bg_scaled, (0, 0))
    else:
        screen.fill(BLACK)
    clock.tick(FPS)
    draw()
    draw_aoe_effects()

    if player_health <= 0:
        game_over_active = True

    if kill_count >= required_kills:
        victory_screen_active = True
        if bg_scaled:
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill(BLACK)
        draw()
        draw_victory_menu()
        pygame.display.flip()
        continue

    if game_over_active:
        pause_music_if_game()
        if bg_scaled:
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill(BLACK)
        draw_game_over_menu()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    for enemy in enemies:
        updateEnemy(enemy)
        drawEnemy(enemy)
        enemyCollisions(enemy)

    current_time = pygame.time.get_ticks()
    remaining_aoe = aoe_cooldown - (current_time - aoe_last_used)
    aoe_radius = max(1, int((aoe_image_scaled.get_width() if aoe_image_scaled else aoeAttackImage.get_width()) * 0.65))
    for effect in aoe_attack_effects[:]:
        if current_time - effect['start'] >= effect['duration']:
            aoe_attack_effects.remove(effect)
            continue
        effect['pos'] += effect['direction'] * effect['speed']
        for enemy in enemies:
            if not enemy['alive']:
                continue
            if id(enemy) in effect['hit_targets']:
                continue
            to_enemy = Vector2(enemy['rect'].center) - effect['pos']
            if to_enemy.length() > aoe_radius:
                continue
            if to_enemy.length() == 0:
                forward_dot = 1
            else:
                forward_dot = effect['direction'].dot(to_enemy.normalize())
            if forward_dot > 0.3:
                enemy['health'] -= 5
                if enemy['health'] <= 0:
                    enemy['alive'] = False
                    kill_count += 1
                effect['hit_targets'].add(id(enemy))

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

    if bullet_image_scaled is not None:
        bullet_to_draw = bullet_image_scaled
    else:
        bullet_to_draw = holyLightBullet
    for b in holylightBullets:
        rotated_bullet = pygame.transform.rotate(bullet_to_draw, b['angle'])
        rot_rect = rotated_bullet.get_rect(center=(int(b['pos'].x), int(b['pos'].y)))
        screen.blit(rotated_bullet, rot_rect)

    stage_text = font.render(f"Stage {current_stage}/{total_stages}", True, WHITE)
    screen.blit(stage_text, (20, 20))
    goal_text = font.render(f"Demons defeated: {kill_count}/{required_kills}", True, WHITE)
    screen.blit(goal_text, (20, 60))
    cooldown_text = 'AOE Ready' if remaining_aoe <= 0 else f"AOE: {math.ceil(remaining_aoe / 1000)}s"
    cooldown_label = font.render(cooldown_text, True, WHITE)
    screen.blit(cooldown_label, (20, 100))
    
    remaining_dash = dash_cooldown - (current_time - dash_last_used)
    dash_text = 'Dash Ready' if remaining_dash <= 0 else f"Dash: {math.ceil(remaining_dash / 1000)}s"
    dash_label = font.render(dash_text, True, WHITE)
    screen.blit(dash_label, (20, 140))

    angleCalc()
    pygame.display.flip()

