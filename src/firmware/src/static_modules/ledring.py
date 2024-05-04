import time
import board
from rainbowio import colorwheel
import neopixel

import random

import math
import time

from static_modules.singleton import singleton
from static_modules import config
from static_modules import helper
@singleton
class ledring:

    COLOR_PRESET_HSV_H__BLUE: float = 0.66
    COLOR_PRESET_HSV_H__PINK: float = 0.88
    COLOR_PRESET_HSV_H__GREEN: float = 0.36
    COLOR_PRESET_HSV_H__BLACK: float = -1.0

    def hsv_to_rgb(self, hsv_color):
        # https://github.com/Warringer/micropython-rgbled/blob/master/rgbled.py
        (h, s, v) = hsv_color

        if h < 0.0:
            return 0, 0, 0
        i = math.floor(h*6)
        f = h*6 - i
        p = v * (1-s)
        q = v * (1-f*s)
        t = v * (1-(1-f)*s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i%6)]
        r = int(255 * r)
        g = int(255 * g)
        b = int(255 * b)
        return r, g, b

    def rgb_to_hsv(self, rgb_color):
        (r, g, b) = rgb_color
        r = float(1 / 255 * r)
        g = float(1 / 255 * g)
        b = float(1 / 255 * b)
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high

        d = high - low
        s = 0 if high == 0 else d/high

        if high == low:
            h = 0.0
        else:
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

    neopixelring: neopixel.NeoPixel = None
   
    def __init__(self):
        self.neopixelring = neopixel.NeoPixel(config.CFG_NEOPIXEL_PIN, config.CFG_NEOPIXEL_LED_COUNT, brightness=config.CFG_NEOPIXEL_MAX_BRIGHTNESS, auto_write=False)

    def clear(self):
        self.neopixelring.fill((0, 0, 0))


    def set_neopixel_full_hue_value(self, _hue: float = 0.0, _value: float = 1.0, _saturation: float = 1.0):
        hsv_color = [_hue, _saturation, min(_value, config.CFG_NEOPIXEL_MAX_BRIGHTNESS)]

        rgb_color = self.hsv_to_rgb(hsv_color)

        self.neopixelring.fill((rgb_color[0], rgb_color[1], rgb_color[2]))
        
        self.neopixelring.show()


