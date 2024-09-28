from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Координаты кнопки "Далее"
XX, YY = 760, 670
GAME_URL = "https://wikium.ru/game/number-one-numbers"


def find_number():
    # n_cycles = int(input("Число проходов for: "))
    n_cycles = 60

    credentials = {
        "email": ["mezzo-2011@yandex.ru"],  # Вставьте email своего аккаунта
        "psw": ["wikiu2349"]  # Вставьте свой пароль
    }

    browser = webdriver.Chrome()
    browser.get("https://wikium.ru/login")

    search_box = browser.find_element(By.ID, "Form_User_LoginForm_email")
    search_box.send_keys(credentials.get("email"))
    search_box.send_keys(Keys.TAB)

    search_box = browser.find_element(By.ID, "Form_User_LoginForm_password")
    search_box.send_keys(credentials.get("psw"))
    search_box.send_keys(Keys.RETURN)
    # Пауза на прохождение Capture
    time.sleep(20)

    browser.get(GAME_URL)
    browser.fullscreen_window()

    time.sleep(2)
    # Клик по кнопке "Далее"
    pyautogui.moveTo(XX, YY)
    pyautogui.click()

    time.sleep(1)
    # Клик в любой точке для старта
    pyautogui.click()
    time.sleep(3)
    pyautogui.moveTo(XX+400, YY+100)

    # Переключаемся во frame, в котором идёт тренажёр
    try:
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "game__iframe")))
    except Exception as e:
        print(f"Error (switch to frame): {e}")

    # Проходим тренажёр
    for _ in range(n_cycles):
        # Если минута истекла и тренажёр закрылся, завершаем цикл
        if browser.current_url != GAME_URL:
            break
        try:
            # Ищем элемент с загаданным числом
            element_to_find = browser.find_element(By.CSS_SELECTOR, '.number-one-numbers__task-reference')
            number_to_find = element_to_find.text
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Ищем элементы с числами таблицы
            element_table = browser.find_elements(By.CSS_SELECTOR, '.number-one-numbers__item-inner')
        except Exception as e:
            print(f"Error: {e}")

        # Ищем заданное число
        for element in element_table:
            if element.text == number_to_find:
                element.click()  # Если тексты элементов равны, кликаем по найденному объекту
                break

        # Ждём следующее число
        time.sleep(1)

    # Пауза перед закрытием тренажёра; смотрим результат
    time.sleep(30)
    browser.quit()


if __name__ == "__main__":
    find_number()


