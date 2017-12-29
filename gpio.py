from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
import time


def create_device():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    return device


def draw_point(device):
    for y in range(8):
         for x in range(8):
             with canvas(device) as draw:
                 draw.point((x,y), fill="green")
             time.sleep(0.5)


if __name__ == '__main__':
    display = create_device()
    draw_point(display)
    