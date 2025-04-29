from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# game_url = "https://wikium.ru/challenge/12156/play"
CREDENTIALS = {
    "1": {"email": "lan2002@yandex.ru", "psw": "wikiu2349"},
    "2": {"email": "shkolamid@yandex.ru", "psw": "sm1962"},
    "3": {"email": "mezzo-2011@yandex.ru", "psw": "wikiu2349"}
}


def find_number():
    element_table = []
    number_to_find = ""
    n_account = input("Номер аккаунта: ")
    if int(n_account) not in range(1, 4):
        n_account = 2

    n_cycles = int(input("N loops: "))
    # n_cycles = 35

    n_play = int(input("Номер игры: "))
    game_url = f"https://wikium.ru/challenge/{n_play}/play"

    print("*** Когда появится кнопка 'Далее', надо кликнуть по ней и затем по экрану ***")
    time.sleep(1)

    account_email = CREDENTIALS.get(n_account).get("email")
    account_psw = CREDENTIALS.get(n_account).get("psw")

    browser = webdriver.Chrome()
    browser.get("https://wikium.ru/login")

    search_box = browser.find_element(By.ID, "Form_User_LoginForm_email")
    search_box.send_keys(account_email)
    search_box.send_keys(Keys.TAB)

    search_box = browser.find_element(By.ID, "Form_User_LoginForm_password")
    search_box.send_keys(account_psw)
    search_box.send_keys(Keys.RETURN)

    # Capture
    time.sleep(40)
    print("Время Capture истекло")

    start_time = time.time()
    browser.get(game_url)
    browser.fullscreen_window()
    end_time = time.time()

    time_for_fullscreen = end_time - start_time
    print(f"Время, затраченное на browser.get + browser.fullscreen_window: {time_for_fullscreen:.2f} секунд")

    # Пауза для клика на кнопке "Далее" и следующего клика на экране
    time.sleep(6)

    # # Клик по кнопке "Далее"
    # XX, YY = 760, 670
    # wait = WebDriverWait(browser, 10)
    # try:
    #     # button = wait.until(EC.element_to_be_clickable(
    #     #     (By.CSS_SELECTOR, '.game-screen__btn.game-screen__btn--desktop.btn.btn--purple.ng-scope')))
    #     button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".game-screen__btn--desktop")))
    # except  Exception as e:
    #     print(f"Клик по кнопке 'Далее' неудачен: {e}")
    #     pyautogui.moveTo(XX, YY)
    #     pyautogui.click()
    #     print(f"Клик на {XX}x{YY}")
    # else:
    #     button.click()
    # time.sleep(1)
    #
    # # Клик по экрану в любом месте
    # pyautogui.click()
    # print(f"Клик 2 на {XX}x{YY}")
    # # Отсчёт 3…2…1
    # time.sleep(4)

    # Switch to frame
    try:
        WebDriverWait(browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "play__iframe")))
    except Exception as e:
        print(f"Error (switch to frame): {e}")
    else:
        for _ in range(n_cycles):
            if browser.current_url != game_url:
                break
            try:
                element_to_find = browser.find_element(By.CSS_SELECTOR, '.number-one-numbers__task-reference')
                number_to_find = element_to_find.text
            except Exception as e:
                print(f"Error: {e}")

            try:
                element_table = browser.find_elements(By.CSS_SELECTOR, '.number-one-numbers__item-inner')
            except Exception as e:
                print(f"Error: {e}")

            for element in element_table:
                if element.text == number_to_find:
                    element.click()
                    break

            time.sleep(1)

        time.sleep(40)
    finally:
        browser.quit()


if __name__ == "__main__":
    find_number()
