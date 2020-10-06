import pygame as pg
import numpy as np
import sys


def get_neighbors(matrix: np.array, r, c):
    def get(r, c):
        return 0 <= r < matrix.shape[0] and 0 <= c < matrix.shape[1] and matrix[r, c]

    neighbors_list = [get(r - 1, c - 1), get(r - 1, c), get(r - 1, c + 1), get(r, c - 1), get(r, c + 1),
                      get(r + 1, c - 1), get(r + 1, c), get(r + 1, c + 1)]

    return sum(map(bool, neighbors_list))


def random_matrix(n_cells: int):
    return np.random.randint(2, size=(n_cells, n_cells))


def zeros_matrix(n_cells: int):
    return np.zeros((n_cells, n_cells)).astype(int)


class GameOfLife(object):

    def __init__(self, width, height, n_cells, random_init=False, screen_bg=(25, 25, 25)):
        self.width = width
        self.height = height
        self.n_cells = n_cells
        self.screen = pg.display.set_mode((height, width))
        self.screen_bg = screen_bg
        self.random_init = random_init
        self.is_run = True
        self.is_game_run = False
        self.pause = False
        self.cell_h = self.height / self.n_cells
        self.cell_w = self.width / self.n_cells
        self.game_state = random_matrix(self.n_cells) if random_init else zeros_matrix(self.n_cells)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pg.K_RETURN:
                    self.is_game_run = True
                elif event.key == pg.K_ESCAPE:
                    self.is_run = False

            if not self.is_game_run:
                self.click_update(pg.mouse.get_pressed())

    def init_screen(self):
        self.screen.fill(self.screen_bg)

    def click_update(self, mouse_click):
        if sum(mouse_click) > 0:
            pos_x, pos_y = pg.mouse.get_pos()
            cel_x, cel_y = int(np.floor(pos_x / self.cell_w)), int(np.floor(pos_y / self.cell_h))
            self.game_state[cel_x, cel_y] = 1

    def run(self):
        pg.init()
        pg.display.set_caption("The Game of Life")
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

        for y in range(self.n_cells):
            for x in range(self.n_cells):

                if not self.pause:

                    n_neigh = get_neighbors(self.game_state, x, y)

                    if self.game_state[x, y] == 0 and n_neigh == 3:
                        new_game_state[x, y] = 1
                    elif self.game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        new_game_state[x, y] = 0

        self.game_state = np.copy(new_game_state)

    def restart_game(self):
        self.is_game_run = False
        self.pause = False
        self.game_state = np.zero((self.n_cells, self.n_cells))
