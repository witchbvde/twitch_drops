import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Импортируем Keys для использования клавиши Enter
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth  # Подключаем selenium-stealth

# Настройка драйвера с подключением к уже открытому браузеру
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Подключение к уже открытому браузеру
driver = webdriver.Chrome(options=chrome_options)

# Дальше можно управлять браузером
driver.get("https://www.google.com")

# Функция для рандомизации времени ожидания
def random_sleep(min_time=0.5, max_time=2.0):
    time.sleep(random.uniform(min_time, max_time))

# Функция для клика с эмуляцией движений мыши
def click_with_mouse_emulation(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()

# Функция для нажатия на кнопку
def click_button(driver):
    button_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'  # Измените на актуальный XPath
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    click_with_mouse_emulation(driver, button)
    random_sleep()

# Функция для ввода данных из twitch (из файла)
def enter_twitch_from_line(driver, password):
    twitch_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'  # Актуализируйте XPath
    twitch_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, twitch_xpath)))
    twitch_field.clear()
    random_sleep(0.1, 0.3)
    for character in password:  # Эмуляция ввода по символам
        twitch_field.send_keys(character)
        random_sleep(0.05, 0.2)

    # После ввода данных нажимаем Enter
    twitch_field.send_keys(Keys.RETURN)  # Эмуляция нажатия клавиши Enter

# Чтение паролей из файла twitch.txt
with open("twitch.txt", "r", encoding="utf-8") as file:
    passwords = [line.strip() for line in file.readlines()]

# Выполняем действия на первой вкладке
click_button(driver)
enter_twitch_from_line(driver, passwords[0])  # Вводим первый пароль из файла

# Запрашиваем у пользователя количество вкладок
num_tabs = int(input("Введите количество вкладок для открытия: "))

# Открытие новых вкладок и ввод данных из файлов
for i in range(1, num_tabs):
    driver.execute_script("window.open();")  # Открываем новую вкладку
    driver.switch_to.window(driver.window_handles[i])  # Переключаемся на последнюю вкладку
    random_sleep(1, 2)

    click_button(driver)  # Нажимаем кнопку на новой вкладке
    if i < len(passwords):  # Если есть пароль, вводим его
        enter_twitch_from_line(driver, passwords[i])
    else:
        print("Все строки из файла были использованы.")
        break

# Возвращаемся на первую вкладку
driver.switch_to.window(driver.window_handles[0])

input("Нажмите Enter, чтобы закрыть браузер...")

driver.quit()
