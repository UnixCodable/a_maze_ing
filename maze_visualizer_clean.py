# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer_clean.py                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 17:04:43 by lbordana        #+#    #+#               #
#  Updated: 2026/03/27 23:34:32 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from time import sleep, time
from data_test import generation
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
        self.position_x = int((self.win_width / 2) - ((self.maze_width / 2) *
                              self.tile_size * 2))
        self.position_y = 500
        self.view_port = 0

    def close_window(self) -> None:
        self.mlx_loop_exit(self.mlx)

    def image_to_memory(self, array, image: ImgData) -> None:
        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, 0] = array[:, :, 2]
        buffer[:, :, 1] = array[:, :, 1]
        buffer[:, :, 2] = array[:, :, 0]
        buffer[:, :, 3] = array[:, :, 3]

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
        #  Maze declarators
        super().__init__(config, tile_size)
        self.theme = f"themes/{theme}"
        #  Maze Textures
        self.background_texture = \
            np.asarray(Image.open(f"{self.theme}/background_texture.png").convert('RGBA'),
                       dtype=np.uint8)
        self.wall_texture = \
            np.asarray(Image.open(f"{self.theme}/wall_texture.png").convert('RGBA'),
                       dtype=np.uint8)
        self.path_texture = \
            np.asarray(Image.open(f"{self.theme}/path_texture.png").convert('RGBA'),
                       dtype=np.uint8)
        self.wall_path = self.wall_texture + self.path_texture
        self.floor = \
            self.create_mlx_image((self.maze_width * 2 + 1) * self.tile_size,
                                  (self.maze_height * 2 + 1) * self.tile_size)
        self.background = \
            self.create_mlx_image(self.win_width, self.win_height)

    def put_to_screen(self, img_id: any, pos_x: int, pos_y: int) -> None:
        self.mlx_put_image_to_window(self.mlx, self.win, img_id, pos_x, pos_y)

    def generate_floor(self) -> None:
        floor = np.zeros((self.base_height, self.base_width, 4),
                         dtype=np.uint8)
        for w in range(0, self.base_width, self.tile_size):
            for h in range(0, self.base_height, self.tile_size):
                floor[h:h+self.tile_size, w:w+self.tile_size] = self.wall_path
        self.image_to_memory(floor, self.floor)
        self.put_to_screen(self.floor.id, self.position_x, self.position_y - self.view_port)


def render():
    config = read_config("config.txt")
    m = MazeFront(config, 32)
    m.mlx_hook(m.win, 33, 0, MazeInterface.close_window, m)
    m.generate_floor()
    m.mlx_loop(m.mlx)


if __name__ == '__main__':
    render()
