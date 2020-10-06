import pygame as pg
import sys
from game_of_life import GameOfLife


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pg.font.Font("assets/ARCADECLASSIC.ttf", 50)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Menu(object):

    def __init__(self, height, width, screen_bg):
        pg.font.init()
        self.screen = pg.display.set_mode((height, width))
        self.width = width
        self.height = height
        self.bg = screen_bg
        self.font = pg.font.Font("assets/ARCADECLASSIC.ttf", 50)
        self.click = False
        self.random_init = False
        self.n_cells = 50
        self.buttons = [
            ("Play", self.font.render("Play", True, (255, 255, 255)), pg.Rect(100, 100, 205, 80), self.bg),
            ("Options", self.font.render("Options", True, (255, 255, 255)), pg.Rect(100, 200, 205, 80), self.bg),
        ]
        self.option_buttons = [
            ("Random Start", self.font.render("Random   Start", True, (255, 255, 255)), pg.Rect(100, 100, 205, 80), self.bg),
            ("Number of Cells", self.font.render("Number  of  Cells", True, (255, 255, 255)), pg.Rect(100, 200, 205, 80), self.bg),
        ]

    def draw_text(self, text, font, color, screen, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_obj, text_rect)

    def draw_buttons(self, buttons):
        for text, font, rect, color in buttons:
            pg.draw.rect(self.screen, color, rect)
            self.screen.blit(font, rect)

    def run_menu(self):
        pg.init()

        while True:
            self.refresh_screen()
            self.draw_text('Main  Menu', self.font, (255, 255, 255), self.screen, 20, 20)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    pass
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button[2].collidepoint(event.pos):
                            if button[0] == 'Play':
                                gof = GameOfLife(self.width, self.height, 50, self.random_init)
                                gof.run()
                            elif button[0] == "Options":
                                self.options_menu()

            self.draw_buttons(self.buttons)

            pg.display.update()

    def refresh_screen(self):
        self.screen.fill(self.bg)

    def options_menu(self):
        running = True
        box = InputBox(550, 200, 150, 50, str(self.n_cells))

        while running:

            words = [
                ('Options', (255, 255, 255), 20, 20),
                ('False' if not self.random_init else 'True', (255, 255, 255), 550, 100)
            ]

            self.refresh_screen()
            for text, color, x, y in words:
                self.draw_text(text, self.font, color, self.screen, x, y)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.option_buttons:
                        if button[2].collidepoint(event.pos):
                            if button[0] == 'Random Start':
                                self.random_init = not self.random_init

                box.handle_event(event)

            try:
                cells = int(box.text)
                print("rights cells")
            except Exception:
                cells = 50
                print("exception")
            finally:
                self.n_cells = cells

            box.update()
            box.draw(self.screen)

            self.draw_buttons(self.option_buttons)
            pg.display.flip()
