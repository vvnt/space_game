# !/usr/bin/python3
# -*- coding: utf-8 -*-

# source inspiration : https://realpython.com/pygame-a-primer/

import pygame
import pygame.locals
import random

# game
game_speed = 50  # FPS
game_font = 'Terminal'
game_statut = 'menu'  # 'menu', 'play' or 'over'
game_title = 'SpaceGame'
game_music = 'digital_native.mp3'  # http://ericskiff.com/music/
screen_size = (400, 600)
screen_color = (33, 37, 43)
color_main = (231, 76, 60)
color_accent = (52, 152, 219)
color_neutral = (130, 130, 130)
color_soft = (200, 200, 200)

# player
player_pos_start = (100, screen_size[1] / 10)
player_size = (75, 25)
player_color = (255, 255, 255)
player_speed = 10
gun_cooldown = 300

# enemy
enemy_size = (5, 35)
enemy_color = (40, 40, 40)
enemy_angle = 0


class Player(pygame.sprite.Sprite):
    """player"""

    def __init__(self):
        super(Player, self).__init__()
        self.speed = player_speed
        self.surf_down = pygame.image.load(r'img\player\space_ship.png').convert_alpha()
        self.surf_up = pygame.image.load(r'img\player\space_ship_up.png').convert_alpha()
        self.surf_left = pygame.image.load(r'img\player\space_ship_left.png').convert_alpha()
        self.surf_right = pygame.image.load(r'img\player\space_ship_right.png').convert_alpha()
        self.surf = self.surf_down
        self.rect = self.surf.get_rect().move(player_pos_start)
        self.effect_shoot = pygame.mixer.Sound(r'effect\shoot.wav')

    def update(self, pressed_keys):
        if pressed_keys[pygame.locals.K_UP]:
            self.rect.move_ip(0, -self.speed)
            self.surf = self.surf_up

        elif pressed_keys[pygame.locals.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        elif pressed_keys[pygame.locals.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.surf = self.surf_left

        elif pressed_keys[pygame.locals.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.surf = self.surf_right

        else:
            self.rect.move_ip(0, 4)
            self.surf = self.surf_down

        # keep on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_size[1] - 70:
            self.rect.bottom = screen_size[1] - 70

    def shoot(self):
        self.effect_shoot.play(loops=0, maxtime=0)
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    """bullet"""

    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((2, 20))
        self.surf.fill(color_accent)
        self.rect = self.surf.get_rect().move(x, y)
        self.speed = 20
        self.strenght = 10

    def update(self):
        # allow different enemies direction
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < screen_rect.top:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """enemy"""

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf_original = pygame.image.load(r'img\enemies\asteroid_{}.png'.format(random.randint(1, 3))).convert_alpha()
        self.surf = self.surf_original
        self.rect = self.surf.get_rect().move(random.randint(0, screen_size[1]) + 20, 0)
        self.speed = random.randint(3, 13)
        self.rotation_angle = 0
        self.rotation_speed = random.randint(1, 4)
        self.rotation_direction = random.randint(-1, 1)
        self.live = 100

    def update(self):
        # allow different enemies direction
        self.speed_lateral = random.randint(-1, 1)
        self.rect.move_ip(self.speed_lateral, self.speed)
        if self.rect.bottom > screen_rect.bottom:
            self.kill()  # remove or kill ?
        if self.rect.left < 0:
            self.speed_lateral = self.speed_lateral * -1
        elif self.rect.right > screen_size[0]:
            self.speed_lateral = self.speed_lateral * -1

        # enemies rotation
        # rotation of original image (not copy) to avoid increasing image size (pygame doc)
        self.surf = pygame.transform.rotate(self.surf_original, self.rotation_angle * self.rotation_direction)
        # increase angle and prevents angle to overflow
        self.rotation_angle += self.rotation_speed % 360


class Cloud(pygame.sprite.Sprite):
    """intergalactic cloud"""

    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface((random.randint(2, 8), random.randint(90, 180)))
        self.surf.fill((random.randint(41, 42), random.randint(43, 45), random.randint(51, 53)))
        self.rect = self.surf.get_rect().move(random.randint(0, screen_size[1]), -200)
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > screen_size[1] + 200:
            self.kill()


def display_text(text, color=color_neutral, size=30, pos=(200, 300), font=game_font):
    font = pygame.font.SysFont(font, size, bold=False, italic=False)
    textsurface = font.render(str(text), False, color)

    return screen.blit(textsurface, pos)


pygame.init()

# Music
pygame.mixer.init()
pygame.mixer.music.load(r'music\digital_native.mp3')
# number of times to repeat after ﬁrst run-through, -1 to repeat indeﬁnitely
pygame.mixer.music.play(loops=-1)

# allow font in the game
pygame.font.init()

# window caption
pygame.display.set_caption(game_title)

# screen creation according to a size
screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()

# custom event for adding a new nnemy every x milliseconds
ADDENEMY = pygame.USEREVENT + 1  # event not defined in the system, give Event a number between USEREVENT and NUMEVENTS
pygame.time.set_timer(ADDENEMY, 250)  # event will be in the event queue every x ms
enemies = pygame.sprite.Group()

# custom event for adding a new Enemy every x milliseconds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 10)
clouds = pygame.sprite.Group()

player = Player()
bullets = pygame.sprite.Group()


all_sprites = pygame.sprite.Group()
all_sprites.add(player)


enemy_trigger = 1

running = True

clock = pygame.time.Clock()

score = 0
score_last = 0
score_highest = 0
score_incr = 1

while running:

    # limit the game to x frame per second (FPS)
    clock.tick(game_speed)

    # score increase for each loop
    score = score + score_incr

    # pick the highest - max - score (past or current)
    score_highest = max(score_highest, score)

    for event in pygame.event.get():

        if event.type == pygame.locals.KEYDOWN:
            # allow player to leave at anytime
            if event.key == pygame.locals.K_ESCAPE:
                running = False
            if game_statut == 'over' and event.key == pygame.locals.K_SPACE:
                game_statut = 'play'
                score = 0
                score_incr = 1
                all_sprites.add(player)
            if event.key == pygame.locals.K_SPACE:
                game_statut = 'play'
                player.shoot()

        elif event.type == pygame.locals.QUIT:
            running = False
        elif event.type == ADDENEMY and game_statut == 'play':
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    # update elements
    enemies.update()
    clouds.update()
    bullets.update()

    # draw over previous image (previous loop)
    screen.fill(screen_color)

    for cloud in clouds:
        # blit : paste image to the screen
        screen.blit(cloud.surf, cloud.rect)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    display_text(game_title, color=color_soft, size=40, pos=(200, 540))

    # collisions
    # collision player with enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        score_last = score
        game_statut = 'over'

    # collision bullet with enemies
    pygame.sprite.groupcollide(bullets, enemies, True, True)

    if game_statut == 'menu':
        display_text('Are you ready?', color=color_accent, size=50, pos=(30, screen_rect.centery))
        display_text('Press "Space" to start', color=color_accent, size=20, pos=(30, screen_rect.centery + 50))

    if game_statut == 'play':
        display_text(f'score : {score} - higest score : {score_highest}', color=color_soft, size=17, pos=(10, 10))

    if game_statut == 'over':
        score_incr = 0
        display_text('Game Over', color=color_accent, size=60, pos=(30, screen_rect.centery))
        display_text(f'Final score : {score_last}', color=color_neutral, size=30, pos=(30, screen_rect.centery + 50))
        display_text('Press "Space" to restart', color=color_accent, size=20, pos=(30, screen_rect.centery + 80))

    # refresh screen to changes into account
    pygame.display.flip()
