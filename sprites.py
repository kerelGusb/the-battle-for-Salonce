import os
import pygame
import random


ALL_SPRITES = pygame.sprite.Group()
PLAYER_BULLET = pygame.sprite.Group()
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
        self.frames = []
        self.cut_sheet(sheet, columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.pos = [x, y]
        self.v = v
        self.start_bullet_pos = start_bullet_pos
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

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
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
        self.add(ALL_SPRITES)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.shot_bullet_pos = [self.pos[0] + self.start_bullet_pos[0],
                                self.pos[1] + self.start_bullet_pos[1]]
        if self.move_to_up:
            self.pos[1] -= self.v
            self.rect = self.rect.move((0, -self.v))
        if self.move_to_down:
            self.pos[1] += self.v
            self.rect = self.rect.move((0, self.v))
        if self.move_to_left:
            self.pos[0] -= self.v
            self.rect = self.rect.move((-self.v, 0))
        if self.move_to_right:
            self.pos[0] += self.v
            self.rect = self.rect.move((self.v, 0))
        ship_collide = pygame.sprite.spritecollideany(self, ALIEN_SPRITES)
        if ship_collide:
            self.hp -= 50
        bullet_collide = pygame.sprite.spritecollideany(self, ALIEN_BULLET_SPRITES)
        if bullet_collide:
            self.hp -= 50


class Enemy(Ship):
    def __init__(self, sheet, columns, x, y, v, start_bullet_pos, hp, *group):
        super().__init__(sheet, columns, x, y, v, start_bullet_pos, *group)
        self.hp = hp
        self.add(ALIEN_SPRITES)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.shot_bullet_pos = [self.pos[0] + self.start_bullet_pos[0],
                                self.pos[1] + self.start_bullet_pos[1]]
        self.pos[0] -= self.v
        self.rect = self.rect.move((-self.v, 0))


class Boss(Enemy):
    pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, x, y, v, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns)
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


class MainCharBullet(Bullet):
    def __init__(self, sheet, columns, x, y, v, *group):
        super().__init__(sheet, columns, x, y, v, *group)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.pos[0] += self.v
        self.rect = self.rect.move((self.v, 0))

