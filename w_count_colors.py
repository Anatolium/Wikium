from PIL import Image, ImageGrab
import os
import time
import win32api, win32con


START_X, START_Y, FIN_X, FIN_Y = 0, 0, 1130, 900
X_RED, X_EQUAL, X_BLUE = 555, 735, 910
#Y_ANSWER = 938
Y_ANSWER = 865

h_red, h_blue, h_red2, h_blue2 = [], [], [], []


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    global h_red, h_blue

    rows, cols = 0, 0
    width1, height1 = 10, 10
    n_red, n_blue = 0, 0

    if num < 10:
       xx = [385, 447, 510, 572, 635, 697, 760, 822, 885, 947, 1010, 1072]
    # xx = [361, 423, 486, 548, 611, 673, 736, 798, 861, 923, 986, 1048]
    elif num < 16:
       xx = [378, 428, 478, 528, 578, 628, 678, 728, 778, 828, 878, 928, 978, 1028, 1078]
        # xx = [354, 404, 454, 504, 554, 604, 654, 704, 754, 804, 854, 904, 954, 1004, 1054]
    else:
       xx = [375, 419, 463, 506, 550, 593, 638, 681, 725, 769, 813, 856, 900, 944, 988, 1031, 1075]
        # xx = [351, 395, 438, 482, 526, 570, 614, 658, 701, 745, 789, 832, 876, 920, 964, 1007, 1051]
    yy = []

    if num < 2:
        rows, cols = 2, 12
        # yy = [685, 749]
        yy = [615, 675]
        #yy = [555, 615]     # тренажёры
    elif num < 8:
        rows, cols = 3, 12
        # yy = [654, 717, 780]
        yy = [582, 642, 710]
        #yy = [522, 582, 650]     # тренажёры
    elif num < 10:
        rows, cols = 4, 12
        # yy = [624, 686, 749, 811]
        yy = [550, 610, 675, 737]
        #yy = [490, 550, 615, 677]     # тренажёры
    elif num < 14:
        rows, cols = 4, 15
        # xx = [378, 428, 478, 528, 578, 628, 678, 728, 778, 828, 878, 928, 978, 1028, 1078]
        # yy = [643, 693, 743, 793]
        yy = [570, 620, 670, 720]
    elif num < 16:
        rows, cols = 5, 15
        # xx = [378, 428, 478, 528, 578, 628, 678, 728, 778, 828, 878, 928, 978, 1028, 1078]
        # yy = [617, 667, 717, 767, 817]
        yy = [545, 595, 645, 695, 745]
    elif num < 22:
        rows, cols = 5, 17
        # xx = [375, 419, 463, 506, 550, 593, 638, 681, 725, 769, 813, 856, 900, 944, 986, 1031, 1075]
        # yy = [630, 673, 720, 761, 807]
        yy = [556, 600, 644, 688, 732]
    elif num < 50:
        rows, cols = 6, 17
        # xx = [375, 419, 463, 506, 550, 593, 638, 681, 725, 769, 813, 856, 900, 944, 988, 1031, 1075]
        # yy = [533, 576, 620, 665, 708, 750]
        yy = [534, 578, 622, 666, 710, 754]

    box = (START_X, START_Y, FIN_X, FIN_Y)
    im_full = ImageGrab.grab(box)

    with open('w_count_colors.log', 'a') as log:
        log.write('--------------------------------------------------\n')
        for row in range(rows):
            for col in range(cols):
                x1 = xx[col]
                y1 = yy[row]
                box = (x1 - width1/2, y1 - height1/2, x1 + width1/2, y1 + height1/2)
                im_crop = im_full.crop(box)
                # Если не заработает, вернуть вариант 1
                # Вариант 1
                # im_name = os.getcwd() + '\\count_' + str(row+1).zfill(2) + str(col+1).zfill(2) + '.png'
                # im_crop.save(im_name, 'PNG')
                # im1 = Image.open(im_name)
                # im_rgb = im1.convert('RGB')

                # Вариант 2
                im_rgb = im_crop.convert('RGB')
                r, g, b = im_rgb.getpixel((width1/2, height1/2))
                log.write(f'num={num+1} row={row+1} col={col+1} r={r} g={g} b={b}\n')
                # r=255 g=0 b=0 – red
                # r=96 g=209 b=248 – blue
                # r=22 g=46 b=57 – empty
                if r > 250:
                    n_red += 1
                elif r > 93:
                    n_blue += 1

    # if num >= 16:
    #     im_name = os.getcwd() + '\\level_' + str(num+1) + '.png'
    #     im_full.save(im_name, 'PNG')

    if n_red > n_blue:
        x_answer = X_RED
    elif n_red < n_blue:
        x_answer = X_BLUE
    else:
        x_answer = X_EQUAL

    mousePos((x_answer, Y_ANSWER))
    leftClick()

# ------------------------------
#     125%
# ------------------------------


def main():
    # 22 … 30
    for n in range(21):
        screen_grab(n)
        mousePos((1050, 300))
        # 9070
        time.sleep(1.2)
        # 8200
        #time.sleep(2.2)
        # 5115
        #time.sleep(3.5)


if __name__ == '__main__':
    main()
