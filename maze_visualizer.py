# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/26 19:40:14 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from email.mime import image

from mlx import Mlx
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from time import sleep, time
from data_test import generation
import io
import tracemalloc
import ctypes

tracemalloc.start()

def parsed_data():
    parsed = []
    with open("maze.txt", 'r') as file:
        data = file.readlines()[:20]
        for nb_d, d in enumerate(data):
            for nb_char, char in enumerate(d[:-1]):
                parsed.append([nb_char, nb_d, d[nb_char]])
    print(parsed)
    return parsed


class ImgData():
    def __init__(self, id=None, width=None, height=None, data=None, bpp=None, sl=None, iformat=None):
        self.id = id
        self.width = width
        self.height = height
        self.data = data
        self.bpp = bpp
        self.sl = sl
        self.iformat = iformat

    @staticmethod
    def image_constitution(path, m: Mlx):
        img_convert = m.mlx_png_file_to_image(m.mlx_ptr, path)
        img_id, img_width, img_height = img_convert
        img_data, img_bpp, img_sl, img_iformat = m.mlx_get_data_addr(img_id)
        image = ImgData(img_id,
                        img_width,
                        img_height,
                        img_data,
                        img_bpp,
                        img_sl,
                        img_iformat)
        return image


def create_mlx_image(width, height, m: Mlx):
    mlx_image = ImgData()
    mlx_image.id = m.mlx_new_image(m.mlx_ptr, width, height)
    mlx_image.data, mlx_image.bpp, mlx_image.sl, mlx_image.iformat = m.mlx_get_data_addr(mlx_image.id)
    return mlx_image


def image_to_memory(image_pil, mlx_image: ImgData):
    r, g, b, a = image_pil.split()
    image_pil = Image.merge("RGBA", (b, g, r, a))
    mlx_image.data[:] = image_pil._repr_png_()
    return mlx_image


class MazeVisualizer(Mlx):
    def __init__(self, width: int, height: int, theme: str) -> None:
        super().__init__()
        self.theme = theme
        self.tilesize = 32
        self.maze_width = 25
        self.maze_height = 20
        self.mlx_ptr = self.mlx_init()
        self.width, self.height = self.mlx_get_screen_size(self.mlx_ptr)[1:]
        print(self.width, self.height)
        self.win_ptr = self.mlx_new_window(self.mlx_ptr, self.width,
                                           self.height,
                                           "A_maze_ing : Game poetry")
        self.view_port = 0
        self.logo = None
        self.background = None
        self.floor = None
        self.tile = create_mlx_image(self.tilesize * 3, self.tilesize * 3, self)
        self.snapshot = Image.new('RGBA',
                                  (self.width, self.height),
                                  (255, 0, 0, 0))
        self.snap = create_mlx_image(self.width, self.height, self)
        self.wall_tile = Image.open(f"themes/{self.theme}/wall_patch.png").convert('RGBA')
        self.path_tile = Image.open(f"themes/{self.theme}/path_patch.png").convert('RGBA')
        self.wall_mask = Image.new('RGBA', (self.tilesize * 3,
                                            self.tilesize * 3), (255, 0, 0, 0))
        self.path_wall_patch = Image.alpha_composite(self.path_tile, self.wall_tile)
        self.grid = []

    def generate_floor(self):
        start_pos = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                     int(500))
        if self.floor is None:
            floor = Image.new('RGBA',
                              ((self.maze_width * 2 + 1) * self.tilesize,
                               (self.maze_height * 2 + 1) * self.tilesize))
            floor_width, floor_height = floor.size
            self.floor = create_mlx_image(floor_width, floor_height, self)
            for w in range(0, floor_width, self.tilesize):
                for h in range(0, floor_height, self.tilesize):
                    floor.paste(self.path_wall_patch, (w, h))
            image_to_memory(floor, self.floor)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.floor.id, start_pos[0], start_pos[1] - self.view_port)

    def generate_walls(self, data=None):
        start_pos = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                     int(500))
        appending = True
        if data is None:
            data = self.grid
            appending = False
        for d in data:
            binary = bin(int(d[2], 16))[2:].zfill(4)
            if appending is True:
                for letter in '0123456789ABCDEF':
                    try:
                        self.grid.pop(self.grid.index([d[0], d[1], letter]))
                    except Exception:
                        continue
                self.grid.append([d[0], d[1], d[2]])
                self.grid = sorted(self.grid, key=lambda item: int(f'{item[0]}{item[1]}'))
            pos = [start_pos[0] + d[0] * (self.tilesize * 2),
                   start_pos[1] + d[1] * (self.tilesize * 2)]
            self.wall_mask.paste(self.wall_tile, (self.tilesize, 0))
            self.wall_mask.paste(self.wall_tile, (self.tilesize * 2, self.tilesize))
            self.wall_mask.paste(self.wall_tile, (self.tilesize, self.tilesize * 2))
            self.wall_mask.paste(self.wall_tile, (0, self.tilesize))
            self.wall_mask.paste(self.path_tile, (self.tilesize, self.tilesize))
            if int(binary[-1]) == 0:
                self.wall_mask.paste(self.path_tile, (self.tilesize, 0))
            if int(binary[-2]) == 0:
                self.wall_mask.paste(self.path_tile, (self.tilesize * 2, self.tilesize))
            if int(binary[-3]) == 0:
                self.wall_mask.paste(self.path_tile, (self.tilesize, self.tilesize * 2))
            if int(binary[-4]) == 0:
                self.wall_mask.paste(self.path_tile, (0, self.tilesize))
            self.snapshot.paste(self.wall_mask, (pos[0], pos[1]))
            image_to_memory(self.wall_mask, self.tile)
            self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.tile.id, pos[0], pos[1] - self.view_port)
            yield None

    def generate_ways(self, data=None):
        start = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                 int(500))
        entrance_way = [start[0] + d * (self.tilesize * 2) for d in data[0]]
        exit_way = [start[0] + d * (self.tilesize * 2) for d in data[1]]
        entrance = ImgData.image_constitution(f"themes/{self.theme}/entrance.png", self)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, entrance.id, entrance_way[0], entrance_way[1])
        exiting = ImgData.image_constitution(f"themes/{self.theme}/exit.png", self)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, exiting.id, exit_way[0], exit_way[1])


