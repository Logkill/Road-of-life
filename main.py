import os
import numpy as np
import pygame as pg
from pygame import time

import sys


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
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for tile in tiles_group:
            camera.apply(tile)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15,
            tile_height * 6 + 5
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
            elif level[y, x] == '0':
                Tile('rir', x, y)
                level[y, x] = '0'
            elif level[y, x] == ',':
                Tile('empty', x, y)
                level[y, x] = ','
                mas = Car(x, y)
            elif level[y, x] == '@':
                Tile('empty', x, y)
                level[y, x] = '.'
                hero = Player(x, y)
    return mas, hero, x, y


class Camera:
    def __init__(self):
        self.dx, self.dy = 0, 0

    def apply(self, obj):
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self):
        self.dx, self.dy = 0, 0


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def start_screen():
    screen.fill(pg.Color('White'))
    screen.blit(load_image('start.jpg'), (0, 0))
    while True:
        for event_game in pg.event.get():
            if event_game.type == pg.QUIT:
                terminate()
            elif event_game.type == pg.KEYDOWN or event_game.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()


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


def move_car(mas):
    x, y = mas.pos
    if (x < level_x and level_map[y, x + 1] == '.') or (x < level_x and level_map[y, x + 1] == ','):
        mas.move(x + 1, y)
    elif x < level_x and level_map[y, x + 1] == '0' or x >= level_x:
        mas.move(0, y)


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    fps = 60
    size = width, height = 1100, 750
    screen = pg.display.set_mode(size)

    player_image = load_image('chicken.png')
    cars_image = load_image('car.png')

    tile_images = {
        'rir': load_image('water.png'),
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

    camera = Camera()
    start_menu = True
    start_screen()

import os
import numpy as np
import pygame as pg
from pygame import time

import sys


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
        self.y_velocity = 0
        self.bounce_height = 10
        self.bounce_speed = 2
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15,
            tile_height * pos_y + 5
        )

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for tile in tiles_group:
            camera.apply(tile)
        for car in cars_group:
            camera.apply(car)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15,
            tile_height * 6 + 5
        )

    def update(self):
        self.rect.move_ip(0, self.y_velocity)
        if self.rect.bottom >= height - tile_height:
            self.rect.bottom = height - tile_height
            self.y_velocity = -self.bounce_height
        self.y_velocity += self.bounce_speed


class Car(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cars_group)
        self.image = car_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)

    def move(self, x, y):
        self.pos = (x, y)


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
            elif level[y, x] == '0':
                Tile('rir', x, y)
                level[y, x] = '0'
            elif level[y, x] == ',':
                Tile('empty', x, y)
                level[y, x] = ','
                mas = Car(x, y)
            elif level[y, x] == '@':
                Tile('empty', x, y)
                level[y, x] = '.'
                hero = Player(x, y)
    return mas, hero, x, y


class Camera:
    def __init__(self):
        self.dx, self.dy = 0, 0

    def apply(self, obj):
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self):
        self.dx, self.dy = 0, 0


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def start_screen():
    screen.fill(pg.Color('White'))
    screen.blit(load_image('start.jpg'), (0, 0))
    while True:
        for event_game in pg.event.get():
            if event_game.type == pg.QUIT:
                terminate()
            elif event_game.type == pg.KEYDOWN or event_game.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()


def move_player(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1, x] == '.':
            hero.move(x, y - 1)
        else:
            death()
    elif movement == 'down':
        if y < level_y and level_map[y + 1, x] == '.':
            hero.move(x, y + 1)
        else:
            death()
    elif movement == 'left':
        if x > 0 and level_map[y, x - 1] == '.':
            hero.move(x - 1, y)
        else:
            death()
    elif movement == 'right':
        if x < level_x and level_map[y, x + 1] == '.':
            hero.move(x + 1, y)
        else:
            death()


def move_car(mas):
    x, y = mas.pos
    if (x < level_x and level_map[y, x + 1] == '.') or (x < level_x and level_map[y, x + 1] == ','):
        mas.move(x + 1, y)
    elif x < level_x and level_map[y, x + 1] == '0' or x >= level_x:
        mas.move(0, y)


def death():
    waiting = True
    screen.blit(load_image('DeadScreen.png'), (0, 0))
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.K_SPACE:
                terminate()
        pg.display.flip()


def terminate():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    pg.init()
    fps = 60
    size = width, height = 1100, 750
    screen = pg.display.set_mode(size)

    player_image = load_image('chicken.png')
    cars_image = load_image('car.png')

    tile_images = {
        'rir': load_image('water.png'),
        'road': load_image('road.png'),
        'empty': load_image('trava.png')
    }

    tile_width = tile_height = 50

    cars_group = pg.sprite.Group()
    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()
    tiles_group.add(cars_group)

    pg.display.set_caption("Road-of-Life")
    chicken_image = pg.image.load("data/chicken.png")
    car_image = pg.image.load("data/car.png")

    level_map = load_level('level-01.map')
    pg.key.set_repeat(200, 70)
    m, player, level_x, level_y = generate_level(level_map)

    camera = Camera()
    start_menu = True
    start_screen()

    # загружаем музыку
    pg.mixer.music.load("musik.mp3")
    clock = pg.time.Clock()
    # vol уровень громкости
    vol = 1.0
    flPause = False
    running = True
    # запустим фоновую музыку с бесконечным повторением
    pg.mixer.music.play(-1)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # при нажатии клавиш стрелка вверх, вниз, вправо или лево
            # вызывается функция move_player с параметром 'up', 'down', 'left' или 'right'
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
                # при нажатии на Pause Break музыка выключаетя или включается
                # в зависимости от положения до этого
                elif event.key == pg.K_m:
                    flPause = not flPause
                    if flPause:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                # при нажатии на F1 или F2 звук уменьшаетсяся и увеличивается
                elif event.type == pg.K_F1:
                    vol -= 1.0
                    pg.mixer.music.set_volume(vol)
                elif event.type == pg.K_F2:
                    vol += 1.0
                    pg.mixer.music.set_volume(vol)
            if not start_menu:
                tiles_group.draw(screen)
                player_group.draw(screen)
                cars_group.draw(screen)

        time.Clock().tick(fps)
        pg.display.flip()

