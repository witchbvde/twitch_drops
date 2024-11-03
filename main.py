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
import time
import pyautogui
import os

chrome_options = Options()
chrome_options.add_argument("--incognito")

# Инициализация драйвера с инкогнито-режимом
driver = webdriver.Chrome(options=chrome_options)
url = 'https://www.twitch.tv/'
driver.get(url)

def click_button(driver):
    button_xpath = '/html/body/div[1]/div/div[1]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button'
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    button.click()


num_tabs = int(input("Введите количество вкладок для открытия: "))

click_button(driver)

for i in range(1, num_tabs):
    # Открываем новую вкладку с тем же URL
    driver.execute_script(f"window.open('{url}');")

    # Получаем список вкладок и переключаемся на последнюю (только что открытую)
    driver.switch_to.window(driver.window_handles[i])

    # Даем время на загрузку страницы и выполняем нажатие кнопки
    click_button(driver)

# Возвращаемся на первую вкладку
driver.switch_to.window(driver.window_handles[0])

input()
