# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/23 04:56:54 by lbordana        ###   ########.fr        #
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
    def __init__(self, width: int, height: int, theme: str) -> None:
        super().__init__()
        self.binary = convert()
        self.theme = theme
        self.width = width
        self.height = height
        self.mlx_ptr = self.mlx_init()
        self.win_ptr = self.mlx_new_window(self.mlx_ptr, width, height, 
                                           "A_maze_ing : Game poetry")
        self.background = image_constitution(f"themes/{theme}/background.xpm", self)
        self.wall = image_constitution(f"themes/{theme}/wall.xpm", self)
        self.logo = image_constitution(f"themes/{theme}/logo.xpm", self)
        self.path = image_constitution(f"themes/{theme}/path.xpm", self)

    def generate_maze(self):
        maze = (25, 20)  # Tailles manuelles à changer apres parsing
        start_pos = ((self.width / 2) - ((25 / 2) * 32 * 2), self.logo.height + 128 + 100)
        pos = [int(start_pos[0]), int(start_pos[1])]
        follow = 0
        grid = []
        incr = 0
        for w in range(maze[0] * 2 + 1):
            grid.append([])
            for h in range(maze[1] * 2 + 1):
                grid[w].append('Path')
        for col_nbr, col in enumerate(grid):
            for row_nbr, row in enumerate(col):
                if col_nbr % 2 != 0 and row_nbr % 2 != 0:
                    if int(self.binary[incr][-1]) == 1:
                        grid[col_nbr-1][row_nbr-1] = 'Wall'
                        grid[col_nbr-1][row_nbr] = 'Wall'
                        grid[col_nbr-1][row_nbr+1] = 'Wall'
                    if int(self.binary[incr][-2]) == 1:
                        grid[col_nbr-1][row_nbr+1] = 'Wall'
                        grid[col_nbr][row_nbr+1] = 'Wall'
                        grid[col_nbr+1][row_nbr+1] = 'Wall'
                    if int(self.binary[incr][-3]) == 1:
                        grid[col_nbr+1][row_nbr-1] = 'Wall'
                        grid[col_nbr+1][row_nbr] = 'Wall'
                        grid[col_nbr+1][row_nbr+1] = 'Wall'
                    if int(self.binary[incr][-4]) == 1:
                        grid[col_nbr-1][row_nbr-1] = 'Wall'
                        grid[col_nbr][row_nbr-1] = 'Wall'
                        grid[col_nbr+1][row_nbr-1] = 'Wall'
                    incr += 1
        for col in grid:
            for row in col:
                if row == 'Wall':
                    self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.wall.id, pos[0], pos[1])
                else:
                    self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.path.id, pos[0], pos[1])
                pos[1] += 32
            pos[1] = int(start_pos[1])
            pos[0] += 32
            
            
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

class ConvertingTools():
    @staticmethod
    def hex_recover() -> str:
        with open('output_maze.txt', 'r') as output:
            hex_only = [hex for hex in output.read().split('\n')[:-5]]
        return ''.join(hex_only)

    @staticmethod
    def hex_to_bin(hexa: str) -> List:
        return [bin(int(h, 16))[2:].zfill(4) for h in hexa]


def convert() -> List:
    hexa = ConvertingTools().hex_recover()
    binary = ConvertingTools().hex_to_bin(hexa)
    return binary


def image_constitution(path, m) -> ImgData:
    img_convert = m.mlx_xpm_file_to_image(m.mlx_ptr, path)
    img_id, img_width, img_height = img_convert
    img_data, img_bpp, img_sl, img_iformat = m.mlx_get_data_addr(img_id)
    image = ImgData(img_id,
                    img_width,
                    img_height,
                    img_data,
                    img_bpp,
                    img_sl,
                    img_iformat)
    # print(img_id,
    #       img_width,
    #       img_height,
    #       img_data,
    #       img_bpp,
    #       img_sl,
    #       img_iformat)
    return image


def close(m):
    m.mlx_loop_exit(m.mlx_ptr)


def base_assets(m: MazeVisualizer):
    m.mlx_sync(m.mlx_ptr, m.SYNC_IMAGE_WRITABLE, m.background.id)
    for w in range(0, m.width, m.background.width):
        for h in range(0, m.height, m.background.height):
            m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.background.id, w, h)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, m.logo.id, int((m.width / 2) - (m.logo.width / 2)), 100)

def change_theme(keynum, m: MazeVisualizer):
    theme = ['pokemon', 'fallout']
    if keynum == 116:
        try:
            m.theme = theme[theme.index(m.theme) + 1]
        except IndexError:
            m.theme = theme[0]
        m.mlx_clear_window(m.mlx_ptr, m.win_ptr)
        m.background = image_constitution(f"themes/{m.theme}/background.xpm", m)
        m.wall = image_constitution(f"themes/{m.theme}/wall.xpm", m)
        m.logo = image_constitution(f"themes/{m.theme}/logo.xpm", m)
        m.path = image_constitution(f"themes/{m.theme}/path.xpm", m)
        base_assets(m)
        m.generate_maze()


def maze_visualizer() -> None:
    width = 3840
    height = 2160
    theme = 'pokemon'
    m = MazeVisualizer(width, height, theme)
    m.mlx_key_hook(m.win_ptr, change_theme, m)
    base_assets(m)
    m.generate_maze()
    m.mlx_sync(m.mlx_ptr, m.SYNC_WIN_COMPLETED, m.win_ptr)
    m.mlx_hook(m.win_ptr, 33, 0, close, m)
    m.mlx_loop(m.mlx_ptr)


if __name__ == '__main__':
    maze_visualizer()
