from game_of_life import GameOfLife

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000


def main():
    gof = GameOfLife(WINDOW_WIDTH, WINDOW_HEIGHT, 50)
    gof.run()


if __name__ == '__main__':
    main()
