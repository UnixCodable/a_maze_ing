# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_visualizer.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: rshikder, lbordana                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 17:04:43 by lbordana        #+#    #+#               #
#  Updated: 2026/04/01 01:40:30 by lbordana        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as PillowImage
from typing import Any
import numpy as np
import cv2
# from time import sleep, time
from typing import Generator
from config_parser import read_config


class ImgData():
    """
    Gathering mlx images data adresses:
        - ID : Image identifier (C Pointer)
        - Width : Width declared during image creation
        - Height : Height declared during image creation
        - Data : Image data bytes, BGRA colors channel
        - BPP : Bits per pixel needed to represent a pixel colour
        - SL : Used to get / modified number of bytes used to store one line
        - Iformat : Define format used as color channel - BGRA / ARGB
    """
    def __init__(self) -> None:
        """Initialization of an image, all components adresses per item"""
        self.id = None
        self.width = None
        self.height = None
        self.data = None
        self.bpp = None
        self.sl = None
        self.iformat = None


class MazeInterface(Mlx):
    """Maze base components

    Args:
        Mlx : Mlx is a C wrapper of the MiniLibX project, an X-Window
              programming API.
    """
    def __init__(self, config: dict) -> None:
        """Initialization of mlx and maze basics data.

        Args:
            config (dict): Configuration of the maze (Dimensions)
        """
        super().__init__()
        self.mlx = self.mlx_init()
        self.maze_width: int = int(config.get('width', 0))
        self.maze_height: int = int(config.get('height', 0))
        self.maze_entry: tuple = tuple(config.get('entry', 0))
        self.maze_exit: tuple = tuple(config.get('exit', 0))
        self.tile_size = int(32 * self.scale_tile_size())
        self.base_width = (self.maze_width * 2 + 1) * self.tile_size
        self.base_height = (self.maze_height * 2 + 1) * self.tile_size
        self.win_width: int = self.get_window_size()[0]
        self.win_height: int = self.get_window_size()[1]
        self.win = self.mlx_new_window(
                self.mlx,
                self.win_width,
                self.win_height,
                "A_Maze_Ing : An old gaming story"
        )
        self.pos_x = int((self.win_width / 2) - self.base_width / 2)
        self.pos_y = 500
        self.running_state = True
        self.view_port_h = 0
        self.view_port_w = 0

    def put_to_screen(self, img_id: Any, pos_x: int, pos_y: int) -> None:
        """Method that use the mlx_put_image_to_window method

        Args:
            img_id (any): The identifier of the Image
            pos_x (int): The x position to place the image
            pos_y (int): The y position to place the image
        """
        self.mlx_put_image_to_window(self.mlx, self.win, img_id, pos_x, pos_y)

    def image_to_memory(self, array: np.uint8, image: ImgData) -> None:
        """Take a 3 dimensional array of a converted image and place those
        data in the data address of a ImgData object.

        Args:
            array (np.uint8): An image (from cv2 or PIL) converted as array
            image (ImgData): ImgData object, containing all image pointers
        """
        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, :] = array[:, :, :]

    def create_mlx_image(self, width: int, height: int) -> ImgData:
        """Create a new ImgData object and returns it.

        Args:
            width (int): The width of the image, to declare
            height (int): The height of the image, to declare

        Returns:
            ImgData: An ImgData object (mlx compatible image)
        """
        mlx_image = ImgData()
        mlx_image.id = self.mlx_new_image(self.mlx, width, height)
        mlx_image.width, mlx_image.height = (width, height)
        mlx_image.data, mlx_image.bpp, mlx_image.sl, mlx_image.iformat = \
            self.mlx_get_data_addr(mlx_image.id)
        return mlx_image

    def scale_tile_size(self) -> float:
        """Define the size of the tile, based on the size of the maze

        Returns:
            int: Returns the multiplier scale of a tile
        """
        scale: float = 1
        if self.maze_height < 12 or self.maze_width < 20:
            scale = 1.4
        if self.maze_height > 30 or self.maze_width > 50:
            scale = 0.7
        if self.maze_height > 60 or self.maze_width > 100:
            scale = 0.4
        if self.maze_height > 150 or self.maze_width > 200:
            scale = 0.2
        return scale

    def get_window_size(self):
        screen_size = self.mlx_get_screen_size(self.mlx)
        width = (self.maze_width * 2 + 1) * self.tile_size + 400
        height = (self.maze_height * 2 + 1) * self.tile_size + 700
        if width > screen_size[1]:
            width = screen_size[1]
        if height > screen_size[2]:
            height = screen_size[2]
        return (width, height)


