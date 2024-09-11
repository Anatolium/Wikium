from PIL import Image, ImageGrab
import os
import time
import win32api, win32con
import math, operator
from functools import reduce

# Нужно проверить координаты для уровней 15-20 (num = 14…19)


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    rows, cols, start_x, start_y, fin_x, fin_y = 0, 0, 0, 0, 0, 0
    step_x = 62
    # step_x = 60
    step_y = 52
    width1, height1 = 52, 50

    if num < 2:
        rows, cols = 4, 5
        # start_x = 637
        start_x = 631
        start_y = 454
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 4:
        rows, cols = 5, 5
        # start_x = 637
        start_x = 631
        start_y = 429
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 6:
        rows, cols = 5, 6
        # start_x = 608
        start_x = 601
        start_y = 429
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 8:
        rows, cols = 6, 6
        # start_x = 608
        start_x = 601
        start_y = 404
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 10:
        rows, cols = 6, 7
        # start_x = 576
        start_x = 569
        start_y = 404
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 12:
        rows, cols = 7, 7
        # start_x = 576
        start_x = 569
        start_y = 377
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 14:
        rows, cols = 8, 7
        width1, height1 = 45, 45
        start_x = 593
        start_y = 372
        step_x = 56
        step_y = 47
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 16:
        rows, cols = 7, 9
        width1, height1 = 45, 45
        start_x = 515
        start_y = 334
        step_x = 61
        step_y = 52
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 18:
        rows, cols = 7, 10
        width1, height1 = 45, 45
        start_x = 484
        start_y = 335
        step_x = 61
        step_y = 52
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1
    elif num < 20:
        rows, cols = 7, 11
        width1, height1 = 45, 45
        start_x = 479
        start_y = 349
        step_x = 56
        step_y = 47
        fin_x = start_x + (cols - 1) * step_x + width1
        fin_y = start_y + (rows - 1) * step_y + height1

    images = []
    twins = []
    coord = []

    box = (start_x, start_y, fin_x, fin_y)
    im = ImageGrab.grab(box)
    #images.append(im)

    for yy in range(rows):
        for xx in range(cols):
            x1 = xx * step_x
            y1 = yy * step_y
            box = (x1, y1, x1 + width1, y1 + height1)
            im_crop = im.crop(box)
            twins.append(im_crop)
            coord.append((start_x + x1, start_y + y1))

            # if num == 8:
            #     im_name = os.getcwd() + '\\tw_' + str(yy).zfill(2) + str(xx).zfill(2) + '.png'
            #     im_crop.save(im_name, 'PNG')

            # if num == 7:
            #     if yy == 0:
            #         if xx == 3:
            #             im_name = os.getcwd() + '\\tw_' + str(yy) + str(xx) + '.png'
            #             im_crop.save(im_name, 'PNG')
            #             h1 = im.histogram()
            #     elif yy == 3:
            #         if xx == 1:
            #             im_name = os.getcwd() + '\\tw_' + str(yy) + str(xx) + '.png'
            #             im_crop.save(im_name, 'PNG')
            #             h2 = im.histogram()
            #             rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
            #             with open('w_twins.log', 'a') as log:
            #                 log.write(f'rms = {rms}\n')

    guess = compare(twins, num)
    if guess >= 0:
        coord_click = coord[guess]
        mousePos((coord_click[0] + 20, coord_click[1] + 20))
        leftClick()
    else:
        with open('w_twins.log', 'a') as log:
            #im_name = os.getcwd() + '\\twins_' + str(num+1) + '.png'
            #images[num].save(im_name, 'PNG')
            log.write(f'Level {num+1} - Twins not found\n')


def compare(twins: list, nnn):
    size = len(twins)
    for i in range(size):
        h1 = twins[i].histogram()
        for j in range(size):
            if i >= j:
                continue
            h2 = twins[j].histogram()
            rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))

            if rms < 0.8:
                if nnn > 11:
                    with open('w_twins.log', 'a') as log:
                        log.write(f'Level {nnn+1} --- {str(i).zfill(2)} + {str(j).zfill(2)} --- rms = {rms} \n')
                return i
    return -1


def start_game():
    for n in range(10):
        screen_grab(n)
        mousePos((1050, 300))
        time.sleep(2.4)


def main():
    start_game()


if __name__ == '__main__':
    main()
