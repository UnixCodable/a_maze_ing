# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer_clean.py                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 17:04:43 by lbordana        #+#    #+#               #
#  Updated: 2026/03/27 17:58:46 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from time import sleep, time
from data_test import generation
from config_parser import read_config


class ImgData():
    def __init__(self):
        self.id = None
        self.width = None
        self.height = None
        self.data = None
        self.bpp = None
        self.sl = None
        self.iformat = None


class MazeAssets(ImgData):
    def __init__(self, config: dict, tile_size: int,
                 theme: str = 'classic') -> None:
        #  Maze declarators
        self.maze_width = config.get('width')
        self.maze_height = config.get('height')
        self.theme = f"themes/{theme}"
        self.background_texture = \
            np.array(Image.open(f"{self.themes}/background_texture.png"))
        self.wall_


class MazeInterface(MazeAssets, Mlx):
    def __init__(self, config: dict, tile_size: int) -> None:
        #  Mlx declarators
        self.mlx = self.init()
        self.win_width = (self.maze_width * 2 + 1) * self.tile_size
        self.win_height = (self.maze_height * 2 + 1) * self.tile_size
        self.win = self.mlx_new_window(
                self.mlx,
                (self.maze_height * 2 + 1) * self.tile_size,
                (self.maze_width * 2 + 1) * self.tile_size
        )


if __name__ == '__main__':
    print(read_config("config.txt"))