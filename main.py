import os
import sys
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


def load_level(filename):
    filename = os.path.join('data', filename)
    with open(filename, 'r') as map_file:
        map_level = np.array([list(i) for i in [line.strip() for line in map_file]])
    return map_level


def generate_level(level):
    hero, x, y = None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y, x] == '.':
                Tile('empty', x, y)
            elif level[y, x] == '#':
                Tile('road', x, y)
                level[y, x] = '.'
            elif level[y, x] == ',':
                Tile('car', x, y)
            elif level[y, x] == '@':
                Tile('empty', x, y)
                level[y, x] = '.'
                hero = Player(x, y)
    return hero, x, y


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x,
            tile_height * pos_y
        )


def start_screen():
    """Вывод заставки игры"""
    intro_text = ["Лучший результат: "]
    # Выводим изображение заставки:
    start_screen_background = load_image('start.jpg')
    screen.blit(start_screen_background, (0, 0))
    # Выводим текст заставки:
    font = pg.font.Font(None, 40)
    text_coord = 420
    for line in intro_text:
        string_rendered = font.render(line, True, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # Главный игровой цикл для окна заставки:
    while True:
        for event_game in pg.event.get():
            if event_game.type == pg.QUIT:
                terminate()
            elif event_game.type == pg.KEYDOWN or event_game.type == pg.MOUSEBUTTONDOWN:
                return  # Начинаем игру
        pg.display.flip()


def move_player(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1, x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < level_y and level_map[y + 1, x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y, x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < level_x and level_map[y, x + 1] == '.':
            hero.move(x + 1, y)

            
def terminate():
    """Выход из игры"""
    # Определяем отдельную функцию выхода из игры,
    # чтобы ею можно было воспользоваться,
    # как при закрытии игрового окна,
    # так и заставки:
    pg.quit()
    sys.exit()
    
if __name__ == '__main__':
    pg.init()
    size = width, height = 1100, 750
    screen = pg.display.set_mode((size))
    player_image = load_image('chicken.png')
    tile_images = {
        'road': load_image('road.png'),
        'empty': load_image('trava.png'),
        'car': load_image('car.png')
    }
    tile_width = tile_height = 50
    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()

    pg.display.set_caption("Road-of-Life")
    chicken_image = pg.image.load("data/chicken.png")
    car_image = pg.image.load("data/car.png")
    fps = 60
    level_map = load_level('level-01.map')
    pg.key.set_repeat(200, 70)
    player, level_x, level_y = generate_level(level_map)

    start_screen()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_player(player, 'up')
                elif event.key == pg.K_DOWN:
                    move_player(player, 'down')
                elif event.key == pg.K_LEFT:
                    move_player(player, 'left')
                elif event.key == pg.K_RIGHT:
                    move_player(player, 'right')

            screen.fill(pg.Color('white'))
            tiles_group.draw(screen)
            player_group.draw(screen)
            
            time.Clock().tick(fps)
            pg.display.flip()

        time.Clock().tick(fps)

