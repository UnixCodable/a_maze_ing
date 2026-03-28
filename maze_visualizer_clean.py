# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer_clean.py                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 17:04:43 by lbordana        #+#    #+#               #
#  Updated: 2026/03/28 18:34:08 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from PIL import Image, ImageDraw, ImageFont
from 
import numpy as np
import cv2
from time import sleep, time
from data_test import generation
from typing import Generator
from config_parser import read_config


class ImgData():
    def __init__(self) -> None:
        self.id = None
        self.width = None
        self.height = None
        self.data = None
        self.bpp = None
        self.sl = None
        self.iformat = None


class MazeInterface(Mlx):
    def __init__(self, config: dict, tile_size: int) -> None:
        #  Mlx declarators
        super().__init__()
        self.mlx = self.mlx_init()
        self.maze_width = config.get('width')
        self.maze_height = config.get('height')
        self.tile_size = tile_size
        self.base_width = (self.maze_width * 2 + 1) * self.tile_size
        self.base_height = (self.maze_height * 2 + 1) * self.tile_size
        self.win_width = (self.maze_width * 2 + 1) * self.tile_size + 400
        self.win_height = (self.maze_height * 2 + 1) * self.tile_size + 700
        self.win = self.mlx_new_window(
                self.mlx,
                self.win_width,
                self.win_height,
                "A_Maze_Ing : An old gaming story"
        )
        self.pos_x = int((self.win_width / 2) - self.base_width / 2)
        self.pos_y = 500
        self.running_state = True
        self.cam = 0

    def console_text(self, string: str, font_size: int):
        image = Image.new('RGBA', (500, 300), (0, 0, 0, 200))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f'{self.theme}/font.ttf', font_size)
        draw.text((70, 120), string, font=font)
        return image

    def erase_text(self):
        p_height = self.background_texture.shape[0]
        p_width = self.background_texture.shape[1]
        background = np.zeros((400, 550, 4), dtype=np.uint8)
        for w in range(0, 550, p_width):
            for h in range(0, 400, p_height):
                h_size = 400 - h if h + p_height > 400 else p_height
                w_size = 550 - w if w + p_width > 550 else p_width
                print(h_size, w_size)
                background[h:h + h_size, w:w + w_size, 0:3] =\
                    self.background_texture[0:h_size, 0:w_size, 0:3]
                background[:, :, 3] = 255
        eraser = self.create_mlx_image(550, 400)
        self.image_to_memory(background, eraser)
        self.put_to_screen(eraser.id, 0, 0)
        self.mlx_destroy_image(self.mlx, eraser.id)

    def put_to_screen(self, img_id: any, pos_x: int, pos_y: int) -> None:
        self.mlx_put_image_to_window(self.mlx, self.win, img_id, pos_x, pos_y)

    def image_to_memory(self, array, image: ImgData) -> None:
        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, :] = array[:, :, :]

    def create_mlx_image(self, width: int, height: int) -> ImgData:
        mlx_image = ImgData()
        mlx_image.id = self.mlx_new_image(self.mlx, width, height)
        mlx_image.width, mlx_image.height = (width, height)
        mlx_image.data, mlx_image.bpp, mlx_image.sl, mlx_image.iformat = \
            self.mlx_get_data_addr(mlx_image.id)
        return mlx_image


