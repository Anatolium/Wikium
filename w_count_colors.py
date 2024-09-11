from PIL import Image, ImageGrab
import os
import time
import win32api
import win32con
import math, operator
from functools import reduce

START_X, FIN_X = 0, 1130
X_RED, X_EQUAL, X_BLUE = 570, 745, 920
Y_ANSWER = 863

h_red, h_blue, h_red2, h_blue2 = [], [], [], []


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def read_images():
    global h_red, h_blue, h_red2, h_blue2

    file = os.path.join('count_colors', 'count_blue.jpg')
    im_blue = Image.open(file)
    h_blue = im_blue.histogram()

    file = os.path.join('count_colors', 'count_red.jpg')
    im_red = Image.open(file)
    h_red = im_red.histogram()

    file = os.path.join('count_colors', 'count_blue2.jpg')
    im_blue = Image.open(file)
    h_blue2 = im_blue.histogram()

    file = os.path.join('count_colors', 'count_red2.jpg')
    im_red = Image.open(file)
    h_red2 = im_red.histogram()


def screen_grab(num):
    global h_red, h_blue

    rows, cols = 0, 0
    start_y, fin_y = 0, 0
    width1, height1 = 12, 20
    n_red, n_blue = 0, 0

    xx = [45, 110, 173, 232, 299, 357, 423, 482, 554, 608, 670, 735]
    yy = []

    if num < 2:
        rows, cols = 2, 12
        start_y = 567
        fin_y = 717
        yy = [50, 110]
    elif num < 8:
        rows, cols = 3, 12
        start_y = 537
        fin_y = 747
        yy = [43, 105, 168]
    elif num < 10:
        rows, cols = 4, 12
        start_y = 507
        fin_y = 777
        yy = [41, 105, 167, 230]
    elif num < 16:
        # Координаты неверные - изменить, проверив скриншоты
        xx = [37, 87, 137, 187, 237, 287, 337, 387, 437, 487, 537, 587, 637, 687, 737]
        yy = [40, 90, 140, 190]
        rows, cols = 4, 15
        start_y = 530
        fin_y = 749
        width1, height1 = 10, 16

    box = (START_X, start_y, FIN_X, fin_y)
    im_full = ImageGrab.grab(box)

    with open('w_count_colors.log', 'a') as log:
        log.write('--------------------------------------------------\n')
        for row in range(rows):
            for col in range(cols):
                x1 = xx[col] - 7
                y1 = yy[row]
                box = (x1 - width1/2, y1 - height1/2, x1 + width1/2, y1 + height1/2)
                # im_crop = im_full.crop(box)
                im_name = os.getcwd() + '\\count_' + str(row+1).zfill(2) + str(col+1).zfill(2) + '.png'
                # im_crop.save(im_name, 'PNG')
                im1 = Image.open(im_name)
                h1 = im1.histogram()

                if num > 9:
                    h_blue = h_blue2
                    h_red = h_red2

                rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h_blue)) / len(h1))
                log.write(f'Crop {row*12+col+1} is blue? rms = {rms}\n')
                if rms < 14:
                    n_blue += 1
                rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h_red)) / len(h1))
                log.write(f'Crop {row*12+col+1} is red? rms = {rms}\n')
                if rms < 14:
                    n_red += 1

    if n_red > n_blue:
        x_answer = X_RED
    elif n_red < n_blue:
        x_answer = X_BLUE
    else:
        x_answer = X_EQUAL

    mousePos((x_answer, Y_ANSWER))
    leftClick()


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
    read_images()
    for n in range(10):
        screen_grab(n)
        mousePos((1050, 300))
        time.sleep(1.0)


def main():
    start_game()


if __name__ == '__main__':
    main()
