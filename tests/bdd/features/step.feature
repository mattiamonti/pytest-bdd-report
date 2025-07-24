Feature: Check steps

  @interaction
  Scenario Outline: Verify steps in <type> scenario
    Given a test builder with a feature named 'Feature 1'
    And a <type> scenario named 'Scenario under test' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Scenario under test' should have <passed_count> passed steps
    Then the scenario 'Scenario under test' should have <failed_count> failed steps

    Examples:
      | type   | passed_count | failed_count |
      | passed |            1 |            0 |
      | failed |            0 |            1 |

  @interaction @smoke
  Scenario: Verify steps in a real <type> scenario
    Given a test builder with a feature named 'Feature 1'
    And a real <type> scenario for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Real scenario' should have <passed_count> passed steps
    Then the scenario 'Real scenario' should have <failed_count> failed steps

    Examples:
      | type   | passed_count | failed_count |
      | passed |            5 |            0 |
      | failed |            3 |            2 |

  @interaction @visual
  Scenario: Steps should have text
    Given a test builder with a feature named 'Feature 1'
    And a real failed scenario for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Real scenario' passed steps should have text 'step passed'
    Then the scenario 'Real scenario' failed steps should have text 'step '

  @interaction @visual
  Scenario: Duration should not be zero for passed and first failed steps
    Given a test builder with a feature named 'Feature 1'
    And a real failed scenario for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the scenario 'Real scenario' passed steps duration should not be zero
    Then the scenario 'Real scenario' failed steps duration should not be zero
