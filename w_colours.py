from PIL import Image, ImageGrab
import os
import time
import win32api, win32con
import math, operator
from functools import reduce

X1, X2 = 567, 840     # турнир
Y1 = 550              # турнир
# X1, X2 = 562, 835
# Y1 = 505
WIDTH, HEIGHT = 165, 50
X_NO = 750
X_YES = 820
Y_NO = 705            # турнир
# Y_NO = 660
Y_YES = Y_NO


samples_left = []
samples_right = []
hb = 0.0


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
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
    im_name = os.getcwd() + '\\colour_left.jpg'
    im1.save(im_name, 'JPEG')
    im1 = Image.open(im_name)

    if is_blank(im1, num):
        return 0

    box = (X2, Y1, X2+WIDTH, Y1+HEIGHT)
    im2 = ImageGrab.grab(box)
    im_name = os.getcwd() + '\\colour_right.jpg'
    im2.save(im_name, 'JPEG')
    im2 = Image.open(im_name)

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
        if rms < 1.0:
            found_1 = i + 1
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 1 = {round(rms, 4)}  found 1 = {i+1}\n')
            break
        # else:
        #     with open('w_colours.log', 'a') as log:
        #         log.write(f'--- rms 1 = {round(rms, 4)}\n')

    found_2 = 0
    h2 = im2.histogram()
    for i in range(size):
        hs = samples_right[i].histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h2, hs)) / len(h2))
        if rms < 1.0:
            found_2 = i + 1
            with open('w_colours.log', 'a') as log:
                log.write(f'--- rms 2 = {round(rms, 4)}  found 2 = {i+1}\n')
            break
        # else:
        #     with open('w_colours.log', 'a') as log:
        #         log.write(f'--- rms 2 = {round(rms, 4)}\n')

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


def start_game():
    n_blank = 0
    read_images()
    for n in range(99):
        if screen_grab(n) == 0:
            n_blank += 1
        mousePos((1050, 300))
        time.sleep(0.4)
    with open('w_colours.log', 'a') as log:
        log.write(f'--- {n_blank} blank images\n\n')


def main():
    start_game()


if __name__ == '__main__':
    main()
