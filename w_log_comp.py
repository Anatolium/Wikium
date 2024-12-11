from PIL import Image, ImageGrab
import time
import win32api, win32con
import pytesseract

X1, X2 = 652, 862
#X1, X2 = 675, 885
YY = 297
X_LEFT = 760
X_EQUAL = 850
X_RIGHT = 950
Y_ANSWER = 475

WIDTH = 185     #150
HEIGHT = 40

###########
### 67%
###########

# X1, X2 = 590, 840
# YY = 370
# X_LEFT = 710
# X_EQUAL = 825
# X_RIGHT = 940
# # X_LEFT = 650
# # X_EQUAL = 785
# # X_RIGHT = 930
# Y_ANSWER = 590
#
# WIDTH = 220
# HEIGHT = 60


im_name_1 = ''
im_name_2 = ''

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    if num != 0:
        # nn = num + 1
        # if nn > 13:
        #     if (nn % 2) == 0:
        #         makeClick(2)
        #     else:
        #         makeClick(1)
            #makeClick(1)
            # if num == 36:
            #     makeClick(1)
            # elif num == 37:
            #     makeClick(1)
            # elif num == 38:
            #     makeClick(2)
            # elif num == 39:
            #     makeClick(2)
            #return
        pass
    else:
        with open('w_log_comp.log', 'a') as log:
            log.write('\n------------------------------\n')
    wr = WIDTH
    hr = HEIGHT
    res_1, res_2 = 0, 0

    box = (X1, YY, X1 + WIDTH, YY + HEIGHT)
    im1 = ImageGrab.grab(box)

    for j in range(2):
        express_1 = pytesseract.image_to_string(im1)
        if express_1 == 'a (ole)':
            res_1 = 100
            break
        else:
            express_1 = express_1.replace("x", "*")
            express_1 = express_1.replace("l", "1")
        # if len(express_1) > 16:
        #     sys.exit()
        try:
            res_1 = eval(express_1)
            # with open('w_log_comp.log', 'a') as log:
            #     log.write(f'{str(num + 1).zfill(2)} - attempt = {j+1} - express_1 = {express_1}\n')
            break
        except Exception as err:
            wr = round(wr * 0.7)
            hr = round(hr * 0.7)
            im1.thumbnail((wr, hr), Image.ADAPTIVE)
            if j == 1:
                with open('w_log_comp.log', 'a') as log:
                    try:
                        log.write(f'{str(num+1).zfill(2)} - express_1 = {express_1} - {err.__class__.__name__}\n')
                    except Exception as exc:
                        log.write(f'{str(num+1).zfill(2)} - express_1 = {exc.__class__.__name__}\n')
                # im_name = os.getcwd() + '\\log_' + str(num+1).zfill(2) + '.png'
                # im1.save(im_name, 'PNG')
                make_click(2)
                return

    box = (X2, YY, X2 + WIDTH, YY + HEIGHT)
    im2 = ImageGrab.grab(box)

    for j in range(2):
        express_2 = pytesseract.image_to_string(im2)
        if express_2 == 'a (ole)':
            res_2 = 100
            break
        else:
            express_2 = express_2.replace("x", "*")
            express_2 = express_2.replace("l", "1")
        try:
            res_2 = eval(express_2)
            # with open('w_log_comp.log', 'a') as log:
            #     log.write(f'{str(num + 1).zfill(2)} - attempt = {j+1} - express_2 = {express_2}\n')
            break
        except Exception as err:
            wr = round(wr * 0.7)
            hr = round(hr * 0.7)
            im2.thumbnail((wr, hr), Image.ADAPTIVE)
            if j == 1:
                with open('w_log_comp.log', 'a') as log:
                    try:
                        log.write(f'{str(num+1).zfill(2)} - express_2 = {express_2} - {err.__class__.__name__}\n')
                    except Exception as exc:
                        log.write(f'{str(num+1).zfill(2)} - express_2 = {exc.__class__.__name__}\n')
                # im_name = os.getcwd() + '\\log_' + str(num+1).zfill(2) + '_.png'
                # im2.save(im_name, 'PNG')
                make_click(1)
                return

    if isinstance(res_1, tuple):
        res_1 = res_1[0]
    if isinstance(res_2, tuple):
        res_2 = res_2[0]

    if res_1 > res_2:
        make_click(1)
    elif res_1 < res_2:
        make_click(2)
    else:
        make_click(0)


def make_click(button):
    if button == 1:
        mousePos((X_LEFT, Y_ANSWER))
    elif button == 2:
        mousePos((X_RIGHT, Y_ANSWER))
    else:
        mousePos((X_EQUAL, Y_ANSWER))
    leftClick()


def start_game():
    mousePos((1600, 80))
    for n in range(62):     # 68    # 50
        screen_grab(n)
        time.sleep(0.55)


def main():
    start_game()


if __name__ == '__main__':
    main()