class Controler(MazeVisualizer):
    def __init__(self, width: int, height: int, theme: str, data: list):
        super().__init__(width, height, theme)
        self.wall_builder = self.generate_walls(data)
        self.speed = 0.001
        self.running_state = True

    @staticmethod
    def close(m: Mlx):
        m.mlx_destroy_image(m.mlx_ptr, m.background.id)
        m.mlx_destroy_image(m.mlx_ptr, m.logo.id)
        m.mlx_destroy_image(m.mlx_ptr, m.floor.id)
        m.mlx_destroy_window(m.mlx_ptr, m.win_ptr)
        m.mlx_loop_exit(m.mlx_ptr)

    @staticmethod
    def erase_text(m):
        patchwork = Image.open(f"themes/{m.theme}/background_patch.png")
        p_width, p_height = patchwork.size
        background = Image.new('RGBA', (900, 400))
        for w in range(0, 900, p_width):
            for h in range(0, 400, p_height):
                background.paste(patchwork, (w, h))
        eraser = create_mlx_image(900, 400, m)
        image_to_memory(background, eraser)
        m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, eraser.id, 0, 0)
        m.mlx_destroy_image(m.mlx_ptr, eraser.id)

    @staticmethod
    def console_text(string: str, font_size: int, self: Mlx):
        image = Image.new('RGBA', (700, 300), (0, 0, 0, 200))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f'themes/{self.theme}/font.ttf', font_size)
        draw.text((150, 120), string, font=font)
        return image

    @staticmethod
    def keyboard_commands(keynum, self: MazeVisualizer):
        print(f"You've pressed key number : {keynum}")
        if keynum == 32 and self.running_state is True:
            self.erase_text(self)
            text = self.console_text('PAUSE', 60, self)
            console = create_mlx_image(700, 300, self)
            image_to_memory(text, console)
            self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, console.id, 100, 100 - self.view_port)
            self.mlx_destroy_image(self.mlx_ptr, console.id)
            self.running_state = False
            return
        if keynum == 32 and self.running_state is False:
            self.erase_text(self)
            self.running_state = True
            return
        if keynum == 65362:
            if self.speed > 0.0001:
                self.speed /= 3
                self.erase_text(self)
                text = self.console_text('SPEED ++', 60, self)
                console = create_mlx_image(700, 300, self)
                image_to_memory(text, console)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, console.id, 100, 100 - self.view_port)
                self.mlx_destroy_image(self.mlx_ptr, console.id)
        if keynum == 65364:
            if self.speed < 0.04:
                self.speed *= 3
                self.erase_text(self)
                text = self.console_text('SPEED --', 60, self)
                console = create_mlx_image(700, 300, self)
                image_to_memory(text, console)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, console.id, 100, 100 - self.view_port)
                self.mlx_destroy_image(self.mlx_ptr, console.id) 
        if keynum == 116:
            #  Change the theme of th visualizer
            theme = ['classic',
                     'classic_red',
                     'pokemon',
                     'fallout',
                     'minecraft']
            try:
                self.theme = theme[theme.index(self.theme) + 1]
            except IndexError:
                self.theme = theme[0]
            self.wall_tile = Image.open(f"themes/{self.theme}/wall_patch.png").convert('RGBA')
            self.path_tile = Image.open(f"themes/{self.theme}/path_patch.png").convert('RGBA')
            self.mlx_destroy_image(self.mlx_ptr, self.background.id)
            self.mlx_destroy_image(self.mlx_ptr, self.logo.id)
            self.mlx_destroy_image(self.mlx_ptr, self.floor.id)
            self.background = None
            self.logo = None
            self.floor = None
            base_assets(self)
            self.path_wall_patch = Image.alpha_composite(self.path_tile, self.wall_tile)
            self.generate_floor()
            self.wall_builder = self.generate_walls()

    @staticmethod
    def mouse_commands(mouse_num, x, y, self: MazeVisualizer):
        if mouse_num == 4:
            if self.view_port > 0:
                self.view_port -= 100
                base_assets(self)
                self.generate_floor()
                # for snap in self.snapshot:
                #     self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, snap[0].id, snap[1], snap[2] - self.view_port)
                # self.snap = image_to_memory(self.snapshot, self)
                image_to_memory(self.snapshot, self.snap)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.snap.id, 0, 0 - self.view_port)
                # self.mlx_destroy_image(self.mlx_ptr, snap.id)
                # self.mlx_sync(self.mlx_ptr, self.SYNC_IMAGE_WRITABLE, snap.id)
        if mouse_num == 5:
            if self.view_port < self.height:
                self.view_port += 100
                base_assets(self)
                self.generate_floor()
                # for snap in self.snapshot:
                #     self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, snap[0].id, snap[1], snap[2] - self.view_port)
                # snap = image_to_memory(self.snapshot, self)
                image_to_memory(self.snapshot, self.snap)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.snap.id, 0, 0 - self.view_port)
                # self.mlx_destroy_image(self.mlx_ptr, snap.id)
                # self.mlx_sync(self.mlx_ptr, self.SYNC_IMAGE_WRITABLE, snap.id)

    @staticmethod
    def dig(self):
        if self.running_state is False:
            return
        try:
            # for _ in range(10):
            sleep(self.speed)
            next(self.wall_builder)
        except StopIteration:
            pass