class MazeFront(MazeInterface):
    def __init__(self, config: dict, tile_size: int,
                 theme: str = 'classic') -> None:

        #  Maze Data

        super().__init__(config, tile_size)
        self.historic = []
        self.theme = f"themes/{theme}"

        #  Maze Textures

        self.background_texture = \
            np.asarray(cv2.imread(f"{self.theme}/background_texture.png",
                                  flags=cv2.IMREAD_UNCHANGED), dtype=np.uint8)
        print(self.background_texture.shape)
        self.wall_texture = \
            np.asarray(cv2.imread(f"{self.theme}/wall_texture.png",
                                  flags=cv2.IMREAD_UNCHANGED), dtype=np.uint8)
        self.path_texture = \
            np.asarray(cv2.imread(f"{self.theme}/path_texture.png",
                                  flags=cv2.IMREAD_UNCHANGED), dtype=np.uint8)
        self.logo_texture = \
            np.asarray(cv2.imread(f"{self.theme}/logo.png",
                                  flags=cv2.IMREAD_UNCHANGED), dtype=np.uint8)
        self.wall_path = \
            np.where(self.wall_texture == 0, self.path_texture,
                     self.wall_texture)
        self.tile = self.create_mlx_image(self.tile_size * 3,
                                          self.tile_size * 3)
        self.mask = None
        self.floor = \
            self.create_mlx_image((self.maze_width * 2 + 1) * self.tile_size,
                                  (self.maze_height * 2 + 1) * self.tile_size)
        self.background = \
            self.create_mlx_image(self.win_width, self.win_height)
        self.snapshot = \
            np.zeros(((self.maze_height * 2 + 1) * self.tile_size,
                      (self.maze_width * 2 + 1) * self.tile_size, 4),
                     dtype=np.uint8)
        self.logo = self.create_mlx_image(self.logo_texture.shape[1],
                                          self.logo_texture.shape[0])
        self.snap = \
            self.create_mlx_image((self.maze_width * 2 + 1) * self.tile_size,
                                  (self.maze_height * 2 + 1) * self.tile_size)
        self.snap_buf = (np.frombuffer(self.snap.data, dtype=np.uint8).
                         reshape(self.snapshot.shape))
        self.last_bin = '1111'

    def mask_creator(self) -> None:
        tile = self.tile_size
        self.mask = np.zeros((tile * 3, tile * 3, 4), dtype=np.uint8)
        self.mask[0:tile, tile:tile*2] = self.wall_texture
        self.mask[tile:tile*2, tile*2:tile*3] = self.wall_texture
        self.mask[tile*2:tile*3, tile:tile*2] = self.wall_texture
        self.mask[tile:tile*2, 0:tile] = self.wall_texture
        self.mask[tile:tile*2, tile:tile*2] = self.path_texture

    def generate_floor(self) -> None:
        floor = np.zeros((self.base_height, self.base_width, 4),
                         dtype=np.uint8)
        for w in range(0, self.base_width, self.tile_size):
            for h in range(0, self.base_height, self.tile_size):
                floor[h:h+self.tile_size, w:w+self.tile_size] = self.wall_path
        self.image_to_memory(floor, self.floor)
        self.put_to_screen(self.floor.id, self.pos_x, self.pos_y - self.cam)

    def generate_walls(self, data: list = None) -> Generator:
        tile = self.tile_size
        if self.mask is None:
            self.mask_creator()
        for d in data:
            binary = bin(int(d[2], 16))[2:].zfill(4)
            # pos = (self.pos_x + d[0] * (tile * 2),
            #        self.pos_y + d[1] * (tile * 2))
            p_snap = (d[0] * (tile * 2),
                      d[1] * (tile * 2))
            mask = self.mask.copy()
            if int(binary[-1]) == 0:
                mask[0:tile, tile:tile*2] = self.path_texture
            if int(binary[-2]) == 0:
                mask[tile:tile*2, tile*2:tile*3] = self.path_texture
            if int(binary[-3]) == 0:
                mask[tile*2:tile*3, tile:tile*2] = self.path_texture
            if int(binary[-4]) == 0:
                mask[tile:tile*2, 0:tile] = self.path_texture
            self.snap_buf[p_snap[1]:p_snap[1] + (tile * 3),
                          p_snap[0]:p_snap[0] + (tile * 3)] = mask
            self.put_to_screen(self.snap.id, self.pos_x, self.pos_y - self.cam)
            yield

    def generate_background(self) -> None:
        p_height, p_width = self.background_texture.shape[:2]
        background = np.zeros((self.win_height, self.win_width, 4),
                              dtype=np.uint8)
        for w in range(0, self.win_width, p_width):
            for h in range(0, self.win_height, p_height):
                h_size = self.win_height - h if h + p_height > self.win_height\
                    else p_height
                w_size = self.win_width - w if w + p_width > self.win_width\
                    else p_width
                background[h:h + h_size, w:w + w_size, 0:3] =\
                    self.background_texture[0:h_size, 0:w_size, 0:3]
                background[:, :, 3] = 255
        self.image_to_memory(background, self.background)
        self.put_to_screen(self.background.id, 0, 0)

    def generate_logo(self) -> None:
        width = self.logo_texture.shape[1]
        self.image_to_memory(self.logo_texture, self.logo)
        self.put_to_screen(self.logo.id,
                           int((self.win_width / 2) - (width / 2)),
                           100 - self.cam)


class Controler(MazeFront):
    def __init__(self, config: dict, tile_size: int,
                 theme: str = 'classic') -> None:
        super().__init__(config, tile_size, theme)

    def close_window(self) -> None:
        self.mlx_loop_exit(self.mlx)

    def key_commands(self, key_num, *m):
        if key_num == 32 and self.running_state is True:
            self.erase_text()
            text = self.console_text('PAUSE', 60)
            console = self.create_mlx_image(500, 300)
            self.image_to_memory(np.asarray(text), console)
            self.put_to_screen(console.id, 20, 100)
            self.mlx_destroy_image(self.mlx, console.id)
            self.running_state = False
            return
        if key_num == 32 and self.running_state is False:
            self.erase_text()
            self.running_state = True
            return

    def mouse_commands(self, mouse_num, x, y, *a):
        logo_width = self.logo_texture.shape[1]
        if mouse_num == 4:
            if self.cam > 0:
                for _ in range(40):
                    self.cam -= 3
                    self.put_to_screen(self.background.id, 0, 0)
                    self.put_to_screen(
                        self.logo.id,
                        int((self.win_width / 2) - (logo_width / 2)),
                        100 - self.cam
                    )
                    self.put_to_screen(self.floor.id, self.pos_x,
                                       self.pos_y - self.cam)
                    self.put_to_screen(self.snap.id, self.pos_x,
                                       self.pos_y - self.cam)
        if mouse_num == 5:
            if self.cam < self.win_height:
                for _ in range(40):
                    self.cam += 3
                    self.put_to_screen(self.background.id, 0, 0)
                    self.put_to_screen(
                        self.logo.id,
                        int((self.win_width / 2) - (logo_width / 2)),
                        100 - self.cam
                    )
                    self.put_to_screen(self.floor.id, self.pos_x,
                                       self.pos_y - self.cam)
                    self.put_to_screen(self.snap.id, self.pos_x,
                                       self.pos_y - self.cam)

    def generate(self, generator: Generator):
        if self.running_state is False:
            return
        try:
            # sleep(self.speed)
            for _ in range(5):
                start = time()
                next(generator)
                end = time()
                print(end - start)
        except StopIteration:
            pass


def render():
    config = read_config("config.txt")
    m = Controler(config, 32, 'pokemon')
    generator = m.generate_walls(generation)
    m.mlx_hook(m.win, 33, 0, Controler.close_window, m)
    m.generate_background()
    m.generate_logo()
    m.generate_floor()
    m.mlx_key_hook(m.win, m.key_commands, m)
    m.mlx_mouse_hook(m.win, m.mouse_commands, m)
    m.mlx_loop_hook(m.mlx, m.generate, generator)
    m.mlx_loop(m.mlx)


if __name__ == '__main__':
    render()
