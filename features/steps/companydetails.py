# fetch_company_details.py
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from behave import *

# Set up the Selenium WebDriver (assuming you have installed the appropriate driver for your browser)





# BDD Steps
company_details=[]
@given("the user is on the Google search page")
def step_user_on_google_search_page(context):

    # Navigate to Google search page
    context.driver.get("https://www.google.com")
    context.driver.maximize_window()



@when('the user searches for "{company_name}"')
def step_user_searches_for(context, company_name):
    # Enter the search term and perform the search
    company = context.driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]')
    company.send_keys(company_name)
    company.send_keys(Keys.RETURN)
    time.sleep(2)


@then("the user extracts the company details")
def step_user_extracts_company_details(context):
    store_dict={}
    # Extract company details and store them in company_details list
    try:
        company_name = context.driver.find_element(By.XPATH, "//div[@class='SPZz6b']/h2/span")
        store_dict["company"] = company_name.text
    except:
        store_dict["company"] = "not found"
    try:
        company_add = context.driver.find_element(By.XPATH, '//span[@class="LrzXr"]')
        store_dict["address"] = company_add.text
    except:
        store_dict["address"] = "not found"
    try:
        reviews = context.driver.find_element(By.XPATH, '//div[@class="CJQ04"]/div/span[@class="hqzQac"]/span/a')
        store_dict["reviews"] = reviews.text
    except:
        store_dict["reviews"] = "not found"
    try:
        ratings = context.driver.find_element(By.XPATH, '//div[@class="CJQ04"]/div/span[@class="Aq14fc"]')
        store_dict["ratings"] = ratings.text
    except:
        store_dict["ratings"] = "not found"


    else:
        try:
            context.driver.find_element(By.XPATH, "(//*[@class='lu-fs'])[2]").click()
            url = context.driver.current_url
            pattern = r'@([0-9.-]+,[0-9.-]+,[0-9a-zA-Z]+)'
            matches = re.search(pattern, url)
            store_dict["latitude and longitude"] = matches.group(1)
            time.sleep(3)
        except:
            store_dict["latitude and longitude"]="not found"

    company_details.append(store_dict)


@then("the user saves the company details to a CSV file")
def step_user_saves_company_details_to_csv(context):
    # Specify the CSV file path
    csv_file_path = 'company_details2.csv'

    # Extract the keys from the first dictionary in the list (assuming all dictionaries have the same keys)
    field_names = company_details[0].keys()

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(company_details)

    print(f"Data has been successfully written to {csv_file_path}")


# Clean up after all the tests have run
# def after_all(context):
#     # Close the WebDriver
#     context.driver.quit()


