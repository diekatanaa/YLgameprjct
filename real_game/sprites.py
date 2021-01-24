import pygame as pg
from random import uniform, choice
from settings import *
from tilemap import collide_hit_rect
import pytweening as pt
from itertools import chain
from os import path
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.shot_speed = FIREBALL_RATE
        self.damaged = False
        self.healed = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shot_speed:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Fireball(self.game, self.rot, pos, dir)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
                self.game.effects['FIREBALL'].set_volume(0.1)
                self.game.effects['FIREBALL'].play()

    def hit(self):
        self.damaged = True
        self.damage_range = chain(DAMAGE_RANGE * 2)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_range)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        if self.healed:
            try:
                self.image.fill((0, 255, 0, next(self.heal_range)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.healed = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def heal(self, amount):
        self.health += amount
        self.healed = True
        self.heal_range = chain(DAMAGE_RANGE * 2)
        self.game.effects['HEAL'].set_volume(0.3)
        self.game.effects['HEAL'].play()
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def speed_up(self, amount):
        self.shot_speed -= amount
        self.game.effects['SPELL'].set_volume(0.3)
        self.game.effects['SPELL'].play()
        if self.shot_speed < 350:
            self.shot_speed = 350


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_distant = self.target.pos - self.pos
        if target_distant.length_squared() < DETECT_RADIUS ** 2:
            self.rot = target_distant.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            drop_chance = choice([0, 0, 0, 1, 0])
            if drop_chance == 1:
                Item(self.game, self.pos, 'spell_scroll')
            self.game.effects['SPIDER_HIT'].set_volume(0.3)
            self.game.effects['SPIDER_HIT'].play()
            self.game.map_img.blit(pg.transform.rotate(self.game.corpse_img, self.rot), self.pos - vec(16, 16))

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Fireball(pg.sprite.Sprite):
    def __init__(self, game, rot, pos, dir):
        self.rot = rot
        self.groups = game.all_sprites, game.fireballs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.fireball_img
        self.image = pg.transform.rotate(self.game.fireball_img, self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-STAFF_SPREAD, STAFF_SPREAD)
        self.vel = dir.rotate(spread) * FIREBALL_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > FIREBALL_LIFETIME:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.itm_img[type]
        self.image = pg.transform.scale(self.image, (64, 64))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pt = pt.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = RANGE_AN * (self.pt(self.step / RANGE_AN) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += SPEED_AN
        if self.step > RANGE_AN:
            self.step = 0
            self.dir *= -1



