# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/23 18:17:16 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import List
from PIL import Image
from time import sleep


def generator():  # Temporary output simalution of the algorithm
    with open('output_maze.txt', 'r') as output:
        data = [hex for hex in output.read().split('\n')[:-5]]
    for row in data:
        for col in row:
            yield col


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
        # self.background = image_constitution(f"themes/{theme}/background.png", self)
        self.wall = image_constitution(f"themes/{theme}/wall.png", self)
        self.logo = image_constitution(f"themes/{theme}/logo.png", self)
        self.grid = []

    def generate_maze(self):
        start_pos = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                     int(self.logo.height + 128 + 100))
        pos = [start_pos[0], start_pos[1]]
        patchwork = Image.open(f"themes/{self.theme}/path.png")
        path = Image.new('RGB', ((self.maze_width * 2 + 1) * self.tilesize,
                                 (self.maze_height * 2 + 1) * self.tilesize))
        path_width, path_height = path.size()
        for w in path_width:
            for h in path_height:
                path.paste(patchwork, (w, h))
        path.save(f"themes/{m.theme}/path.png")
        path = image_constitution(f"themes/{m.theme}/path.png", self)
        self.mlx_put_image_to_window()
        for gen in generator():
            binary = bin(int(gen, 16))[2:].zfill(4)
            self.grid.append([pos[0], pos[1], binary])
            if int(binary[-1])
            
            
            
        # for data in self.binary:
        #     follow += 1
        #     self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0], pos[1])
        #     if int(data[-1]) == 1:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0], pos[1] - 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] - 32, pos[1] - 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] + 32, pos[1] - 32)
        #     else:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0], pos[1] - 32)
        #     if int(data[-2]) == 1:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] + 32, pos[1])
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] + 32, pos[1] - 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] + 32, pos[1] + 32)
        #     else:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0] + 32, pos[1])
        #     if int(data[-3]) == 1:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0], pos[1] + 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] - 32, pos[1] + 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] + 32, pos[1] + 32)
        #     else:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0], pos[1] + 32)
        #     if int(data[-4]) == 1:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] - 32, pos[1])
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] - 32, pos[1] - 32)
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0] - 32, pos[1] + 32)
        #     else:
        #         self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0] - 32, pos[1])
        #     if follow == maze[0]:
        #         pos[0] = int(start_pos[0])
        #         pos[1] += 64
        #         follow = 0
        #     else:
        #         pos[0] += 64
        #     self.mlx_sync(self.mlx_ptr, self.SYNC_WIN_COMPLETED, self.win_ptr)


# def collage_generator(m: Mlx):
#     path_img = Image.open(f"themes/{theme}/path.png")
#     wall_img = Image.open(f"themes/{theme}/wall.png")
#     patchwork = Image.new


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
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, new_background.id, 0, 0)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.logo.id, int((m.width / 2) - (m.logo.width / 2)), 100)


def change_theme(keynum, m: MazeVisualizer):
    theme = ['pokemon', 'fallout', 'minecraft']
    if keynum == 116:
        try:
            m.theme = theme[theme.index(m.theme) + 1]
        except IndexError:
            m.theme = theme[0]
        m.mlx_clear_window(m.mlx_ptr, m.win_ptr)
        m.wall = image_constitution(f"themes/{m.theme}/wall.png", m)
        m.logo = image_constitution(f"themes/{m.theme}/logo.png", m)
        m.path = image_constitution(f"themes/{m.theme}/path.png", m)
        base_assets(m)
        m.generate_maze()


def maze_visualizer() -> None:
    width = 3840
    height = 2160
    theme = 'minecraft'
    m = MazeVisualizer(width, height, theme)
    m.mlx_key_hook(m.win_ptr, change_theme, m)
    base_assets(m)
    m.generate_maze()
    m.mlx_sync(m.mlx_ptr, m.SYNC_WIN_COMPLETED, m.win_ptr)
    m.mlx_hook(m.win_ptr, 33, 0, close, m)
    m.mlx_loop(m.mlx_ptr)


if __name__ == '__main__':
    maze_visualizer()
