import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import os

# Настройка драйвера с инкогнито-режимом
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

# URL для открытия
url = 'https://www.twitch.tv/'
driver.get(url)

# Функция для нажатия на кнопку
def click_button(driver):
    button_xpath = '/html/body/div[1]/div/div[1]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button'
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    button.click()

def enter_data_from_line(driver, data):
    input_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/input'  # Замените на актуальный XPath поля ввода
    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    input_field.clear()
    input_field.send_keys(data)
    time.sleep(2)

# Чтение данных из файла
with open("twitch_login.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file.readlines()]

# Ввод первого значения и нажатие кнопки
click_button(driver)
enter_data_from_line(driver, lines[0])

# Запрашиваем у пользователя количество вкладок
num_tabs = int(input("Введите количество вкладок для открытия: "))

# Открытие новых вкладок и ввод данных из файла
for i in range(1, num_tabs):
    # Открываем новую вкладку с тем же URL
    driver.execute_script(f"window.open('{url}');")

    # Переключаемся на новую вкладку
    driver.switch_to.window(driver.window_handles[i])
    time.sleep(2)  # Пауза для загрузки страницы

    # Нажимаем кнопку и вводим строку
    click_button(driver)
    if i < len(lines):
        enter_data_from_line(driver, lines[i])
    else:
        print("Все строки из файла были введены.")
        break

# Возвращаемся на первую вкладку
driver.switch_to.window(driver.window_handles[0])

# Оставляем браузер открытым до нажатия Enter
input("Нажмите Enter, чтобы закрыть браузер...")

# Закрытие браузера
driver.quit()
