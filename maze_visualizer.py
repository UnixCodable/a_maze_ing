# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 03:32:25 by lbordana        #+#    #+#               #
#  Updated: 2026/03/25 02:49:30 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from PIL import Image, ImageDraw, ImageText, ImageFont
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
    
    @staticmethod
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

    # def generate_menu

    def generate_floor(self):
        start_pos = (int((self.width / 2) - ((self.maze_width / 2) * self.tilesize * 2)),
                     int(500))
        path_patch = Image.open(f"themes/{self.theme}/path_patch.png").convert('RGBA')
        wall_patch = Image.open(f"themes/{self.theme}/wall_patch.png").convert('RGBA')
        path_wall_patch = Image.alpha_composite(path_patch, wall_patch)
        path = Image.new('RGB',
                         ((self.maze_width * 2 + 1) * self.tilesize,
                          (self.maze_height * 2 + 1) * self.tilesize))
        path_width, path_height = path.size
        for w in range(0, path_width, self.tilesize):
            for h in range(0, path_height, self.tilesize):
                path.paste(path_wall_patch, (w, h))
        path.save(f"themes/{self.theme}/path.png")
        new_path = ImgData.image_constitution(f"themes/{self.theme}/path.png", self)
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
                for letter in '0123456789ABCDEF':
                    try:
                        self.grid.pop(self.grid.index([d[0], d[1], letter]))
                    except Exception:
                        continue
                self.grid.append([d[0], d[1], d[2]])
                self.grid = sorted(self.grid, key=lambda item: int(f'{item[0]}{item[1]}'))
            pos = [start_pos[0] + d[0] * (self.tilesize * 2),
                   start_pos[1] + d[1] * (self.tilesize * 2)]
            wall_tile = Image.open(f"themes/{self.theme}/wall_patch.png")
            path_tile = Image.open(f"themes/{self.theme}/path_patch.png")
            wall_mask = Image.new('RGBA', (self.tilesize * 3,
                                           self.tilesize * 3), (255, 0, 0, 0))
            wall_mask.paste(wall_tile, (self.tilesize, 0))
            wall_mask.paste(wall_tile, (self.tilesize * 2, self.tilesize))
            wall_mask.paste(wall_tile, (self.tilesize, self.tilesize * 2))
            wall_mask.paste(wall_tile, (0, self.tilesize))
            wall_mask.paste(path_tile, (self.tilesize, self.tilesize))
            if int(binary[-1]) == 0:
                wall_mask.paste(path_tile, (self.tilesize, 0))
            if int(binary[-2]) == 0:
                wall_mask.paste(path_tile, (self.tilesize * 2, self.tilesize))
            if int(binary[-3]) == 0:
                wall_mask.paste(path_tile, (self.tilesize, self.tilesize * 2))
            if int(binary[-4]) == 0:
                wall_mask.paste(path_tile, (0, self.tilesize))
            wall_mask.save(f"themes/{self.theme}/wall.png")
            walls = ImgData.image_constitution(f"themes/{self.theme}/wall.png", self)
            self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, walls.id, pos[0], pos[1])
            self.mlx_destroy_image(self.mlx_ptr, walls.id)
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
        self.speed = 0.1
        self.running_state = True

    @staticmethod
    def close(m: Mlx):
        m.mlx_loop_exit(m.mlx_ptr)

    @staticmethod
    def erase_text(m):
        patchwork = Image.open(f"themes/{m.theme}/background_patch.png")
        p_width, p_height = patchwork.size
        background = Image.new('RGB', (900, 400))
        for w in range(0, 900, p_width):
            for h in range(0, 400, p_height):
                background.paste(patchwork, (w, h))
        background.save(f"themes/{m.theme}/eraser.png")
        new_eraser = ImgData.image_constitution(f"themes/{m.theme}/eraser.png", m)
        m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, new_eraser.id, 0, 0)
        m.mlx_destroy_image(m.mlx_ptr, new_eraser.id)

    @staticmethod
    def console_text(string: str, font_size: int, self: Mlx):
        image = Image.new('RGBA', (700, 300), (0, 0, 0, 200))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f'themes/{self.theme}/font.ttf', font_size)
        draw.text((150, 120), string, font=font)
        image.save(f"themes/{self.theme}/text.png")

    @staticmethod
    def commands(keynum, self: MazeVisualizer):
        print(f"You've pressed key number : {keynum}")
        if keynum == 32 and self.running_state is True:
            self.erase_text(self)
            self.console_text('PAUSE', 60, self)
            text = ImgData.image_constitution(f"themes/{self.theme}/text.png", self)
            self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, text.id, 100, 100)
            self.mlx_destroy_image(self.mlx_ptr, text.id)
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
                self.console_text('SPEED ++', 60, self)
                text = ImgData.image_constitution(f"themes/{self.theme}/text.png", self)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, text.id, 100, 100)
                self.mlx_destroy_image(self.mlx_ptr, text.id)
        if keynum == 65364:
            if self.speed < 0.04:
                self.speed *= 3
                self.erase_text(self)
                self.console_text('SPEED --', 60, self)
                text = ImgData.image_constitution(f"themes/{self.theme}/text.png", self)
                self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, text.id, 100, 100)
                self.mlx_destroy_image(self.mlx_ptr, text.id)
        if keynum == 116:
            theme = ['classic',
                     'classic_red',
                     'pokemon',
                     'fallout',
                     'minecraft']
            try:
                self.theme = theme[theme.index(self.theme) + 1]
            except IndexError:
                self.theme = theme[0]
            base_assets(self)
            self.generate_floor()
            self.wall_builder = self.generate_walls()

    @staticmethod
    def dig(self):
        if self.running_state is False:
            return
        try:
            for _ in range(5):
                sleep(self.speed)
                next(self.wall_builder)
        except StopIteration:
            pass


def base_assets(m: MazeVisualizer):
    patchwork = Image.open(f"themes/{m.theme}/background_patch.png")
    p_width, p_height = patchwork.size
    background = Image.new('RGB', (m.width, m.height))
    for w in range(0, m.width, p_width):
        for h in range(0, m.height, p_height):
            background.paste(patchwork, (w, h))
    background.save(f"themes/{m.theme}/background.png")
    console = Image.new('RGBA', (700, 300), (0, 0, 0, 200))
    console.save(f"themes/{m.theme}/console.png")
    new_background = ImgData.image_constitution(f"themes/{m.theme}/background.png", m)
    logo = ImgData.image_constitution(f"themes/{m.theme}/logo.png", m)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, new_background.id, 0, 0)
    m.mlx_put_image_to_window(m.mlx_ptr, m.win_ptr, logo.id, int((m.width / 2) - (logo.width / 2)), 100)
    m.mlx_destroy_image(m.mlx_ptr, new_background.id)
    m.mlx_destroy_image(m.mlx_ptr, logo.id)


def controler(m: Mlx):
    m.mlx_hook(m.win_ptr, 33, 0, m.close, m)
    m.mlx_key_hook(m.win_ptr, m.commands, m)
    if m.running_state is True:
        print(m.running_state)
        m.mlx_loop_hook(m.mlx_ptr, m.dig, m)


def maze_visualizer() -> None:
    width = 3840
    height = 2160
    theme = 'pokemon'
    m = Controler(width, height, theme, generation)
    base_assets(m)
    m.generate_floor()
    # m.generate_ways([[2, 3], [16, 18]])
    # m.generate_walls(generation)
    m.mlx_loop_hook(m.mlx_ptr, controler, m)
    m.mlx_loop(m.mlx_ptr)


if __name__ == '__main__':
    maze_visualizer()
