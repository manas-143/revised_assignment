Feature: Scraping Google Maps for Restaurants

Scenario Outline: Scrape restaurants from Google Maps
    Given the user is on the Google Maps search for "<places>"
    When the user scrolls down and loads "<numbers>" more places
    Then the user should scrape and save information for the places in a csv file
    Examples:
    | places      | numbers|
    | restaurants |   30   |
    |  hospitals  |   10   |
    |     gym     |   12   |
