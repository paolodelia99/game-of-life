import pygame as pg
import sys


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

    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font("assets/ARCADECLASSIC.ttf", 50)
        self.click = False
        self.random_init = False
        self.n_cells = 50
        self.buttons = [
            ("Play", self.font.render("Play", True, (255, 255, 255)), pg.Rect(100, 100, 205, 80), (25, 25, 25)),
            ("Options", self.font.render("Options", True, (255, 255, 255)), pg.Rect(100, 200, 205, 80), (25, 25, 25)),
        ]
        self.option_buttons = [
            ("Random Start", self.font.render("Random Start", True, (255, 255, 255)), pg.Rect(100, 100, 205, 80), (25, 25, 25)),
            ("Number of Cells", self.font.render("Number of Cells", True, (255, 255, 255)), pg.Rect(100, 200, 205, 80), (25, 25, 25)),
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
                                return self.random_init, self.n_cells
                            elif button[0] == "Options":
                                self.options_menu()

            self.draw_buttons(self.buttons)

            pg.display.update()

    def refresh_screen(self):
        self.screen.fill((25, 25, 25))

    def options_menu(self):
        running = True
        box = InputBox(550, 200, 205, 80, str(self.n_cells))

        while running:

            self.refresh_screen()
            self.draw_text('Options', self.font, (255, 255, 255), self.screen, 20, 20)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button[2].collidepoint(event.pos):
                            if button[0] == 'Random Start':
                                self.random_init = True

                box.handle_event(event)

            try:
                self.n_cells = int(box.text)
            except Exception:
                print('Cannot parse text in the box')
                self.n_cells = 50

            box.update()
            self.refresh_screen()
            box.draw(self.screen)

            self.draw_buttons(self.option_buttons)
            pg.display.flip()
