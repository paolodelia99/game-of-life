import pygame

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


def main():
    gof = GameOfLife(WINDOW_WIDTH, WINDOW_HEIGHT)

    gof.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


class GameOfLife(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run(self):
        while True:
            self.draw_grid()
        pass

    def draw_grid(self):
        pass
