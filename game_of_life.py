import pygame as pg
import numpy as np


class GameOfLife(object):

    def __init__(self, width, height, nx_cells, ny_cells):
        self.width = width
        self.height = height
        self.n_cells = nx_cells
        self.cell_w = width / nx_cells
        self.cell_h = height / ny_cells
        self.screen = pg.display.set_mode((height, width))
        self.game_state = np.zeros((nx_cells, ny_cells)).astype(int)
        self.is_run = True
        self.is_game_run = False
        self.pause = False

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pg.K_RETURN:
                    self.is_game_run = True

            if not self.is_game_run:
                self.click_update(pg.mouse.get_pressed())

    def init_screen(self):
        self.screen.fill((25, 25, 25))

    def click_update(self, mouse_click):
        if sum(mouse_click) > 0:
            pos_x, pos_y = pg.mouse.get_pos()
            cel_x, cel_y = int(np.floor(pos_x / self.cell_w)), int(np.floor(pos_y / self.cell_h))
            self.game_state[cel_x, cel_y] = 1

    def run(self):
        pg.init()
        py.display.set_caption("The Game of Life")
        self.init_screen()

        while self.is_run:
            self.init_screen()
            self.event_loop()
            self.draw_grid()

            if self.is_game_run:
                self.update_game_state()

            pg.display.flip()

    def draw_grid(self):
        for x in range(self.n_cells):
            for y in range(self.n_cells):

                poly = [(x * self.cell_w, y * self.cell_h),
                        ((x + 1) * self.cell_w, y * self.cell_h),
                        ((x + 1) * self.cell_w, (y + 1) * self.cell_h),
                        (x * self.cell_w, (y + 1) * self.cell_h)]

                if self.game_state[x, y] == 0:
                    pg.draw.polygon(self.screen, (128, 128, 128), poly, 1)
                else:
                    pg.draw.polygon(self.screen, (255, 255, 255), poly, 0)

    def update_game_state(self):

        new_game_state = np.copy(self.game_state)

        for y in range(0, self.n_cells):
            for x in range(self.n_cells):

                if not self.pause:

                    n_neigh = self.game_state[(x - 1) % self.n_cells, (y - 1) % self.n_cells] + \
                              self.game_state[x % self.n_cells, (y - 1) % self.n_cells] + \
                              self.game_state[(x + 1) % self.n_cells, (y - 1) % self.n_cells] + \
                              self.game_state[(x - 1) % self.n_cells, y % self.n_cells] + \
                              self.game_state[(x + 1) % self.n_cells, y % self.n_cells] + \
                              self.game_state[(x - 1) % self.n_cells, (y + 1) % self.n_cells] + \
                              self.game_state[x % self.n_cells, (y + 1) % self.n_cells] + \
                              self.game_state[(x + 1) % self.n_cells, (y + 1) % self.n_cells]

                    if self.game_state[x, y] == 0 and n_neigh == 3:
                        new_game_state[x, y] = 1
                    elif self.game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        new_game_state[x, y] = 0

        self.game_state = np.copy(new_game_state)
