import argparse
from menu import Menu

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SREEN_BG = (25, 25, 25)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dimension", type=int, help="dimension of the pygame's screen")

    args = parser.parse_args()
    return args.dimension if args.dimension else WINDOW_WIDTH


def main():
    dim = parse_args()

    menu = Menu(dim, dim, SREEN_BG)
    menu.run_menu()


if __name__ == '__main__':
    main()
