Feature: get company details
  Scenario Outline: Fetch company details and save to CSV
    Given the user is on the Google search page
    When the user searches for "<company name>"
    Then the user extracts the company details
    And the user saves the company details to a CSV file
    Examples:
      |        company name        |
      |actualize consulting pvt.ltd|
      |      aroha technologies    |
      |    microsoft corporations  |
      |              TCS           |