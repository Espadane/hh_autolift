# !путь до интерпритатора python, можно узнать командой "which python3"
# crontab -e - редактировать крон 
# crontab -ls - процессы крона для пользователя 
# * 4 * * * python3 pwd - крон будет запускать скрипт каждые 4 часа, нужно прописать абсолютный путь до скрипта
from config import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


class ResumeLifter():
    """Класс поднимателя резюме в выдаче"""
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) #loging off
        self.options.add_argument('--headless') #headless mode
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=ex_pass, 
                    options=self.options)
    @staticmethod
    def print_to_file(message):
        """Метод вывода принтов в файл"""
        log_file = 'absolute/path/to/log/file' #абсолютный путь до файла логов
        message_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

        with open(f'{log_file}', 'a') as f:
            print(f'{message}    [{message_time}] ', file=f)
        
    def login_to_hh(self):
        """Входим в учетную запись HeadHunter и переходим на страницу резюме"""
        try:
            driver = self.driver
            driver.get('https://hh.ru')

            #Кликаем по кнопке "Вход"
            try:
                driver.implicitly_wait(10)
                enter_btn = driver.find_element(by=By.XPATH,value='/html/body/div[7]/div/div[1]/div[1]/div/div[6]/a')
                enter_btn.click()
                self.print_to_file('[!] - Кнопка "Вход" нажата.')
            except Exception as error:
                self.print_to_file(f'[X] - Ошибка: клик по кнопке "Вход" не удался.\n{error}\n')

            # Клик по кнопке войти с паролем
            try:
                driver.implicitly_wait(10)
                enter_with_pass_btn = driver.find_elements(by=By.TAG_NAME,value='button')[11]
                enter_with_pass_btn.click()
                self.print_to_file('[!] - Кликнули на кнопку "Войти по паролю".')
            except Exception as error:
                self.print_to_file(f'[X] - Ошибка: клик по кнопке "Войти с паролем" не удался.\n{error}\n')

            #Вход в учетную запись
            try:
                driver.implicitly_wait(10)
                login_form = driver.find_element(by=By.XPATH, value='//*[@id="HH-React-Root"]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/form/div[1]/input')
                login_form.send_keys(hh_login)
                password_form = driver.find_element(by=By.XPATH, value='//*[@id="HH-React-Root"]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/form/div[2]/span/input')
                password_form.send_keys(hh_password)
                login_btn = driver.find_element(by=By.XPATH, value='//*[@id="HH-React-Root"]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/form/div[4]/div/button[1]')
                login_btn.click()
                self.print_to_file('[!] - Залогинились!')
            except Exception as error:
                self.print_to_file(f'[X] - Ошибка: не удалось залогиниться.\n{error}\n')

            # Переходим на страницу с резюме
            try:
                driver.implicitly_wait(10)
                my_resume_btn = driver.find_element(by=By.XPATH, value='/html/body/div[6]/div[1]/div/div/div[1]/div[1]/a')
                my_resume_btn.click()
                self.print_to_file('[!] - Переход на страницу с резюме выполнен.')
            except Exception as error:
                self.print_to_file(f'[X] - Ошибка: не удалось перейти на страницу с резюме.\n{error}\n')
        except Exception as error:
            self.print_to_file('[X] - Ошибка: не удалось создать браузер.')

    def get_lift_time(self):
            """Получаем время следующего поднятия резюме """
            driver = self.driver
            try:
                driver.implicitly_wait(20)
                lift_time = driver.find_element(by=By.CLASS_NAME, value='applicant-resumes-action').text.strip()[-5:]
                self.print_to_file(f'[!] - Время поднятия резюме - {lift_time}.')
            except Exception as error:
                lift_time = None
                self.print_to_file(f'[X] - Ошибка: не удалось получить время следующего поднятия резюме.\n{error}\n')

            return lift_time
    
    def lift_resume(self):
        """ Поднимаем резюме"""
        driver = self.driver
        #Пытаемся поднять резюме
        try:
            driver.implicitly_wait(10)
            lift_btn = driver.find_element(by=By.XPATH, value='//*[@id="HH-React-Root"]/div/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[6]/div/div/div/div[1]/span/button')
            lift_btn.click()
            self.print_to_file('[!] - Поднятие резюме в поиске успешно!')
        except Exception:
            self.print_to_file(f'[!] - Поднимать резюме пока рано. Время следующего поднятия - {self.get_lift_time()}')

    def close_driver(self):
        """Закрываем браузер"""
        self.driver.quit()
        self.print_to_file(f'[!] - Браузер закрыт!')


def main():
    resume_lifter = ResumeLifter()
    resume_lifter.login_to_hh()
    resume_lifter.lift_resume()
    resume_lifter.get_lift_time()
    resume_lifter.close_driver()



if __name__ == '__main__':
    main()