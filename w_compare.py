from PIL import Image, ImageGrab, ImageChops
import os
import time
import win32api, win32con
import math, operator
from functools import reduce


X1 = 515
X2 = 805
YY = 350
width = 260
height = 320
im_name_1 = ''
im_name_2 = ''


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print('Click')


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    global im_name_1, im_name_2

    box = (X1, YY, X1 + width, YY + height)
    im1 = ImageGrab.grab(box)
    h1 = im1.histogram()

    for shift in range(8):
        box = (X2 + shift, YY, X2 + width + shift, YY + height)
        im2 = ImageGrab.grab(box)
        h2 = im2.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
        if rms < 6.0:
            write_log(num, rms)
            return True
        elif shift == 0:
            write_log(num, rms)
    return False


def write_log(num, rms):
    with open('w_matches.log', 'a') as log:
        if num == 0:
            log.write(f'\n------------------------------\n')
        log.write(f'Level {num + 1}: rms= {rms}\n')


def start_game():
    for n in range(64):
        if screen_grab(n):
            mousePos((820, 700))
            #mousePos((820, 650))
        else:
            mousePos((750, 700))
            #mousePos((750, 650))
        leftClick()
        time.sleep(0.35)


def main():
    start_game()


if __name__ == '__main__':
    main()
