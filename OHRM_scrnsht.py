from selenium import webdriver
from selenium.webdriver.common.by import By
import time

links = {
    "username" : "//input[@name='username']",
    "password" : "//input[@name='password']",
    "submit"   : '//button[@type="submit"]'
    }
driver1=webdriver.Chrome()
driver1.maximize_window()
driver1.implicitly_wait(10)
driver1.get("https://opensource-demo.orangehrmlive.com/")
driver1.find_element(By.XPATH,links["username"]).send_keys("Admin")
driver1.find_element(By.XPATH,links["password"]).send_keys("admin123")
driver1.find_element(By.XPATH,links["submit"]).click()
screen = driver1.find_element(By.XPATH,"//div[@class='oxd-sheet oxd-sheet--rounded oxd-sheet--white orangehrm-dashboard-widget']/following::div[1]")
time.sleep(3)
screen.screenshot("screen.png")
driver1.quit()


