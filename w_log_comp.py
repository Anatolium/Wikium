from PIL import Image, ImageGrab, ImageChops
import os
import time
import win32api
import win32con
import cv2
import pytesseract

# X1, X2 = 500, 810
# YY = 435
# width = 270
# height = 80

# X1, X2 = 655, 860
# YY = 295
# width = 180
# height = 45

X1, X2 = 735, 890
YY = 273
width = 135
height = 30

X_LEFT = 810
X_EQUAL = 880
X_RIGHT = 950
Y_ANSWER = 405

# delta = 290
# im_name_1 = ''
# im_name_2 = ''

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):
    box = (X1, YY, X1 + width, YY + height)
    im = ImageGrab.grab(box)
    im_name_1 = os.getcwd() + "\\log_" + str(num + 1).zfill(2) + ".png"
    im.save(im_name_1, "PNG")

    image = cv2.imread(im_name_1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = f"{format(os.getpid())}.png"
    cv2.imwrite(filename, gray)

    image = Image.open(filename)
    # image = Image.open(im_name_1)

    express_1 = pytesseract.image_to_string(image)

    box = (X2, YY, X2 + width, YY + height)
    im = ImageGrab.grab(box)
    im_name_2 = os.getcwd() + "\\log_" + str(num + 1).zfill(2) + "_.png"
    im.save(im_name_2, "PNG")

    image = cv2.imread(im_name_2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = f"{format(os.getpid())}.png"
    cv2.imwrite(filename, gray)

    image = Image.open(filename)
    # image = Image.open(im_name_2)

    express_2 = pytesseract.image_to_string(image)

    with open('w_log_comp.log', 'a') as log:
        try:
            res_1 = eval(express_1)
            log.write(f"{str(num + 1).zfill(2)} res_1 - {res_1} \n")
            try:
                res_2 = eval(express_2)
                log.write(f"{str(num + 1).zfill(2)} res_2 - {res_2} \n")
                if res_1 > res_2:
                    # mousePos((650, 710))
                    mouse_pos((X_LEFT, Y_ANSWER))
                else:
                    mouse_pos((X_RIGHT, Y_ANSWER))
                left_click()

            except Exception as exc:
                log.write(f"{str(num + 1).zfill(2)} express_2 - {exc.__class__.__name__} \n")
                mouse_pos((X_LEFT, Y_ANSWER))
                left_click()
            else:
                os.remove(im_name_2)

        except Exception as exc:
            log.write(f"{str(num + 1).zfill(2)} express_1 - {exc.__class__.__name__} \n")
            mouse_pos((X_LEFT, Y_ANSWER))
            left_click()
        else:
            os.remove(im_name_1)


# ---------
# 67%
# ---------

def start_game():
    for n in range(30):
        screen_grab(n)
        time.sleep(1.5)


def main():
    start_game()


if __name__ == '__main__':
    main()
