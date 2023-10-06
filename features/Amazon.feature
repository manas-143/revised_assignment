Feature: Adding highly-rated Dell laptops to the Amazon cart

  Scenario Outline: Customer adds three highly-rated Dell laptops to the cart and verifies total price
    Given the user is on the Amazon.in homepage
    When the user searches for "<products>"
    Then the user adds "<number>" highly-rated Dell laptops to the cart
    And the user verifies the total price in the cart
    Examples:
    |    products     |number|
    |   dell laptops  |   3  |
    |   hp laptops    |   4  |
    |   acer laptops  |   7  |
