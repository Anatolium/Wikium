from PIL import Image, ImageGrab, ImageChops
import os
import time
import win32api, win32con
import math, operator
from functools import reduce

# X1 = 515
# X2 = 804
# WIDTH = 260
# X1 = 506
# X2 = 796
# YY = 410
# WIDTH = 260
# HEIGHT = 310
X1 = 506
X2 = 796
YY = 350
WIDTH = 260
HEIGHT = 320
X_NO = 750
X_YES = 820
Y_NY = 700

# там, где появляется галочка или крестик
# XS, YS = 788, 555
# XS, YS = 783, 615
XS, YS = 783, 550


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    # time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    box = (X1, YY, X1 + WIDTH, YY + HEIGHT)
    im1 = ImageGrab.grab(box)
    h1 = im1.histogram()

    rms_s = 0
    for shift in range(15):
        box = (X2 + shift, YY, X2 + WIDTH + shift, YY + HEIGHT)
        im2 = ImageGrab.grab(box)
        h2 = im2.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
        if shift > 0 and rms >= rms_s:
            write_log(num, shift, rms, 0)
            break
        rms_s = rms
        # if rms > 133.0:
        #     exit(0)
        if rms < 5.0:
            write_log(num, shift, rms, 1)
            return True
        # elif shift == 0 or shift >= 8:
        else:
            write_log(num, shift, rms, 0)
    return False


def write_log(num, shift, rms, answer):
    with open('w_matches.log', 'a') as log:
        if num == 0:
            log.write(f'\n------------------------------\n')
        if answer == 1:
            log.write(f'Level {num + 1} - shift = {shift + 1}: rms= {rms}    Match\n')
        else:
            log.write(f'Level {num + 1} - shift = {shift + 1}: rms= {rms}    Not match\n')


def check_answer(num):
    box = (XS - 5, YS - 5, XS + 5, YS + 5)
    im = ImageGrab.grab(box)
    im_rgb = im.convert('RGB')
    r, g, b = im_rgb.getpixel((5, 5))
    if r != 27:
        with open('w_matches.log', 'a') as log:
            log.write(f'--- Level {num + 1}: {r} {g} {b}\n')
    # im_name = os.getcwd() + '\\match_' + str(num+1).zfill(2) + '.png'
    # im.save(im_name, 'PNG')

############################
#   100%
############################
def start_game():
    for n in range(101):    #95
        if screen_grab(n):
            mousePos((X_YES, Y_NY))
        else:
            mousePos((X_NO, Y_NY))
        leftClick()
        time.sleep(0.1)
        check_answer(n)
        time.sleep(0.22)


if __name__ == '__main__':
    start_game()