class MazeFront(MazeInterface):
    def __init__(self, config: dict, theme: str = 'classic',
                 interface: bool = True) -> None:
        if interface is True:
            super().__init__(config)
        self.historic = []
        self.theme = f"themes/{theme}"
        self.background_texture = self.gen_array('background_texture.png')
        self.wall = self.gen_array('wall.png', True)
        self.path = self.gen_array('path.png', True)
        self.logo_texture = self.gen_array('logo.png')
        self.entrance_texture = self.gen_array('entrance.png', True)
        self.exit_texture = self.gen_array('exit.png', True)
        self.res_path = self.gen_array('resolution_path.png', True)
        self.tile = self.create_mlx_image(self.tile_size * 3,
                                          self.tile_size * 3)
        self.mask = None
        self.floor = self.create_mlx_image(self.base_width, self.base_height)
        self.background = self.create_mlx_image(self.win_width,
                                                self.win_height)
        self.snapshot = np.zeros((self.base_height, self.base_width, 4),
                                 dtype=np.uint8)
        self.res = np.zeros((self.base_height, self.base_width, 4),
                            dtype=np.uint8)
        self.logo = self.create_mlx_image(self.logo_texture.shape[1],
                                          self.logo_texture.shape[0])
        self.snap = self.create_mlx_image(self.base_width, self.base_height)
        self.snap_buf = (np.frombuffer(self.snap.data, dtype=np.uint8).
                         reshape(self.snapshot.shape))
        self.snap_buf.fill(0)
        self.last_bin = '1111'
        self.generator = None
        self.speed = 1

    def console_text(self, string: str, font_size: int) -> PillowImage:
        """Text to image method. Draw with PIL a text as a new image with 4
           colors channels (RGBA)

        Args:
            string (str): The string to write
            font_size (int): The size of the font

        Returns:
            ImgData: Newly created image of a text
        """
        image = Image.new('RGBA', (700, 300), (0, 0, 0, 200))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f'{self.theme}/font.ttf', font_size)
        draw.text((150, 120), string, font=font)
        return image

    def erase_text(self) -> None:
        p_height = self.background_texture.shape[0]
        p_width = self.background_texture.shape[1]
        logo_width = self.logo_texture.shape[1]
        background = np.zeros((400, 900, 4), dtype=np.uint8)
        for w in range(0, 900, p_width):
            for h in range(0, 400, p_height):
                h_size = 400 - h if h + p_height > 400 else p_height
                w_size = 900 - w if w + p_width > 900 else p_width
                background[h:h + h_size, w:w + w_size, 0:3] =\
                    self.background_texture[0:h_size, 0:w_size, 0:3]
                background[:, :, 3] = 255
        eraser = self.create_mlx_image(900, 400)
        self.image_to_memory(background, eraser)
        self.put_to_screen(eraser.id,
                           0 - self.view_port_h,
                           0 - self.view_port_h)
        self.put_to_screen(self.logo.id,
                           int((self.win_width / 2) -
                               (logo_width / 2)) - self.view_port_w,
                           100 - self.view_port_h)
        self.mlx_destroy_image(self.mlx, eraser.id)

    def mask_creator(self) -> None:
        tile = self.tile_size
        self.mask = np.zeros((tile * 3, tile * 3, 4), dtype=np.uint8)
        self.mask[0:tile, tile:tile*2] = self.wall
        self.mask[tile:tile*2, tile*2:tile*3] = self.wall
        self.mask[tile*2:tile*3, tile:tile*2] = self.wall
        self.mask[tile:tile*2, 0:tile] = self.wall
        self.mask[tile:tile*2, tile:tile*2] = self.path

    def generate_floor(self) -> None:
        floor = np.zeros((self.base_height, self.base_width, 4),
                         dtype=np.uint8)
        for w in range(0, self.base_width, self.tile_size):
            for h in range(0, self.base_height, self.tile_size):
                floor[h:h+self.tile_size, w:w+self.tile_size] = self.wall
        self.image_to_memory(floor, self.floor)
        self.put_to_screen(self.floor.id,
                           self.pos_x - self.view_port_w,
                           self.pos_y - self.view_port_h)

    def generate_walls(self, data: list = None) -> Generator:

        tile = self.tile_size

        if self.mask is None:
            self.mask_creator()
        for d in data:
            binary = bin(int(d[2], 16))[2:].zfill(4)
            p_snap = (d[0] * (tile * 2),
                      d[1] * (tile * 2))
            mask = self.mask.copy()
            if int(binary[-1]) == 0:
                mask[0:tile, tile:tile*2] = self.path
            if int(binary[-2]) == 0:
                mask[tile:tile*2, tile*2:tile*3] = self.path
            if int(binary[-3]) == 0:
                mask[tile*2:tile*3, tile:tile*2] = self.path
            if int(binary[-4]) == 0:
                mask[tile:tile*2, 0:tile] = self.path
            self.snap_buf[p_snap[1]:p_snap[1] + (tile * 3),
                          p_snap[0]:p_snap[0] + (tile * 3)] = mask
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
        self.mlx_sync(self.mlx, self.SYNC_IMAGE_WRITABLE, self.background.id)

    def generate_logo(self) -> None:
        width = self.logo_texture.shape[1]
        self.image_to_memory(self.logo_texture, self.logo)
        self.put_to_screen(self.logo.id,
                           int((self.win_width / 2) -
                               (width / 2)) - self.view_port_w,
                           100 - self.view_port_h)

    def generate_entrance_exit(self):
        tile = self.tile_size
        p_entry = ((self.maze_entry[0] * 2 + 1) * tile,
                   (self.maze_entry[1] * 2 + 1) * tile)
        p_exit = ((self.maze_exit[0] * 2 + 1) * tile,
                  (self.maze_exit[1] * 2 + 1) * tile)
        self.snap_buf[p_entry[1]:p_entry[1] + tile,
                      p_entry[0]:p_entry[0] + tile] = self.entrance_texture
        self.snap_buf[p_exit[1]:p_exit[1] + tile,
                      p_exit[0]:p_exit[0] + tile] = self.exit_texture

    def generate_resolution(self, resolution_path: str) -> None:
        tile = self.tile_size
        path = [(self.maze_entry[1] * 2 + 1) * tile,
                (self.maze_entry[0] * 2 + 1) * tile]
        for direction in resolution_path[:-1]:
            if direction == 'N':
                for _ in range(2):
                    path[0] -= tile
                    self.snap_buf[path[0]:path[0] + tile,
                                  path[1]:path[1] + tile] = self.res_path
            if direction == 'E':
                for _ in range(2):
                    path[1] += tile
                    self.snap_buf[path[0]:path[0] + tile,
                                  path[1]:path[1] + tile] = self.res_path
            if direction == 'S':
                for _ in range(2):
                    path[0] += tile
                    self.snap_buf[path[0]:path[0] + tile,
                                  path[1]:path[1] + tile] = self.res_path
            if direction == 'W':
                for _ in range(2):
                    path[1] -= tile
                    self.snap_buf[path[0]:path[0] + tile,
                                  path[1]:path[1] + tile] = self.res_path
        if resolution_path[-1] == 'N':
            path[0] -= tile
            self.snap_buf[path[0]:path[0] + tile,
                          path[1]:path[1] + tile] = self.res_path
        if resolution_path[-1] == 'E':
            path[1] += tile
            self.snap_buf[path[0]:path[0] + tile,
                          path[1]:path[1] + tile] = self.res_path
        if resolution_path[-1] == 'S':
            path[0] += tile
            self.snap_buf[path[0]:path[0] + tile,
                          path[1]:path[1] + tile] = self.res_path
        if resolution_path[-1] == 'W':
            path[1] -= tile
            self.snap_buf[path[0]:path[0] + tile,
                          path[1]:path[1] + tile] = self.res_path 

    def gen_array(self, filename: str, resizing: bool = False):
        image = cv2.imread(f"{self.theme}/{filename}",
                           flags=cv2.IMREAD_UNCHANGED)
        image_argb = cv2.cvtColor(image, code=cv2.COLOR_BGR2BGRA)
        if resizing is True:
            image_scale = cv2.resize(image_argb, (self.tile_size,
                                                  self.tile_size))
            return np.asarray(image_scale, dtype=np.uint8)
        return np.asarray(image_argb, dtype=np.uint8)


