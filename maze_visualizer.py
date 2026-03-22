# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/22 02:40:01 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import List
from time import sleep


class ImgData():
    def __init__(self, id, width, height, data, bpp, sl, iformat):
        self.id = id
        self.width = width
        self.height = height
        self.data = data
        self.bpp = bpp
        self.sl = sl
        self.iformat = iformat


class MazeVisualizer(Mlx):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.mlx_ptr = self.mlx_init()
        self.win_ptr = self.mlx_new_window(self.mlx_ptr, width, height, "a maze ing")
        self.background = None
        self.decor = None

    def generate_maze():
        pass

    @staticmethod
    def clic(self):
        self.mlx_loop_exit(self.mlx_ptr)


class ConvertingTools():
    @staticmethod
    def hex_recover() -> str:
        with open('output_maze.txt', 'r') as output:
            hex_only = [hex for hex in output.read().split('\n')[:-5]]
        return ''.join(hex_only)
    
    @staticmethod
    def hex_to_bin(hexa: str) -> List:
        return [bin(int(h, 16))[2:].zfill(4) for h in hexa]


def convert() -> None:
    hexa = ConvertingTools().hex_recover()
    binary = ConvertingTools().hex_to_bin(hexa)


def image_constitution(path, m) -> ImgData:
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


def maze_visualizer() -> None:
    convert()
    width = 1900
    height = 1080
    m = MazeVisualizer(width, height)
    m.mlx_hook(m.win_ptr, 33, 0, m.clic, m)
    m.background = image_constitution("themes/pokemon/background.png", m)
    for w in range(0, width, 32):
        for h in range(0, height, 32):
            m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.background.id, w, h)
            sleep(0.00001)
    m.decor = image_constitution("themes/pokemon/decor.png", m)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.decor.id, 30, 30)
    m.mlx_loop(m.mlx_ptr)


if __name__ == '__main__':
    maze_visualizer()
