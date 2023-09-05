import time
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

'''-----------all the locators-------------'''
Locators = {"search_box": "twotabsearchtextbox",
            "search_button": "//input[@value='Go']",
            "rating_review_span_class": "span.a-icon-alt",
            "RATINGS": "//li[@id='p_72/1318476031']",
            "laptop_list_div": '//div[@data-component-type="s-search-result"]',
            "add_to_cart_button": '//input[@id="add-to-cart-button"]',
            "Price_tag": '//span[@class="a-price-whole"][1]',
            "cart_icon": '//div[@id="nav-cart-count-container"]',
            "total_price": '//span[@id="sc-subtotal-amount-activecart"]'
            }
'''----------------------------------------------'''
amount = []  # -----empty list to add the amount


@given("the Customer is on the Amazon.in homepage")
def amazon_login(context):
    context.wait = WebDriverWait(context.driver, 50)
    context.driver.get("https://www.amazon.in/")


@when('the Customer searches for "{search_query}"')
def search_for_laptops(context, search_query):
    search_box = context.driver.find_element(By.ID, Locators["search_box"])
    search_box.send_keys(search_query)
    search_button = context.driver.find_element(By.XPATH, Locators["search_button"])
    search_button.click()


@then("the Customer adds three highly-rated Dell laptops to the cart")
def add_laptops_to_cart(context):
    """ Filtering Laptop More than Four Rating """
    context.wait.until(ec.element_to_be_clickable((By.XPATH, Locators["RATINGS"]))).click()
    time.sleep(5)
    context.parent_url = context.driver.current_window_handle
    '''Now Adding Product To Cart Based On User Choice'''
    products = context.driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    count = 0
    for i in range(1, len(products)):
        if count == 5:
            break
        time.sleep(5)

        products[i].click()
        time.sleep(10)
        count += 1
        multiple_window = context.driver.window_handles
        for window in multiple_window:
            if window != context.parent_url:
                print(context.parent_url)
                print(window)
                context.driver.switch_to.window(window)
                price_element = context.driver.find_element(By.XPATH, Locators[
                    "Price_tag"])  # ----------price webelement of laptop
                p = price_element.get_attribute("innerHTML")  # price of laptop

                """extracting the price by replacing the unnecessary character"""
                amount.append(p.replace('<span class="a-price-decimal">.</span>', ""))

                context.wait.until(ec.element_to_be_clickable((By.XPATH, Locators["add_to_cart_button"]))).click()
                time.sleep(5)
                context.driver.close()
                multiple_window.remove(window)
                context.driver.switch_to.window(context.parent_url)


@then("the Customer verifies the total price in the cart")
def price_compare(context):
    cart_button = context.driver.find_element(By.XPATH, Locators["cart_icon"])
    cart_button.click()
    time.sleep(2)

    price = context.driver.find_element(By.XPATH, Locators["total_price"])
    time.sleep(3)
    final_price = price.text
    final_price = float(final_price.replace(",", ""))

    total_amount = sum(float(x.replace(',', '')) for x in amount)

    assert final_price == total_amount, "Total price in cart does not match with expected."


@then('the Customer closes the browser')
def close_browser(context):
    context.driver.quit()
