Feature: User flows

  @flow
  Scenario: User search for the failed tests by filtering and navigating to the failes scenario
    Given a report with multiple features and all type of scenarios inside
    When I create the report
    And I open the report
    Then the feature statistic table should have a row for the feature 'Feature all scenarios'
    Then the feature statistic table should have a row for the feature 'Feature failed scenarios'
    When I toggle the 'passed' filter
    When I toggle the 'skipped' filter
    Then the 'failed' filter should be enabled
    When I click on the feature link 'Feature all scenarios'
    Then the feature 'Feature all scenarios' should be visible
    When I open the failed scenarios modal for the feature 'Feature all scenarios'
    Then the modal should be visible
    Then the modal should contain link with text "Failed scenario"
    When I click on the link "Failed scenario"
    Then the scenario "Failed scenario" should be visible
    When I click the return to top button
    When I click on the feature link 'Feature failed scenarios'
    Then the feature 'Feature failed scenarios' should be visible
    When I open the failed scenarios modal for the feature 'Feature failed scenarios'
    Then the modal should be visible
    Then the modal should contain link with text "Failed scenario 1"
    Then the modal should contain link with text "Failed scenario 2"
    Then the modal should contain link with text "Failed scenario 3"
    When I click on the link "Failed scenario 3"
    Then the scenario "Failed scenario 3" should be visible
    When I click the return to top button
    When I toggle the 'passed' filter
    When I toggle the 'skipped' filter
    Then the 'passed' filter should be enabled
    Then the 'skipped' filter should be enabled
    Then the 'failed' filter should be enabled
