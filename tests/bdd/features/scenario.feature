Feature: Check scenarios

  @visual @smoke
  Scenario Outline: Verify <type> scenario background color
    Given a test builder with a feature named 'Feature 1'
    And a <type> scenario named 'Scenario under test' for the feature 'Feature 1'
    And a passed scenario named 'Passed' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Scenario under test' should have <type> color

    Examples:
      | type    |
      | passed  |
      | failed  |
      | skipped |

  @visual
  Scenario: Verify multiple scenario background color
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Passed 1' for the feature 'Feature 1'
    And a failed scenario named 'Failed 1' for the feature 'Feature 1'
    And a skipped scenario named 'Skipped 1' for the feature 'Feature 1'
    And a failed scenario named 'Failed 2' for the feature 'Feature 1'
    And a passed scenario named 'Passed 2' for the feature 'Feature 1'
    And a skipped scenario named 'Skipped 2' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Passed 1' should have passed color
    Then the scenario 'Passed 2' should have passed color
    Then the scenario 'Failed 1' should have failed color
    Then the scenario 'Failed 2' should have failed color
    Then the scenario 'Skipped 1' should have skipped color
    Then the scenario 'Skipped 2' should have skipped color

  @interaction
  Scenario: Open failed scenario details
    Given a test builder with a feature named 'Feature 1'
    And a failed scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    When I toggle the scenario 'Scenario under test' error message
    Then the scenario 'Scenario under test' error message should be visible

  @interaction @smoke
  Scenario: Close failed scenario details
    Given a test builder with a feature named 'Feature 1'
    And a failed scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Scenario under test' error message should be hidden
    When I toggle the scenario 'Scenario under test' error message
    Then the scenario 'Scenario under test' error message should be visible
    When I toggle the scenario 'Scenario under test' error message
    Then the scenario 'Scenario under test' error message should be hidden

  @interaction
  Scenario Outline: Duration should not be zero for <type> scenario
    Given a test builder with a feature named 'Feature 1'
    And a <type> scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Scenario under test' duration should not be zero

    Examples:
      | type   |
      | passed |
      | failed |

  @interaction
  Scenario: Duration should be zero for skipped scenario
    Given a test builder with a feature named 'Feature 1'
    And a skipped scenario named 'Scenario under test' for the feature 'Feature 1'
    And a passed scenario named 'Passed' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Scenario under test' duration should be zero

  @interaction
  Scenario: Expand and collapse passed scenario
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    When I expand the scenario 'Scenario under test'
    Then the steps are visible for the scenario 'Scenario under test'
    When I collapse the scenario 'Scenario under test'
    Then the steps are not visible for the scenario 'Scenario under test'

  @interaction
  Scenario: Expand and collapse failed scenario
    Given a test builder with a feature named 'Feature 1'
    And a failed scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the steps are visible for the scenario 'Scenario under test'
    When I collapse the scenario 'Scenario under test'
    Then the steps are not visible for the scenario 'Scenario under test'
    When I expand the scenario 'Scenario under test'
    Then the steps are visible for the scenario 'Scenario under test'

  @interaction @current
  Scenario: Expand and collapse all scenarios
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Passed 1' for the feature 'Feature 1'
    And a failed scenario named 'Failed 1' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    When I expand all the scenarios
    Then the steps are visible for the scenario 'Passed 1'
    Then the steps are visible for the scenario 'Failed 1'
    When I collapse all the scenarios
    Then the steps are not visible for the scenario 'Passed 1'
    Then the steps are not visible for the scenario 'Failed 1'
