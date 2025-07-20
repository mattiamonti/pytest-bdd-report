Feature: Scenario Modal Behavior

  Scenario: Open and close the Failed Scenarios link modal
    Given the report is open with a failed scenario
    When I open the failed scenarios modal
    Then the modal should be visible
    When I close the modal
    Then the modal should not be visible