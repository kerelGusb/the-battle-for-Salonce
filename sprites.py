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
        self.got_shot = 0
        self.was_killed = False
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
            if pygame.sprite.collide_mask(self, bullet_collide):
                self.hp -= 50
                if self.hp <= 0:
                    self.was_killed = True
                if not self.is_almost_dead:
                    self.got_shot += 1
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


class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_num, hp, *group):
        super().__init__(*group)
        self.boss_num = boss_num
        self.image = load_image(f"boss_ic_{boss_num}.png")
        self.pos = [850, 300 - (self.image.get_height() // 2)]
        self.rect = self.image.get_rect().move(self.pos)
        self.hp = hp
        self.v = 6
        self.start_bullet_pos_1 = [-20, (self.image.get_height() * 2) // 15 - 4]
        self.start_bullet_pos_2 = [-20, (self.image.get_height() * 13) // 15 - 4]
        self.move_up = random.choice([True, False])
        self.start_ticks_dir = self.start_ticks_shoot = pygame.time.get_ticks()
        self.time_to_change_dir = random.randint(500, 2500)
        self.time_to_shoot = random.randint(350, 750)
        self.barrier = 800 - (self.image.get_width() + 30)
        self.got_shot = 0
        self.is_almost_dead = False
        self.is_dead = False

        self.frames = []
        self.sheet = load_image(f"boss_ic_{self.boss_num}_death.png")
        self.columns = 5
        self.cur_frame = 0
        for i in range(self.columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(self.sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        if self.is_almost_dead:
            self.image = self.frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.rect = self.image.get_rect().move(self.pos)
            if self.cur_frame == 4:
                self.is_dead = True
        if pygame.time.get_ticks() - self.start_ticks_dir > self.time_to_change_dir:
            self.move_up = not self.move_up
            self.start_ticks_dir = pygame.time.get_ticks()
            self.time_to_change_dir = random.randint(1000, 4000)
        if pygame.time.get_ticks() - self.start_ticks_shoot > self.time_to_shoot:
            self.shoot()
            self.start_ticks_shoot = pygame.time.get_ticks()
            self.time_to_shoot = random.randint(700, 1500)
        if self.pos[0] > self.barrier:
            self.pos[0] -= self.v
        else:
            if self.move_up:
                self.pos[1] -= self.v
                if self.pos[1] - self.v < 0:
                    self.move_up = not self.move_up
                    self.start_ticks_dir = pygame.time.get_ticks()
                    self.time_to_change_dir = random.randint(1000, 4000)
            else:
                self.pos[1] += self.v
                if self.pos[1] + self.v + self.image.get_height() > 600:
                    self.move_up = not self.move_up
                    self.start_ticks_dir = pygame.time.get_ticks()
                    self.time_to_change_dir = random.randint(1000, 4000)
        bullet_collide = pygame.sprite.spritecollideany(self, PLAYER_BULLET)
        if bullet_collide:
            if pygame.sprite.collide_mask(self, bullet_collide):
                if not self.is_almost_dead:
                    self.got_shot += 1
                    self.hp -= 50
                    bullet_collide.kill()
        if self.hp <= 0:
            self.is_almost_dead = True
        self.rect = self.image.get_rect().move(self.pos)

    def shoot(self):
        shot_bullet_pos = random.choice([self.start_bullet_pos_1, self.start_bullet_pos_2])
        shot_bullet_pos = [self.pos[0] + shot_bullet_pos[0],
                           self.pos[1] + shot_bullet_pos[1]]
        AlienBullet("bullet_alien.png", 4, *shot_bullet_pos,
                    self.v * 2, ALL_SPRITES, ALIEN_BULLET_SPRITES)
        self.time_to_shoot = random.randint(350, 750)
        self.start_ticks_shoot = pygame.time.get_ticks()


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
