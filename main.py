import os
import numpy as np
import pygame as pg
from pygame import time


def load_image(name):
    filename = os.path.join('data', name)
    try:
        image = pg.image.load(filename)
    except pg.error as error:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(error)
    return image


def load_level(filename):
    filename = os.path.join('data', filename)
    with open(filename, 'r') as map_file:
        map_level = np.array([list(i) for i in [line.strip() for line in map_file]])
    return map_level


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15,
            tile_height * pos_y + 5
        )

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15,
            tile_height * self.pos[1] + 5
        )


class Car(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cars_group)
        self.image = car_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 1,
            tile_height * pos_y + 1
        )

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 1,
            tile_height * self.pos[1] + 1
        )


def generate_level(level):
    mas, hero, x, y = None, None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '.':
                Tile('empty', x, y)
            elif level[y, x] == '#':
                Tile('road', x, y)
                level[y, x] = '.'
            elif level[y, x] == ',':
                Tile('empty', x, y)
                level[y, x] = ','
                mas = Car(x, y)
            elif level[y, x] == '@':
                Tile('empty', x, y)
                level[y, x] = '.'
                hero = Player(x, y)
    return mas, hero, x, y


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x,
            tile_height * pos_y
        )


def start():
    start_menu = True
    if start_menu:
        screen.blit(instructions_text, instructions_rect)


def move_player(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1, x] == '.' or (y > 0 and level_map[y - 1, x] == ','):
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < level_y and level_map[y + 1, x] == '.' or (y < level_y and level_map[y + 1, x] == ','):
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y, x - 1] == '.' or (x > 0 and level_map[y, x - 1] == ','):
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < level_x and level_map[y, x + 1] == '.' or (x < level_x and level_map[y, x + 1] == ','):
            hero.move(x + 1, y)
    if level_map[y - 1, x] != '.':
        screen.fill('white')


def move_car(mas):
    x, y = mas.pos
    if (x < level_x and level_map[y, x + 1] == '.') or (x < level_x and level_map[y, x + 1] == ','):
        mas.move(x + 1, y)
    if x >= level_x:
        mas.move(0, y)


if __name__ == '__main__':
    pg.init()
    fps = 30
    size = width, height = 1100, 750
    screen = pg.display.set_mode(size)

    player_image = load_image('chicken.png')
    cars_image = load_image('car.png')

    tile_images = {
        'road': load_image('road.png'),
        'empty': load_image('trava.png')
    }

    tile_width = tile_height = 50

    cars_group = pg.sprite.Group()
    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    pg.display.set_caption("Road-of-Life")
    chicken_image = pg.image.load("data/chicken.png")
    car_image = pg.image.load("data/car.png")

    level_map = load_level('level-01.map')
    pg.key.set_repeat(200, 70)
    m, player, level_x, level_y = generate_level(level_map)

    start_menu = True
    screen.fill(pg.Color('White'))
    instructions_text = pg.font.Font(None, 48).render("Press SPACE to start", True, pg.Color('Black'))
    instructions_rect = instructions_text.get_rect(center=(width // 2, height // 2))

    running = True
    while running:
        move_car(m)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    start_menu = False
                elif event.key == pg.K_UP:
                    move_player(player, 'up')
                elif event.key == pg.K_DOWN:
                    move_player(player, 'down')
                elif event.key == pg.K_LEFT:
                    move_player(player, 'left')
                elif event.key == pg.K_RIGHT:
                    move_player(player, 'right')
            if not start_menu:
                tiles_group.draw(screen)
                player_group.draw(screen)
                cars_group.draw(screen)
            elif start_menu:
                screen.blit(instructions_text, instructions_rect)
            time.Clock().tick(fps)
            pg.display.flip()


        time.Clock().tick(fps)

