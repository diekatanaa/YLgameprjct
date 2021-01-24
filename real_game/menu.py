import pygame as pg
from settings import *


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_screen = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('0', self.game.font, 15, WHITE, self.cursor_rect.x, self.cursor_rect.y, align='center')

    def blit_screen(self):
        self.game.screen.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h - 80
        self.optionsx, self.optionsy = self.mid_w, self.mid_h - 20
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_screen = True
        while self.run_screen:
            self.game.events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('Main Menu', self.game.font, 100, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align='center')
            self.game.draw_text("Start Game", self.game.font, 60, WHITE, self.startx, self.starty, align='center')
            self.game.draw_text("Options", self.game.font, 60, WHITE, self.optionsx, self.optionsy, align='center')
            self.game.draw_text("Credits", self.game.font, 60, WHITE, self.creditsx, self.creditsy, align='center')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_screen = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h - 80
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_screen = True
        while self.run_screen:
            self.game.events()
            self.check_input()
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text('Options', self.game.font, 100, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align='center')
            self.game.draw_text("Volume", self.game.font, 60, WHITE, self.volx, self.voly, align='center')
            self.game.draw_text("Controls", self.game.font, 60, WHITE, self.controlsx, self.controlsy, align='center')
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_screen = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_screen = True
        while self.run_screen:
            self.game.events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_screen = False
            self.game.screen.fill(BLACK)
            self.game.draw_text('Credits', self.game.font, 100, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align='center')
            self.game.draw_text('Made by me', self.game.font, 80, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
            self.blit_screen()
