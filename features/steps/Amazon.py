from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

'''-----------all the locators-------------'''
Locators = {"search_box": "twotabsearchtextbox",
            "search_button": "//input[@value='Go']",
            "rating_review_span_class": "span.a-icon-alt",
            "RATINGS": "//li[@id='p_72/1318476031']",
            "laptop_list_div": "//span[@class='a-size-medium a-color-base a-text-normal']",
            "add_to_cart_button": '//input[@id="add-to-cart-button"]',
            "Price_tag": '//span[@class="a-price-whole"][1]',
            "cart_icon": '//div[@id="nav-cart-count-container"]',
            "total_price": '//span[@id="sc-subtotal-amount-activecart"]'
            }
'''----------------------------------------------'''

amount = []  # -----empty list to add the amount


@given("the Customer is on the Amazon.in homepage")
def amazon_login(context):
    context.wait = WebDriverWait(context.driver, 100)
    context.driver.get("https://www.amazon.in/")


@when('the Customer searches for "{search_query}"')
def search_for_laptops(context, search_query):

    """searching the product in the search tab"""

    search_box = context.driver.find_element(By.ID, Locators["search_box"])
    search_box.send_keys(search_query)
    search_button = context.driver.find_element(By.XPATH, Locators["search_button"])
    search_button.click()


@then("the Customer adds three highly-rated Dell laptops to the cart")
def add_laptops_to_cart(context):

    """ Filtering Laptop More than Four Rating """

    context.wait.until(ec.element_to_be_clickable((By.XPATH, Locators["RATINGS"]))).click()
    parent_window = context.driver.current_window_handle  # for storing the parent windows id
    products = context.wait.until(ec.presence_of_all_elements_located((By.XPATH, Locators["laptop_list_div"])))  # storing all the products

    """ clicking each product and adding it to cart"""

    for i in range(1, 5):  # iterate over product list
        products[i].click()
        windows = context.driver.window_handles  # storing the child windows address
        context.driver.switch_to.window(windows[1])  # switching to the child window to add the product to cart

        price_element = context.driver.find_element(By.XPATH, Locators["Price_tag"])  # price web-element of laptop
        p = price_element.get_attribute("innerHTML")  # price of laptop
        amount.append(p.replace('<span class="a-price-decimal">.</span>', ""))  # adding the amount to the list for sum

        context.wait.until(ec.presence_of_element_located((By.XPATH, Locators["add_to_cart_button"]))).click()  # adding the product to cart
        context.wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='attachDisplayAddBaseAlert']")))  # waiting for a element to confirm that product is added

        context.driver.close()
        context.driver.switch_to.window(parent_window) # after every iteration completed we switch to parent window for going to next item


@then("the Customer verifies the total price in the cart")
def price_compare(context):
    """going to cart button to see the final price"""
    cart_button = context.driver.find_element(By.XPATH, Locators["cart_icon"])
    cart_button.click()

    """extracting the price that displayed on the cart"""

    price = context.wait.until(ec.presence_of_element_located((By.XPATH, Locators["total_price"])))
    final_price = price.text
    final_price = float(final_price.replace(",", ""))
    total_amount = sum(float(x.replace(',', '')) for x in amount)

    assert final_price == total_amount, "Total price in cart does not match with expected."  # checking the final price is same or not


@then('the Customer closes the browser')
def close_browser(context):
    context.driver.quit()
