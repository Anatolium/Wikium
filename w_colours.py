from PIL import Image, ImageGrab
# from pillow import Image, ImageGrab
import os
import time
import win32api
import win32con
import math
import operator
from functools import reduce

############################
#   100%
############################

ERROR_DELTA = 8.0

# X1, X2 = 567, 840     # турнир
# Y1 = 550              # турнир
X1, X2 = 563, 836
# X1, X2 = 538, 811
# Y1 = 560
Y1 = 551
WIDTH, HEIGHT = 165, 50
#X_NO = 730
#X_YES = 795
X_NO, X_YES = 750, 820
Y_YES, Y_NO = 705, 705
# Y_NO = 660
# Y_YES = Y_NO


samples_left = []
samples_right = []
hb = []


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def read_images():
    global hb
    for i in range(4):
        for j in range(4):
            file = os.path.join('colours', 'left-' + str(i+1) + str(j+1) + '.jpg')
            im = Image.open(file)
            samples_left.append(im)

    for i in range(4):
        for j in range(4):
            file = os.path.join('colours', 'right-' + str(i+1) + str(j+1) + '.jpg')
            im = Image.open(file)
            samples_right.append(im)

    file = os.path.join('colours', 'blank.jpg')
    blank = Image.open(file)
    hb = blank.histogram()


def screen_grab(num):
    box = (X1, Y1, X1+WIDTH, Y1+HEIGHT)
    im1 = ImageGrab.grab(box)
    im_name1 = os.getcwd() + '\\colour_left-{}.jpg'.format(str(num+1).zfill(3))
    im1.save(im_name1, 'JPEG')
    im1 = Image.open(im_name1)

    if is_blank(im1, num):
        return 0

    box = (X2, Y1, X2+WIDTH, Y1+HEIGHT)
    im2 = ImageGrab.grab(box)
    im_name2 = os.getcwd() + '\\colour_right-{}.jpg'.format(str(num+1).zfill(3))
    im2.save(im_name2, 'JPEG')
    im2 = Image.open(im_name2)

    # mousePos((X_YES, Y_YES))
    # leftClick()

    guess = compare(im1, im2, num)
    if guess == 1:
        mousePos((X_YES, Y_YES))
        leftClick()
    elif guess == 2:
        mousePos((X_NO, Y_NO))
        leftClick()
    else:
        with open('w_colours.log', 'a') as log:
            log.write(f'Level {num+1} - Colour not found\n\n')

    if guess > 0:
        os.remove(im_name1)
        os.remove(im_name2)

    return 1


def is_blank(im, num):
    h1 = im.histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, hb)) / len(h1))
    if rms < 1.0:
        with open('w_colours.log', 'a') as log:
            log.write(f'------------------------------- Level {num+1}\n')
            log.write(f'--- rms 1 = {round(rms, 4)} --- blank image\n')
        return True
    return False


def compare(im1, im2, num):
    size = 16
    found_1 = 0
    h1 = im1.histogram()
    for i in range(size):
        if i == 0:
            with open('w_colours.log', 'a') as log:
                log.write(f'------------------------------- Level {num+1}\n')
        hs = samples_left[i].histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, hs)) / len(h1))
        #if rms < 1.0:
        if rms < ERROR_DELTA or round(rms, 3) == 11.255:
            found_1 = i + 1
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 1 = {round(rms, 4)}  found 1 = {i+1}\n')
            break
        else:
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 1 = {round(rms, 4)}\n')

    found_2 = 0
    h2 = im2.histogram()
    for i in range(size):
        hs = samples_right[i].histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h2, hs)) / len(h2))
        #if rms < 1.0:
        if rms < ERROR_DELTA:
            found_2 = i + 1
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 2 = {round(rms, 4)}  found 2 = {i+1}\n')
            break
        else:
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 2 = {round(rms, 4)}\n')

    if found_1 * found_2 > 0:
        if found_1 == 1 or found_1 == 5 or found_1 == 9 or found_1 == 13:
            if found_2 == 1 or found_2 == 2 or found_2 == 3 or found_2 == 4:
                return 1
            else:
                return 2

        if found_1 == 2 or found_1 == 6 or found_1 == 10 or found_1 == 14:
            if found_2 == 5 or found_2 == 6 or found_2 == 7 or found_2 == 8:
                return 1
            else:
                return 2

        if found_1 == 3 or found_1 == 7 or found_1 == 11 or found_1 == 15:
            if found_2 == 9 or found_2 == 10 or found_2 == 11 or found_2 == 12:
                return 1
            else:
                return 2

        if found_1 == 4 or found_1 == 8 or found_1 == 12 or found_1 == 16:
            if found_2 == 13 or found_2 == 14 or found_2 == 15 or found_2 == 16:
                return 1
            else:
                return 2

    return 0


############################
#   100%
############################

def start_game():
    n_blank = 0
    read_images()
    # 70 … 140
    for n in range(130):
        if screen_grab(n) == 0:
            n_blank += 1
        # mousePos((1600, 180))
        time.sleep(0.35)


if __name__ == '__main__':
    start_game()
