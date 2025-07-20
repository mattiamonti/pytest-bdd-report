Feature: Scenario Modal Behavior

  Scenario: Open and close the Failed Scenarios link modal
    Given the report is open with a failed scenario
    Then the modal should not be visible
    When I open the failed scenarios modal
    Then the modal should be visible
    When I close the modal
    Then the modal should not be visible

  Scenario: Verify modal content
    Given the report is open with multiple failed scenarios
    When I open the failed scenarios modal
    Then the modal should be visible
    Then the modal should contain 3 link
    Then the modal should contain link with text "Failed 1"
    Then the modal should contain link with text "Failed 2"
    Then the modal should contain link with text "Failed 3"

  Scenario: Failed scenarios link should be present in failed feature
    Given the report is open with a failed scenario
    Then the feature scenarios link should be visible 

  Scenario: Failed scenarios link should be present in passed feature
    Given the report is open with a passed scenario
    Then the feature scenarios link should not be visible 

