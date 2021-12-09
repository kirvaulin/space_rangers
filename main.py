# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 2000

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические рейнджеры")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color('white'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newenemy():
    zlo = Enemy()
    all_sprites.add(zlo)
    mobs.add(zlo)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Космические рейнджеры", 44, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Стрелочки для движения, пробел для стрельбы", 18,
              WIDTH / 2, HEIGHT * 3 / 5)
    draw_text(screen, "Для продолжения нажмите любую кнопку", 18,
              WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def draw_health_bar(surf, x, y, picture):
    if picture < 0:
        picture = 0
    bar_lenght = 100
    bar_height = 10
    fill = (picture / 100) * bar_lenght
    empty_bar = pygame.Rect(x, y, bar_lenght, bar_height)
    full_bar = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, pygame.Color('green'), full_bar)
    pygame.draw.rect(surf, pygame.Color('white'), empty_bar, 2)


class Starship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = pygame.transform.scale(ship_img, (50, 38))
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and \
                (pygame.time.get_ticks() - self.power_time > POWERUP_TIME):
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedX = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedX = -8
        if keystate[pygame.K_RIGHT]:
            self.speedX = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedX
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        moment = pygame.time.get_ticks()
        if moment - self.last_shot > self.shoot_delay:
            self.last_shot = moment
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 50))
        self.image = pygame.transform.scale(enemy_img, (50, 50))
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-85, -30)
        self.speedY = random.randrange(7, 11)
        self.speedX = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        if self.rect.top > HEIGHT + 10 or \
                (self.rect.left < -25 or self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-85, -30)
            self.speedY = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedY = -8

    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        moment = pygame.time.get_ticks()
        if moment - self.last_update > self.frame_rate:
            self.last_update = moment
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(pygame.Color('Black'))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
ship_img = pygame.image.load(path.join(img_dir, "starship.png")).convert()
mini_ship_img = pygame.transform.scale(ship_img, (25, 19))
mini_ship_img.set_colorkey(pygame.Color('black'))
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
explosion_anim = {}
explosion_anim['far'] = []
explosion_anim['close'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(pygame.Color('black'))
    img_far = pygame.transform.scale(img, (75, 75))
    explosion_anim['far'].append(img_far)
    img_close = pygame.transform.scale(img, (32, 32))
    explosion_anim['close'].append(img_close)
    filename = 'sonicExplosion0{}.png'.format(i)
    img_player = pygame.image.load(path.join(img_dir, filename)).convert()
    img_player.set_colorkey(pygame.Color('black'))
    explosion_anim['player'].append(img_player)
powerup_images = {}
powerup_images['shield'] = \
    pygame.image.load(path.join(img_dir, 'health.png')).convert()
powerup_images['gun'] = \
    pygame.image.load(path.join(img_dir, 'weaphon.png')).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shot.wav'))
shoot_sound.set_volume(0.4)
explore_sound = pygame.mixer.Sound(path.join(snd_dir, 'enemy.wav'))
explore_sound.set_volume(0.4)
pygame.mixer.music.load(path.join(snd_dir,
                                  'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
starship = Starship()
all_sprites.add(starship)
for i in range(8):
    newenemy()
score = 0
pygame.mixer.music.play(loops=-1)
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        upgrades = pygame.sprite.Group()
        starship = Starship()
        all_sprites.add(starship)
        for i in range(8):
            newenemy()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50
        explore_sound.play()
        expl = Explosion(hit.rect.center, 'far')
        all_sprites.add(expl)
        if random.random() > 0.95:
            upgrade = Upgrade(hit.rect.center)
            all_sprites.add(upgrade)
            upgrades.add(upgrade)
        newenemy()

    hits = pygame.sprite.spritecollide(starship, mobs,
                                       True, pygame.sprite.collide_circle)
    for hit in hits:
        starship.health -= 25
        expl = Explosion(hit.rect.center, 'close')
        all_sprites.add(expl)
        newenemy()
        if starship.health <= 0:
            death_explosion = Explosion(starship.rect.center, 'player')
            all_sprites.add(death_explosion)
            starship.hide()
            starship.lives -= 1
            starship.health = 100

    hits = pygame.sprite.spritecollide(starship, upgrades, True)
    for hit in hits:
        if hit.type == 'shield':
            starship.health += random.randrange(10, 30)
            if starship.health >= 100:
                starship.health = 100
        if hit.type == 'gun':
            starship.powerup()

    if starship.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.fill(pygame.Color('black'))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health_bar(screen, 5, 5, starship.health)
    draw_lives(screen, WIDTH - 100, 5, starship.lives,
               mini_ship_img)
    pygame.display.flip()

pygame.quit()
