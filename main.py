import pygame as pg
import sys

pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Road-of-Life")
chicken_image = pg.image.load("chicken.png")
car_image = pg.image.load("car.png")


start_menu = True
screen.fill(pg.Color('White'))
instructions_text = pg.font.Font(None, 48).render("Press SPACE to start", True, pg.Color('Black'))
instructions_rect = instructions_text.get_rect(center=(width // 2, height // 2))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if start_menu and keys[pg.K_SPACE]:
        start_menu = False
    if not start_menu:
        screen.fill(pg.Color('Black'))
    if start_menu:
        screen.blit(instructions_text, instructions_rect)

    pg.display.flip()