class Controler(MazeFront):
    def __init__(self, config: dict, theme: str = 'classic',
                 interface: bool = True) -> None:
        super().__init__(config, theme, interface)

    def close_window(self) -> None:
        self.mlx_loop_exit(self.mlx)

    def key_commands(self, key_num, *m):
        logo_width = self.logo_texture.shape[1]
        if key_num == 32 and self.running_state is True:
            self.erase_text()
            text = self.console_text('PAUSE', 60)
            console = self.create_mlx_image(700, 300)
            self.image_to_memory(np.asarray(text), console)
            self.put_to_screen(console.id,
                               100 - self.view_port_w,
                               100 - self.view_port_h)
            self.mlx_destroy_image(self.mlx, console.id)
            self.running_state = False
            return
        if key_num == 32 and self.running_state is False:
            self.erase_text()
            self.running_state = True
            return
        if key_num == 116:
            theme = ['classic',
                     'classic_red',
                     'pokemon',
                     'fallout',
                     'minecraft',
                     'mario']
            active = self.theme.split('/')[1]
            self.mlx_destroy_image(self.mlx, self.floor.id)
            self.mlx_destroy_image(self.mlx, self.logo.id)
            self.mlx_destroy_image(self.mlx, self.tile.id)
            self.mlx_destroy_image(self.mlx, self.snap.id)
            self.mlx_destroy_image(self.mlx, self.background.id)
            try:
                self.__init__(None, theme[theme.index(active) + 1], False)
            except IndexError:
                self.__init__(None, theme[0], False)
            self.mlx_clear_window(self.mlx, self.win)
            self.generator = self.generate_walls(parsed_data()[0])
            self.generate_background()
            self.generate_logo()
            self.generate_floor()
            self.mask_creator()
        if key_num == 61:
            if self.speed < 500:
                if self.speed < 5:
                    self.speed += 1
                elif self.speed < 20:
                    self.speed += 5
                elif self.speed < 100:
                    self.speed += 20
                elif self.speed < 500:
                    self.speed += 100
                self.erase_text()
                text = self.console_text(f'SPEED {self.speed}', 60)
                console = self.create_mlx_image(700, 300)
                self.image_to_memory(np.asarray(text), console)
                self.put_to_screen(console.id,
                                   100 - self.view_port_w,
                                   100 - self.view_port_h)
                self.mlx_destroy_image(self.mlx, console.id)
        if key_num == 45:
            if self.speed > 1:
                if self.speed <= 5:
                    self.speed -= 1
                elif self.speed <= 20:
                    self.speed -= 5
                elif self.speed <= 100:
                    self.speed -= 20
                elif self.speed <= 500:
                    self.speed -= 100
                self.erase_text()
                text = self.console_text(f'SPEED {self.speed}', 60)
                console = self.create_mlx_image(700, 300)
                self.image_to_memory(np.asarray(text), console)
                self.put_to_screen(console.id,
                                   100 - self.view_port_w,
                                   100 - self.view_port_h)
                self.mlx_destroy_image(self.mlx, console.id)
        if key_num == 65361 or key_num == 97:
            if self.view_port_w > self.base_width * -1:
                # for _ in range(20):
                self.view_port_w -= 200
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
        if key_num == 65363 or key_num == 100:
            if self.view_port_w < self.base_width:
                # for _ in range(20):
                self.view_port_w += 200
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
        if key_num == 65362 or key_num == 119:
            if self.view_port_h > 0:
                # for _ in range(20):
                self.view_port_h -= 200
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
        if key_num == 65364 or key_num == 115:
            if self.view_port_h < self.base_height:
                self.view_port_h += 200
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)

    def mouse_commands(self, mouse_num, x, y, *a):
        logo_width = self.logo_texture.shape[1]
        if mouse_num == 4:
            if self.view_port_h > 0:
                # for _ in range(20):
                self.view_port_h -= 60
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
        if mouse_num == 5:
            if self.view_port_h < self.base_height:
                self.view_port_h += 60
                self.put_to_screen(self.background.id, 0, 0)
                self.put_to_screen(
                    self.logo.id,
                    int((self.win_width / 2) - (logo_width / 2)),
                    100 - self.view_port_h
                )
                self.put_to_screen(self.floor.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)
                self.put_to_screen(self.snap.id,
                                   self.pos_x - self.view_port_w,
                                   self.pos_y - self.view_port_h)

    def generate(self, resolution_path):
        if self.running_state is False:
            return
        # start = time()
        try:
            # for _ in range():
            for _ in range(self.speed):
                next(self.generator)
                # sleep(0.5)
        except StopIteration:
            self.generate_entrance_exit()
            self.generate_resolution(resolution_path)
            self.running_state = False
        self.put_to_screen(self.snap.id,
                           self.pos_x - self.view_port_w,
                           self.pos_y - self.view_port_h)
        # end = time()
        # print(end - start)


def parsed_data():
    parsed = []
    with open("maze.txt", 'r') as file:
        data = file.readlines()
        nb = 0
        to_parse = []
        directions = []
        while data[nb] != '\n':
            to_parse.append(data[nb])
            nb += 1
        nb += 3
        for d in data[nb]:
            if d == '\n':
                break
            directions.append(d)
        for nb_d, d in enumerate(to_parse):
            for nb_char, char in enumerate(d[:-1]):
                parsed.append([nb_char, nb_d, d[nb_char]])
    return (parsed, directions)


def render():
    config = read_config("config.txt")
    m = Controler(config)
    m.generator = m.generate_walls(parsed_data()[0])
    m.mlx_hook(m.win, 33, 0, Controler.close_window, m)
    m.generate_background()
    m.generate_logo()
    m.generate_floor()
    m.mlx_key_hook(m.win, m.key_commands, m)
    m.mlx_mouse_hook(m.win, m.mouse_commands, m)
    m.mlx_loop_hook(m.mlx, m.generate, parsed_data()[1])
    m.mlx_loop(m.mlx)


if __name__ == '__main__':
    render()
