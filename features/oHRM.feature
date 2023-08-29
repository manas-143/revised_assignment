Feature: Deleting employee records

  Scenario: Delete multiple employee records
    Given the user is on the OrangeHRM website
    When the user logs in and adds new employees
    And the user deletes selected employee records
    Then the selected records should be deleted

