from PIL import Image, ImageGrab
import os
import time
import win32api, win32con
import math, operator
from functools import reduce

# full screen 206x252
# ------------------------------
#     100%
# ------------------------------

#X1, Y1, X2, Y2 = 693, 417, 899, 669
#X1, Y1, X2, Y2 = 688, 477, 894, 729
X1, Y1, X2, Y2 = 688, 417, 894, 669
WIDTH, HEIGHT = 42, 54
win_x = [0, 54, 110, 164]
win_y = [0, 66, 134, 199]
#answer = [(645, 725), (685, 725), (725, 725), (765, 725), (800, 725), (840, 725), (880, 725), (920, 725)]
#answer = [(640, 785), (678, 785), (718, 785), (758, 785), (796, 785), (836, 785), (876, 785), (916, 785)]
answer = [(640, 725), (678, 725), (718, 725), (758, 725), (796, 725), (836, 725), (876, 725), (916, 725)]

windows_1, windows_2 = [], []
h_empty = []


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def read_image():
    global h_empty
    file_name = os.path.join('observer', 'empty_window.jpg')
    empty = Image.open(file_name)
    h_empty = empty.histogram()
    #print(f'h_empty = {h_empty}')


def screen_grab(num):
    global windows_1, windows_2
    box = (X1, Y1, X2, Y2)
    im = ImageGrab.grab(box)
    for y in range(4):
        for x in range(4):
            xx = win_x[x]
            yy = win_y[y]
            box = (xx, yy, xx + WIDTH, yy + HEIGHT)
            im_crop = im.crop(box)
            windows_2.append(im_crop)
            if num == 0:
                im_name = os.getcwd() + '\\nabl_' + str(y+1) + str(x+1) + '.png'
                im_crop.save(im_name, 'PNG')

    if num == 0:
        windows_1 = windows_2.copy()
        windows_2.clear()
        return

    guess = compare_windows(num)

    windows_1 = windows_2.copy()
    windows_2.clear()

    try:
        mouse_pos((answer[guess - 1][0], answer[guess - 1][1]))
        left_click()
    except:
        print(f'guess = {guess}')


def compare_windows(num):
    n_diff = 0
    if num == 1:
        with open('w_observer.log', 'a') as log:
            log.write('\n----------------------------------------\n')
    for i in range(len(windows_1)):
        h1 = windows_1[i].histogram()
        h2 = windows_2[i].histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
        with open('w_observer.log', 'a') as log:
            if rms > 3.0:
                file_name = os.getcwd() + '\\nabl_.jpg'
                windows_2[i].save(file_name, 'JPEG')
                im = Image.open(file_name)
                h2 = im.histogram()
                rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h2, h_empty)) / len(h2))
                if rms > 13.0:
                    n_diff += 1
                    log.write(f'--- num={num+1} i={i+1} rms_empty={rms}\n')
                    if rms > 100.0:
                        exit(0)
    return n_diff


def start_game():
    read_image()
    for n in range(95):
        screen_grab(n)
        time.sleep(1.2)



if __name__ == '__main__':
    start_game()
