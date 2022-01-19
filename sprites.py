import os
import pygame
import random


ALL_SPRITES = pygame.sprite.Group()
PLAYER_BULLET = pygame.sprite.Group()
BONUSES = pygame.sprite.Group()
HEARTS = pygame.sprite.Group()
ALIEN_SPRITES = pygame.sprite.Group()
ALIEN_BULLET_SPRITES = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data/images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Background(pygame.sprite.Sprite):
    def __init__(self, bg, *group):
        super().__init__(*group)
        self.image = bg
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        clock.tick(16)
        self.rect = self.rect.move(-1, 0)


class Ship(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, x, y, v, start_bullet_pos, *group):
        super().__init__(*group)
        self.pos = [x, y]
        self.v = v
        self.start_sheet = sheet
        self.start_bullet_pos = start_bullet_pos
        self.set_image(sheet, columns, *self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.start_ticks = pygame.time.get_ticks()
        self.shot_bullet_pos = [self.pos[0] + start_bullet_pos[0],
                                self.pos[1] + start_bullet_pos[1]]
        self.add(ALL_SPRITES)

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def set_image(self, sheet, columns, x, y):
        self.frames = []
        self.cut_sheet(load_image(sheet), columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.shot_bullet_pos = [self.pos[0] + self.start_bullet_pos[0],
                                self.pos[1] + self.start_bullet_pos[1]]


class MainCharacter(Ship):
    def __init__(self, sheet, columns, x, y, v, start_bullet_pos, *group):
        super().__init__(sheet, columns, x, y, v, start_bullet_pos, *group)
        self.move_to_up = False
        self.move_to_down = False
        self.move_to_left = False
        self.move_to_right = False
        self.hp = 150
        self.harmless = True  # неуязвимость после удара
        self.is_almost_dead = False
        self.is_dead = False
        self.add(ALL_SPRITES)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        if not self.is_almost_dead:
            self.shot_bullet_pos = [self.pos[0] + self.start_bullet_pos[0],
                                    self.pos[1] + self.start_bullet_pos[1]]
            if self.move_to_up and self.pos[1] >= 0:
                self.pos[1] -= self.v
                self.rect = self.rect.move((0, -self.v))
            if self.move_to_down and self.pos[1] <= 600 - self.image.get_height():
                self.pos[1] += self.v
                self.rect = self.rect.move((0, self.v))
            if self.move_to_left and self.pos[0] >= 0:
                self.pos[0] -= self.v
                self.rect = self.rect.move((-self.v, 0))
            if self.move_to_right and self.pos[0] <= 800 - self.image.get_width():
                self.pos[0] += self.v
                self.rect = self.rect.move((self.v, 0))
            if self.hp <= 0:
                self.is_almost_dead = True
                self.set_image("new_hero_ic_loop_death.png", 7, *self.pos)
            if self.harmless:
                if pygame.time.get_ticks() - self.start_ticks > 2000:
                    self.set_image("new_hero_ic_loop.png", 4, *self.pos)
                    self.harmless = False
            ship_collide = pygame.sprite.spritecollideany(self, ALIEN_SPRITES)
            if ship_collide:
                if pygame.sprite.collide_mask(self, ship_collide):
                    if not self.harmless:
                        self.get_hit()
            bullet_collide = pygame.sprite.spritecollideany(self, ALIEN_BULLET_SPRITES)
            if bullet_collide:
                if pygame.sprite.collide_mask(self, bullet_collide):
                    if not self.harmless:
                        self.get_hit()
        else:
            if self.cur_frame == 6:
                self.is_dead = True

    def get_hit(self):
        self.hp -= 50
        self.start_ticks = pygame.time.get_ticks()
        self.harmless = True
        self.set_image("new_hero_ic_loop_hit_2.png", 4, *self.pos)


class Enemy(Ship):
    def __init__(self, sheet, columns, x, y, v, start_bullet_pos, hp, *group):
        super().__init__(sheet, columns, x, y, v, start_bullet_pos, *group)
        self.enemy_death_im = {"enemy_ic_loop_1_16.png": "enemy_ic_1_death.png",
                               "enemy_ic_loop_2_6.png": "enemy_ic_2_death.png",
                               "enemy_ic_loop_3_4.png": "enemy_ic_3_death.png"}
        self.hp = hp
        self.add(ALIEN_SPRITES)
        self.shot_time_dist = random.randint(700, 1500)
        self.is_almost_dead = False
        self.is_dead = False

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.shot_bullet_pos = [self.pos[0] + self.start_bullet_pos[0],
                                self.pos[1] + self.start_bullet_pos[1]]
        self.pos[0] -= self.v
        self.rect = self.rect.move((-self.v, 0))
        if pygame.time.get_ticks() - self.start_ticks > self.shot_time_dist:
            self.shot()
        bullet_collide = pygame.sprite.spritecollideany(self, PLAYER_BULLET)
        if bullet_collide:
            self.hp -= 50
            bullet_collide.kill()
        if self.hp <= 0 and not self.is_almost_dead:
            self.is_almost_dead = True
            self.set_image(self.enemy_death_im[self.start_sheet], 5, *self.pos)
        if self.is_almost_dead and self.cur_frame == 4:
            self.kill()
        if self.pos[0] < -100:
            self.kill()

    def shot(self):
        AlienBullet("bullet_alien.png", 4, *self.shot_bullet_pos,
                    self.v * 2, ALL_SPRITES, ALIEN_BULLET_SPRITES)
        self.shot_time_dist = random.randint(700, 1500)
        self.start_ticks = pygame.time.get_ticks()


class Boss(Enemy):
    pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, x, y, v, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(load_image(sheet), columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pos = [x, y]
        self.v = v
        self.add(ALL_SPRITES)

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class AlienBullet(Bullet):
    def __init__(self, sheet, columns, x, y, v, *group):
        super().__init__(sheet, columns, x, y, v, *group)
        self.add(ALIEN_BULLET_SPRITES)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.pos[0] -= self.v
        self.rect = self.rect.move((-self.v, 0))
        if self.pos[0] > 900:
            self.kill()


class MainCharBullet(Bullet):
    def __init__(self, sheet, columns, x, y, v, *group):
        super().__init__(sheet, columns, x, y, v, *group)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.pos[0] += self.v
        self.rect = self.rect.move((self.v, 0))
        if self.pos[0] > 900:
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, char, hp_to_disable, pos, *group):
        super().__init__(*group)
        self.char = char
        self.hp_to_disable = hp_to_disable
        self.image = load_image("full_heart.png")
        self.enabled = True
        self.rect = self.image.get_rect().move(pos)
        self.pos = pos

    def update(self):
        if self.hp_to_disable >= self.char.hp and self.enabled:
            self.image = load_image("empty_heart.png")
            self.enabled = False
        elif self.hp_to_disable < self.char.hp and not self.enabled:
            self.image = load_image("full_heart.png")
            self.enabled = True


class Battery(pygame.sprite.Sprite):
    def __init__(self, inc_charge_time_dist, pos, *group):
        super().__init__(*group)
        self.inc_charge_time_dist = inc_charge_time_dist
        self.images = []
        for i in range(11):
            self.images.append(load_image(f"battery_charge/battery_charge_{i}.png"))
        self.charge = 10
        self.image = self.images[self.charge]
        self.rect = self.image.get_rect().move(pos)
        self.pos = pos
        self.time_to_inc_charge = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.time_to_inc_charge > self.inc_charge_time_dist and \
                self.charge < 10:
            self.charge += 1
            self.time_to_inc_charge = pygame.time.get_ticks()
        self.image = self.images[self.charge]
