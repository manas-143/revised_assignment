from behave import *
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import time

"""locators for the webpage"""
tags = {
    "INPUT_AREA": "//*[@jslog='11886']",
    "SEARCH_BTN": "//*[@jslog='11887']",
    "SEARCH ITEMS": "//*[@class='Nv2PK THOPZb CpccDe ']/child::a",
    "PLACE_NAME": "//h1[@class='DUwDvf lfPIob']",
    "RATINGS": "//span[@class='ceNzKf']/preceding-sibling::span",
    "REVIEW": "(//div[@class='F7nice ']/child::span)[2]",
    "ADDRESS": "(//div[@class='rogA2c ']/child::div)[1]"

}
"""............................."""

places_list = []  # to store the final details of the places


@given(u'the user is on the Google Maps search for "{places}"')
def search_for_places(context, places):
    context.name = places
    context.wait = WebDriverWait(context.driver, 10)

    context.driver.get("https://www.google.com/maps")  # going to google map webpage
    search_box = context.wait.until(ec.presence_of_element_located((By.XPATH, tags["INPUT_AREA"])))
    search_box.send_keys(places)
    search_button = context.driver.find_element(By.XPATH, tags["SEARCH_BTN"])
    search_button.click()  # searching for the places


@when(u'the user scrolls down and loads "{num}" more places')
def scrolling_and_loading_the_place_details(context, num):
    total = int(num)  # converting the string format num to int

    """function for extracting restaurant details"""

    def places_info(arg):
        for i in range(total):

            d = {}
            arg[i].click()
            context.driver.implicitly_wait(20)
            time.sleep(5)  # used time.sleep as browser taking more time to load
            try:
                context.wait.until(ec.visibility_of_element_located((By.XPATH, tags["PLACE_NAME"])))
                d["name"] = context.driver.find_element(By.XPATH, tags["PLACE_NAME"]).text
            except:
                d["name"] = "name not found"
            try:
                context.wait.until(ec.visibility_of_element_located((By.XPATH, tags["RATINGS"])))
                d["ratings"] = context.driver.find_element(By.XPATH, tags["RATINGS"]).text
            except:
                d["ratings"] = "rating not found"
            try:
                context.wait.until(ec.visibility_of_element_located((By.XPATH, tags["REVIEW"])))
                d["review"] = context.driver.find_element(By.XPATH, tags["REVIEW"]).text
            except:
                d["review"] = "review not found"
            try:
                context.wait.until(ec.visibility_of_element_located((By.XPATH, tags["ADDRESS"])))
                d["address"] = context.driver.find_element(By.XPATH, tags["ADDRESS"]).text
            except:
                d["address"] = "address not found"

            """filtering and adding the details into the list"""

            if len(places_list) != total and d not in places_list:
                places_list.append(d)
                context.driver.find_element(By.XPATH, tags["SEARCH ITEMS"]).send_keys(Keys.DOWN)

    """-----------------------------------------"""

    places = []  # to store the list of the places displayed on the search result

    """running an infinite loop for scrolling down until user gets desire output"""
    while len(places) <= total:
        places = context.wait.until(ec.presence_of_all_elements_located((By.XPATH, tags["SEARCH ITEMS"])))
        single_item = context.wait.until(ec.presence_of_element_located((By.XPATH, tags["SEARCH ITEMS"])))
        single_item.send_keys(Keys.END)  # scrolling to the end
   
    places_info(places)  # running the function to extract the details


@then(u'the user should scrape and save information for the places in a csv file')
def scrape_and_save_the_information_in_CSV(context):
    # Specify the CSV file path
    csv_file_path = f'{context.name}'

    # Extract the keys from the first dictionary in the list (assuming all dictionaries have the same keys)
    field_names = places_list[0].keys()

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(places_list)
