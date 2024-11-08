import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Настройка драйвера с подключением к уже открытому браузеру
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Подключение к уже открытому браузеру
driver = webdriver.Chrome(options=chrome_options)


# Функция для рандомизации времени ожидания (уменьшаем задержки)
def random_sleep(min_time=0.1, max_time=1.0):
    time.sleep(random.uniform(min_time, max_time))


# Функция для клика с эмуляцией движений мыши
def click_with_mouse_emulation(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.05, 0.1)).click().perform()


# Функция для нажатия на кнопку
def click_button(driver, xpath):
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    click_with_mouse_emulation(driver, button)
    random_sleep()


# Функция для ввода пароля из файла twitch.txt
def enter_twitch_from_line(driver, password):
    twitch_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'  # Обновите XPath
    twitch_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, twitch_xpath)))
    twitch_field.clear()
    random_sleep(0.05, 0.1)  # Уменьшаем паузы
    for character in password:
        twitch_field.send_keys(character)
        random_sleep(0.05, 0.1)  # Уменьшаем паузы

    # После ввода данных нажимаем Enter
    twitch_field.send_keys(Keys.RETURN)


# Функция для ввода логина из файла twitch_login.txt
def enter_login(driver, login):
    login_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/input'  # Обновите XPath для поля логина
    login_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
    login_field.clear()
    random_sleep(0.05, 0.1)
    for character in login:
        login_field.send_keys(character)
        random_sleep(0.05, 0.1)

    # Нажимаем "Enter" для отправки
    login_field.send_keys(Keys.RETURN)


# Функция для ввода пароля из файла twitch_password.txt
def enter_password(driver, password):
    password_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[2]/div/div[1]/div[2]/div[1]/div/input'  # Обновите XPath для поля пароля
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, password_xpath)))
    password_field.clear()
    random_sleep(0.05, 0.1)
    for character in password:
        password_field.send_keys(character)
        random_sleep(0.05, 0.1)

    # Нажимаем "Enter" для отправки
    password_field.send_keys(Keys.RETURN)


# Чтение логинов и паролей из файлов
with open("twitch_login.txt", "r", encoding="utf-8") as file:
    logins = [line.strip() for line in file.readlines()]

with open("twitch_password.txt", "r", encoding="utf-8") as file:
    passwords = [line.strip() for line in file.readlines()]

# Чтение паролей из файла twitch.txt (для вставки в нужное поле)
with open("twitch.txt", "r", encoding="utf-8") as file:
    twitch_passwords = [line.strip() for line in file.readlines()]

# Запрашиваем у пользователя количество вкладок
num_tabs = int(input("Введите количество вкладок для открытия: "))

# Открываем все вкладки сразу
for i in range(1, num_tabs):
    driver.execute_script("window.open();")  # Открываем новую вкладку

# Выполняем действия на каждой вкладке
for i in range(num_tabs):
    driver.switch_to.window(driver.window_handles[i])  # Переключаемся на вкладку

    # Не загружаем страницу заново, если она уже загружена
    driver.get("https://www.google.com")  # Можно заменить на актуальный URL, если нужно


    # Вводим данные из файла twitch.txt (пароли)
    if i < len(twitch_passwords):
        enter_twitch_from_line(driver, twitch_passwords[i])

    # Уменьшаем время ожидания, чтобы ускорить процесс
    random_sleep(0.2, 0.5)


# XPath первой кнопки
button_xpath1 = '/html/body/div[3]/div/div[12]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3'

# XPath второй кнопки (например, кнопка для действий на Twitch)
button_xpath2 = '/html/body/div[1]/div/div[1]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button'  # Замените на актуальный XPath для второй кнопки

# Кликаем по кнопке на каждой вкладке
for i in range(num_tabs):
    driver.switch_to.window(driver.window_handles[i])  # Переключаемся на вкладку

    # Клик по первой кнопке
    click_button(driver, button_xpath1)

    # Уменьшаем время ожидания
    random_sleep(0.2, 0.5)

    # Если это твич или страница с кнопкой для второго действия, нажимаем вторую кнопку
    if "twitch" in driver.current_url:  # Если текущий URL содержит "twitch", это предполагает, что мы на сайте Twitch
        click_button(driver, button_xpath2)

        # Вводим логин и пароль из файлов
        if i < len(logins) and i < len(passwords):
            enter_login(driver, logins[i])  # Вводим логин
            enter_password(driver, passwords[i])  # Вводим пароль
        else:
            print(f"Логин и пароль для вкладки {i + 1} не найдены. Используются другие вкладки.")

# Завершаем выполнение программы
input("Нажмите Enter, чтобы закрыть браузер...")

driver.quit()
