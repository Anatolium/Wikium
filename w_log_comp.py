from PIL import Image, ImageGrab, ImageChops
import os
import time
import win32api, win32con
import cv2
import pytesseract

X1, X2 = 500, 810
YY = 435
width = 270
height = 80

delta = 290
im_name_1 = ''
im_name_2 = ''

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def screen_grab(num):

    box = (X1, YY, X1+width, YY+height)
    im = ImageGrab.grab(box)
    im_name = os.getcwd() + '\\log_' + str(num+1).zfill(2) + '.png'
    im.save(im_name, 'PNG')

    image = cv2.imread(im_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    image = Image.open(filename)

    express_1 = pytesseract.image_to_string(image)

    box = (X2, YY, X2+width, YY+height)
    im = ImageGrab.grab(box)
    im_name = os.getcwd() + '\\log_' + str(num+1).zfill(2) + '_.png'
    im.save(im_name, 'PNG')

    image = cv2.imread(im_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    image = Image.open(filename)
    express_2 = pytesseract.image_to_string(image)

    with open('w_log_comp.log', 'a') as log:
        try:
            res_1 = eval(express_1)
            log.write(f'res_1 - {res_1} \n')
            try:
                res_2 = eval(express_2)
                log.write(f'res_2 - {res_2} \n')
                if res_1 > res_2:
                    mousePos((650, 710))
                else:
                    mousePos((930, 710))
                leftClick()

            except Exception as exc:
                log.write(f'express_2 - {exc.__class__.__name__} \n')
        except Exception as exc:
            log.write(f'express_1 - {exc.__class__.__name__} \n')



def start_game():
    for n in range(3):
        screen_grab(n)
        time.sleep(4.0)


def main():
    start_game()


if __name__ == '__main__':
    main()