def base_assets(m: MazeVisualizer):
    if m.background is None and m.logo is None:
        patchwork = Image.open(f"themes/{m.theme}/background_patch.png")
        p_width, p_height = patchwork.size
        background = Image.new('RGBA', (m.width, m.height))
        for w in range(0, m.width, p_width):
            for h in range(0, m.height, p_height):
                background.paste(patchwork, (w, h))
        m.background = create_mlx_image(m.width, m.height, m)
        image_to_memory(background, m.background)
        m.logo = ImgData.image_constitution(f"themes/{m.theme}/logo.png", m)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.background.id, 0, 0)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.logo.id, int((m.width / 2) - (m.logo.width / 2)), 100 - m.view_port)


def controler(m: Mlx):
    m.mlx_hook(m.win_ptr, 33, 0, m.close, m)
    m.mlx_key_hook(m.win_ptr, m.keyboard_commands, m)
    m.mlx_mouse_hook(m.win_ptr, m.mouse_commands, m)
    m.mlx_loop_hook(m.mlx_ptr, m.dig, m)


def maze_visualizer() -> None:
    width = 3840
    height = 2160
    theme = 'minecraft'
    m = Controler(width, height, theme, generation)
    base_assets(m)
    m.generate_floor()
    m.mlx_loop_hook(m.mlx_ptr, controler, m)
    m.mlx_loop(m.mlx_ptr)
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    for stat in top_stats[:10]:
        print(stat)


if __name__ == '__main__':
    maze_visualizer()
