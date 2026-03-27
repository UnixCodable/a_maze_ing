import numpy as np
from PIL import Image
from mlx import Mlx
import time
import ctypes


class m(Mlx):
    def __init__(self):
        super().__init__()
        self.ptr = self.mlx_init()
        self.win = self.mlx_new_window(self.ptr, 1920, 1080, "test")
        self.image = new_image(self)


class ImgData():
    def __init__(self, id=None, width=None, height=None, data=None, bpp=None, sl=None, iformat=None):
        self.id = id
        self.width = width
        self.height = height
        self.data = data
        self.bpp = bpp
        self.sl = sl
        self.iformat = iformat


def close(m: Mlx):
    m.mlx_loop_exit(m.ptr)


def new_image(m: Mlx):
    img = ImgData()
    img.id = m.mlx_new_image(m.ptr, 1920, 1080)
    img.width, img.height = (1920, 1080)
    img.data, img.bpp, img.sl, img.iformat = m.mlx_get_data_addr(img.id)
    return img


def write_in(m: Mlx):
    start = time.time()
    # big_pic = Image.new('RGBA', (1920, 1080))
    pil_image = Image.open("themes/pokemon/background_patch.png").convert('RGBA')
    width, height = pil_image.size
    pil_array = np.array(pil_image)
    image = np.zeros((1080, 1920, 4), dtype=np.uint8)
    image[80:80+height, 40:40+width] = pil_array
    buffer = np.frombuffer(m.image.data, dtype=np.uint8).reshape(image.shape)
    buffer[:, :, 0] = image[:, :, 2]
    buffer[:, :, 1] = image[:, :, 1]
    buffer[:, :, 2] = image[:, :, 0]
    buffer[:, :, 3] = image[:, :, 3]
    # big_pic.paste(pil_image, (0, 0))
    # r, g, b, a = big_pic.split()
    # big_pic = Image.merge('RGBA', (b, g, r, a))
    # m.image.data[:] = big_pic.tobytes()

    m.mlx_put_image_to_window(m.ptr, m.win, m.image.id, 0, 0)
    m.mlx_sync(m.ptr, m.SYNC_WIN_COMPLETED, m.win)
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    m = m()

    m.mlx_hook(m.win, 33, 0, close, m)
    write_in(m)
    m.mlx_loop(m.ptr)

# Image.fromarray(image).show()