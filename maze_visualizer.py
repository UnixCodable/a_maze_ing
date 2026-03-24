# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/24 05:46:03 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import List
from PIL import Image
from time import sleep
from data_test import generation


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
    def __init__(self, width: int, height: int, theme: str) -> None:
        super().__init__()
        self.theme = theme
        self.tilesize = 32
        self.maze_width = 25
        self.maze_height = 20
        self.width = width
        self.height = height
        self.mlx_ptr = self.mlx_init()
        self.win_ptr = self.mlx_new_window(self.mlx_ptr, width, height, 
                                           "A_maze_ing : Game poetry")
        self.grid = []

    def generate_floor(self):
        start_pos = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                     int(500))
        patchwork = Image.open(f"themes/{self.theme}/path_patch.png")
        path = Image.new('RGBA',
                         ((self.maze_width * 2 + 1) * self.tilesize,
                          (self.maze_height * 2 + 1) * self.tilesize),
                         (255, 0, 0, 0))
        path_width, path_height = path.size
        for w in range(0, path_width, self.tilesize):
            for h in range(0, path_height, self.tilesize):
                path.paste(patchwork, (w, h))
        path.save(f"themes/{self.theme}/path.png")
        new_path = image_constitution(f"themes/{self.theme}/path.png", self)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, new_path.id, start_pos[0], start_pos[1])
        self.mlx_destroy_image(self.mlx_ptr, new_path.id)

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
                self.grid.append([d[0], d[1], d[2]])
            pos = [start_pos[0] + d[0] * (self.tilesize * 2),
                   start_pos[1] + d[1] * (self.tilesize * 2)]
            wall_tile = Image.open(f"themes/{self.theme}/wall_patch.png")
            path_tile = Image.open(f"themes/{self.theme}/path_patch.png")
            wall_mask = Image.new('RGBA', (self.tilesize * 3,
                                           self.tilesize * 3), (255, 0, 0, 0))
            wall_mask.paste(path_tile, (self.tilesize, 0))
            wall_mask.paste(path_tile, (self.tilesize * 2, self.tilesize))
            wall_mask.paste(path_tile, (self.tilesize, self.tilesize * 2))
            wall_mask.paste(path_tile, (0, self.tilesize))
            if int(binary[-1]) == 1:
                wall_mask.paste(wall_tile, (0, 0))
                wall_mask.paste(wall_tile, (self.tilesize, 0))
                wall_mask.paste(wall_tile, (self.tilesize * 2, 0))
            if int(binary[-2]) == 1:
                wall_mask.paste(wall_tile, (self.tilesize * 2, 0))
                wall_mask.paste(wall_tile, (self.tilesize * 2, self.tilesize))
                wall_mask.paste(wall_tile, (self.tilesize * 2, self.tilesize * 2))
            if int(binary[-3]) == 1:
                wall_mask.paste(wall_tile, (0, self.tilesize * 2))
                wall_mask.paste(wall_tile, (self.tilesize, self.tilesize * 2))
                wall_mask.paste(wall_tile, (self.tilesize * 2, self.tilesize * 2))
            if int(binary[-4]) == 1:
                wall_mask.paste(wall_tile, (0, 0))
                wall_mask.paste(wall_tile, (0, self.tilesize))
                wall_mask.paste(wall_tile, (0, self.tilesize * 2))
            wall_mask.save(f"themes/{self.theme}/wall.png")
            walls = image_constitution(f"themes/{self.theme}/wall.png", self)
            self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, walls.id, pos[0], pos[1])
            self.mlx_destroy_image(self.mlx_ptr, walls.id)

    def generate_ways(self, data=None):
        start = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                 int(500))
        entrance_way = [start[0] + d * (self.tilesize * 2) for d in data[0]]
        exit_way = [start[0] + d * (self.tilesize * 2) for d in data[1]]
        entrance = image_constitution(f"themes/{self.theme}/entrance.png", self)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, entrance.id, entrance_way[0], entrance_way[1])
        exiting = image_constitution(f"themes/{self.theme}/exit.png", self)
        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, exiting.id, exit_way[0], exit_way[1])


def image_constitution(path, m: Mlx) -> ImgData:
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


def close(m):
    m.mlx_loop_exit(m.mlx_ptr)


def base_assets(m: MazeVisualizer):
    patchwork = Image.open(f"themes/{m.theme}/background_patch.png")
    p_width, p_height = patchwork.size
    background = Image.new('RGB', (m.width, m.height))
    for w in range(0, m.width, p_width):
        for h in range(0, m.height, p_height):
            background.paste(patchwork, (w, h))
    background.save(f"themes/{m.theme}/background.png")
    new_background = image_constitution(f"themes/{m.theme}/background.png", m)
    logo = image_constitution(f"themes/{m.theme}/logo.png", m)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, new_background.id, 0, 0)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, logo.id, int((m.width / 2) - (logo.width / 2)), 100)
    m.mlx_destroy_image(m.mlx_ptr, new_background.id)
    m.mlx_destroy_image(m.mlx_ptr, logo.id)


def change_theme(keynum, m: MazeVisualizer):
    theme = ['classic', 'classic_red', 'pokemon', 'fallout', 'minecraft']
    if keynum == 116:
        try:
            m.theme = theme[theme.index(m.theme) + 1]
        except IndexError:
            m.theme = theme[0]
        base_assets(m)
        m.generate_floor()
        m.generate_walls()


def generator():  # Temporary output simalution of the algorithm
    with open('output_maze.txt', 'r') as output:
        data = [hex for hex in output.read().split('\n')[:-5]]
    for row in data:
        for col in row:
            yield col


def maze_visualizer() -> None:
    width = 3840
    height = 2160
    theme = 'classic'
    m = MazeVisualizer(width, height, theme)
    m.mlx_key_hook(m.win_ptr, change_theme, m)
    base_assets(m)
    # m.mlx_sync(m.mlx_ptr, m.SYNC_WIN_COMPLETED, m.win_ptr)
    m.generate_floor()
    # with open('output_maze.txt', 'r') as output:
    #     data = [hex for hex in output.read().split('\n')[:-5]]
    # for row_nbr, row in enumerate(data):
    #     for col_nbr, col in enumerate(row):
    #         m.generate_walls([[col_nbr, row_nbr, col]])
    m.generate_walls(generation)
    # m.generate_ways([[2, 3], [16, 18]])
    m.mlx_hook(m.win_ptr, 33, 0, close, m)
    m.mlx_loop(m.mlx_ptr)


if __name__ == '__main__':
    maze_visualizer()
