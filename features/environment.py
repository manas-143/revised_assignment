import time
from selenium import webdriver


def before_scenario(context,driver):
    context.driver = webdriver.Chrome()


def after_scenario(context,driver):
    context.driver.quit()


def after_step(context,step):
    print()
#process finished