from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# all the XPATH of the O-HRM website that need to be tested
_LINKS = {
    "USERNAME": "//input[@name='username']",
    "PASSWORD": "//input[@name='password']",
    "SUBMIT": "//button[@type='submit']",
    "PIM_BTN": "//li[@class='oxd-main-menu-item-wrapper'][2]",
    "ADD_BTN": "//button/i[@class='oxd-icon bi-plus oxd-button-icon']",
    "FRST_NAME": "//input[@name='firstName']",
    "MIDDLE_NAME": "//input[@name='middleName']",
    "LAST_NAME": "//input[@name='lastName']",
    "ACTIVE_BTN": "//span[@class='oxd-switch-input oxd-switch-input--active --label-right']",
    "NEW_USER_NAME": "(//*[text()='Username']/following::input)[1]",
    "NEW_PASSWORD": "(//*[text()='Password']/following::input)[1]",
    "CONFIRM_PASSWORD": "(//*[text()='Confirm Password']/following::input)[1]",
    "SAVE_BTN": "//*[@type='submit']",
    "EMPLOYEE_DIV": "//div[@class='oxd-table-body']",
    "CHECK_BOX": "//div[@class='oxd-table-card-cell-checkbox']",
    "DLT_BTN": "//button[text()=' Delete Selected ']",
    "CONFIRM_DLT": "//div[@class='orangehrm-modal-footer']/button[2]"
}
# Orange_HRM url
url = "https://opensource-demo.orangehrmlive.com/"
# total records  user wants to delete
records_to_be_delete = 10


@given("the user is on the OrangeHRM website")
def opening_source_page(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.implicitly_wait(10)
    context.driver.get(url)  # orangehrm webpage


@when("the user logs in and adds new employees")
def logged_in_and_add_new_employee(context):
    # providing username and password for login
    context.driver.find_element(By.XPATH, _LINKS["USERNAME"]).send_keys("Admin")
    context.driver.find_element(By.XPATH, _LINKS["PASSWORD"]).send_keys("admin123")
    context.driver.find_element(By.XPATH, _LINKS["SUBMIT"]).click()

    # adding a new employee name and userID
    context.driver.find_element(By.XPATH, _LINKS["PIM_BTN"]).click()
    context.driver.find_element(By.XPATH, _LINKS["ADD_BTN"]).click()
    try:
        # sign-up for new username
        context.driver.find_element(By.XPATH, _LINKS["FRST_NAME"]).send_keys('Manas')
        context.driver.find_element(By.XPATH, _LINKS["MIDDLE_NAME"]).send_keys("kumar")
        context.driver.find_element(By.XPATH, _LINKS["LAST_NAME"]).send_keys("dash")
        context.driver.find_element(By.XPATH, _LINKS["ACTIVE_BTN"]).click()

        # creating new userID and password
        context.driver.find_element(By.XPATH, _LINKS["NEW_USER_NAME"]).send_keys('Manas1')
        context.driver.find_element(By.XPATH, _LINKS["NEW_PASSWORD"]).send_keys("12@manas")
        context.driver.find_element(By.XPATH, _LINKS["CONFIRM_PASSWORD"]).send_keys("12@manas")
        context.driver.find_element(By.XPATH, _LINKS["SAVE_BTN"]).click()
        wait = WebDriverWait(context.driver, 10)
        try:
            details = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='orangehrm-edit-employee-content']")))
        except:
            raise Exception("details are not saved")
    except:
        pass


@when("the user deletes selected employee records")
def select_and_delete_multiple_employee(context):
    context.driver.find_element(By.XPATH, _LINKS["pim_button"]).click()

    # selecting the employee name that user wants to delete
    parent_div = context.driver.find_element(By.XPATH, _LINKS["EMPLOYEE_DIV"])  # div that contains all the details div
    child_div = parent_div.find_elements(By.XPATH, _LINKS["CHECK_BOX"])  # selecting the checkboxes
    for user in range(records_to_be_delete):  # it contains the total number of records to be deleted
        child_div[user].click()

    # scrolling to the top of the webpage
    scroll_distance = -1700
    context.driver.execute_script(f"window.scrollTo(0, {scroll_distance});")

    # delete all the selected employee name
    context.driver.find_element(By.XPATH, _LINKS["DLT_BTN"]).click()
    context.driver.find_element(By.XPATH, _LINKS["CONFIRM_DLT"]).click()


@then("the selected records should be deleted")
def closing_the_browser(context):
    context.driver.quit()
