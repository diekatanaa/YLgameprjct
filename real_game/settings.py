import pygame as pg
vec = pg.math.Vector2

# defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Pixi's Story"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tree.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'pixi.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(20, 5)
DAMAGE_RANGE = [i for i in range(0, 256, 25)]

# Staff settings
FIREBALL_IMG = 'fireball.png'
FIREBALL_SPEED = 500
FIREBALL_LIFETIME = 2000
FIREBALL_RATE = 1000
KICKBACK = 200
STAFF_SPREAD = 5
FIREBALL_DAMAGE = [30, 40, 50, 75, 100]

# Sound
BG_MUSIC = 'background.wav'
EFF = {'FIREBALL': 'fireball.wav',
       'HEAL': 'heal.wav',
       'SPELL': 'spell_upgrade.wav',
       'SPIDER_HIT': 'spider_dead.wav',
       'PLAYER_DEATH': 'player_dead.wav',
       'PLAYER_HIT': 'player_damaged.wav'}

# Items
ITM = {'heal': 'heal_potion.png',
       'spell_scroll': 'scroll.png'}
HEAL_AMOUNT = 25
RATE_UP_AMOUNT = 75

RANGE_AN = 20
SPEED_AN = 0.6

# Mob settings
MOB_IMG = 'spider.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DEAD_MOB_IMAGE = 'dead_spider.png'
DETECT_RADIUS = 550
