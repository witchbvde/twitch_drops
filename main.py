import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth  # Подключаем selenium-stealth

# Список User-Agent для случайного выбора
user_agents = [
    # Chrome (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",

    # Chrome (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36",

]
    # Настройка драйвера с подменой User-Agent и другими параметрами маскировки
chrome_options = Options()
chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")  # Случайный User-Agent
chrome_options.add_argument("--incognito")  # Инкогнито режим
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Отключение флагов автоматизации
chrome_options.add_experimental_option("useAutomationExtension", False)  # Отключение расширений для автоматизации

# Инициализация драйвера с отключением флага webdriver
driver = webdriver.Chrome(options=chrome_options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        });
    """
})

# URL для открытия
url = 'https://www.twitch.tv/'
driver.get(url)

# Функция для рандомизации времени ожидания
def random_sleep(min_time=0.5, max_time=2.0):
    time.sleep(random.uniform(min_time, max_time))

# Функция для клика с эмуляцией движений мыши
def click_with_mouse_emulation(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()

# Функция для нажатия на кнопку
def click_button(driver):
    button_xpath = '/html/body/div[1]/div/div[1]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button'
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    click_with_mouse_emulation(driver, button)
    random_sleep()

# Функция для ввода логина
def enter_data_from_line(driver, data):
    input_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/input'
    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    input_field.clear()
    random_sleep(0.1, 0.3)
    for character in data:  # Эмуляция ввода по символам
        input_field.send_keys(character)
        random_sleep(0.05, 0.2)

# Функция для ввода пароля
def enter_password_from_line(driver, password):
    password_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[2]/div/div[1]/div[2]/div[1]/div/input'
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, password_xpath)))
    password_field.clear()
    random_sleep(0.1, 0.3)
    for character in password:  # Эмуляция ввода по символам
        password_field.send_keys(character)
        random_sleep(0.05, 0.2)

# Функция для нажатия на кнопку входа после ввода логина и пароля
def submit_form(driver):
    submit_button_xpath = '/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div[2]/form/div/div[3]/div/button'
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    click_with_mouse_emulation(driver, submit_button)
    random_sleep()

# Чтение данных из файлов
with open("twitch_login.txt", "r", encoding="utf-8") as file:
    logins = [line.strip() for line in file.readlines()]

with open("twitch_password.txt", "r", encoding="utf-8") as file:
    passwords = [line.strip() for line in file.readlines()]

# Ввод первого логина и пароля
click_button(driver)
enter_data_from_line(driver, logins[0])
enter_password_from_line(driver, passwords[0])
submit_form(driver)

# Запрашиваем у пользователя количество вкладок
num_tabs = int(input("Введите количество вкладок для открытия: "))

# Открытие новых вкладок и ввод данных из файлов
for i in range(1, num_tabs):
    driver.execute_script(f"window.open('{url}');")
    driver.switch_to.window(driver.window_handles[i])
    random_sleep(1, 2)

    click_button(driver)
    if i < len(logins) and i < len(passwords):
        enter_data_from_line(driver, logins[i])
        enter_password_from_line(driver, passwords[i])
        submit_form(driver)
    else:
        print("Все строки из файлов были введены.")
        break

# Возвращаемся на первую вкладку
driver.switch_to.window(driver.window_handles[0])
input("Нажмите Enter, чтобы закрыть браузер...")

driver.quit()
