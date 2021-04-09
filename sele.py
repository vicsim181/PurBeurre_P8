from django.contrib.auth import login
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


# class UserStory1Test():

    # def settings():
    #     driver = Chrome()
    #     driver.maximize_window()
    #     driver.get("http://127.0.0.1:8000/")
    #     driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li > a').click()
    #     username = driver.find_element(By.CSS_SELECTOR, '#id_username')
    #     return username, driver

    # @staticmethod
    # def login_when_registered():
    #     # username, driver = UserStory1Test.settings()
    #     # assert driver.current_url == live_server_url + reverse('login')
    #     driver = Chrome()
    #     driver.maximize_window()
    #     driver.get("http://localhost:8000/")
    #     driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li > a').click()
    #     username = driver.find_element(By.CSS_SELECTOR, '#id_username')
    #     username.click()
    #     username.send_keys("victor@gmail.fr")
    #     password = driver.find_element(By.CSS_SELECTOR, '#id_password')
    #     password.click()
    #     password.send_keys("blabla75")
    #     driver.find_element(By.CSS_SELECTOR, '#page > div:nth-child(2) > div > div > form > button').click()
    #     driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li:nth-child(1) > a').click()
    #     driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li.nav-item.ml-4.mr-4 > a').click()
    #     driver.quit()


    # @staticmethod
    # def login_without_registered():
    #     username, driver = UserStory1Test.initialisation()
    #     username.click()
    #     username.send_keys("simon@gmail.fr")
    #     password = driver.find_element(By.CSS_SELECTOR, '#id_password')
    #     password.click()
    #     password.send_keys("blabla76")
    #     driver.find_element(By.CSS_SELECTOR, '#page > div:nth-child(2) > div > div > form > button').click()
    #     driver.quit()

def essai():
    driver = Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/")
    # login_option = driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li > a')
    # assertEqual(login_option.title, 'Se Connecter')
    driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li > a').click()
    username = driver.find_element(By.CSS_SELECTOR, '#id_username')
    username.click()
    username.send_keys("victor@gmail.fr")
    password = driver.find_element(By.CSS_SELECTOR, '#id_password')
    password.click()
    password.send_keys("blabla75")
    driver.find_element(By.CSS_SELECTOR, '#page > div:nth-child(2) > div > div > form > button').click()
    driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li:nth-child(1) > a').click()
    driver.find_element(By.CSS_SELECTOR, '#navbarResponsive > ul.navbar-nav.ml-auto.liste > li.nav-item.ml-4.mr-4 > a').click()


essai()
