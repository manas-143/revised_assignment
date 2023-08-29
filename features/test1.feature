Feature: Search Functionality

  Scenario Outline: Search for a valid product
    Given User got navigated to webpage
    When User entered username as "<email>" and password as "<password>" into seachbox field
    And User clicked on search button
    Then Valid product should get displayed
    Examples:
      |    email    |password|
      |abc@gmail.com|abc123  |
      |xyz@gmail.com|xyz@123 |
      |ff@gmail.com |ff@123  |