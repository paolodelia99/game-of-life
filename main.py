from game_of_life import GameOfLife
from menu import Menu

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SREEN_BG = (25, 25, 25)


def main():
    menu = Menu(WINDOW_HEIGHT, WINDOW_WIDTH, SREEN_BG)
    menu.run_menu()


if __name__ == '__main__':
    main()
