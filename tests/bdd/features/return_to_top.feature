Feature: Return to top

  Background:
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Passing 1' for the feature 'Feature 1'
    And a passed scenario named 'Passing 2' for the feature 'Feature 1'
    And a passed scenario named 'Passing 3' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report

  @interaction @smoke
  Scenario: Return to top using the button
    When I scroll to the bottom
    And I click the return to top button
    Then the report should be at the top

  @interaction
  Scenario: On hover the button should display the text
    Then the button should not contain text 'Return'
    When I hover on the return to top button
    Then the button should contain text 'Return'

  @interaction
  Scenario: Click the return to top button after hover animation
    When I scroll to the bottom
    And I hover on the return to top button
    Then the button should contain text 'Return'
    When I click the return to top button
    Then the report should be at the top
