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
    button_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    click_with_mouse_emulation(driver, button)
    random_sleep()

# Функция для ввода данных из twitch (из файла)
def enter_twitch_from_line(driver, password):
    twitch_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'  # Актуализируйте XPath
    twitch_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, twitch_xpath)))
    twitch_field.clear()
    random_sleep(0.05, 0.1)  # Уменьшаем паузы
    for character in password:
        twitch_field.send_keys(character)
        random_sleep(0.05, 0.1)  # Уменьшаем паузы

    # После ввода данных нажимаем Enter
    twitch_field.send_keys(Keys.RETURN)

# Чтение паролей из файла twitch.txt
with open("twitch.txt", "r", encoding="utf-8") as file:
    passwords = [line.strip() for line in file.readlines()]

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

    # Вводим пароль из файла
    if i < len(passwords):
        enter_twitch_from_line(driver, passwords[i])
    else:
        print(f"Пароль для вкладки {i + 1} не найден. Используются другие вкладки.")

    # Уменьшаем время ожидания, чтобы ускорить процесс
    random_sleep(0.2, 0.5)

button_xpath1 = '/html/body/div[3]/div/div[12]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3'
# Кликаем по кнопке на каждой вкладке
for i in range(num_tabs):
    driver.switch_to.window(driver.window_handles[i])  # Переключаемся на вкладку
    click_button(driver, button_xpath1)

# Завершаем выполнение программы
input("Нажмите Enter, чтобы закрыть браузер...")

driver.quit()
