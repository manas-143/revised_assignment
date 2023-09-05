Feature: Adding highly-rated Dell laptops to the Amazon cart

  Scenario: Customer adds three highly-rated Dell laptops to the cart and verifies total price
    Given the Customer is on the Amazon.in homepage
    When the Customer searches for "dell laptops"
    Then the Customer adds three highly-rated Dell laptops to the cart
    And the Customer verifies the total price in the cart