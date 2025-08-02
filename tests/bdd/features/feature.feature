Feature: Test features

  @interaction
  Scenario: Check feature with passed scenario
    Given a test builder with a feature named 'Feature 1'
    And the feature 'Feature 1' has the description 'Sample description for the feature'
    And a passed scenario named 'Passing 1' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the feature 'Feature 1' should have path 'generated_tests/feature_1.feature'
    Then the feature 'Feature 1' should have description 'Sample description for the feature'
    Then the feature 'Feature 1' duration should not be zero
    Then the feature 'Feature 1' badge should have 1 passed scenarios

  @interaction
  Scenario: Check feature with failed scenario
    Given a test builder with a feature named 'Feature 1'
    And the feature 'Feature 1' has the description 'Sample description for the feature'
    And a failed scenario named 'Failing 1' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the feature 'Feature 1' should have path 'generated_tests/feature_1.feature'
    Then the feature 'Feature 1' should have description 'Sample description for the feature'
    Then the feature 'Feature 1' duration should not be zero
    Then the feature 'Feature 1' badge should have 1 failed scenarios

  @interaction
  Scenario: Check feature with skipped scenario
    Given a test builder with a feature named 'Feature 1'
    And the feature 'Feature 1' has the description 'Sample description for the feature'
    And a passed scenario named 'Passing 1' for the feature 'Feature 1'
    And a skipped scenario named 'Skipping 2' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the feature 'Feature 1' should have path 'generated_tests/feature_1.feature'
    Then the feature 'Feature 1' should have description 'Sample description for the feature'
    Then the feature 'Feature 1' duration should not be zero
    Then the feature 'Feature 1' badge should have 1 passed scenarios
    Then the feature 'Feature 1' badge should have 1 skipped scenarios

  @interaction
  Scenario: Feature should have correct badges for scenario number
    Given a test builder with a feature named 'Feature 1'
    And <passed> passed scenarios for the feature 'Feature 1'
    And <failed> failed scenarios for the feature 'Feature 1'
    And <skipped> skipped scenarios for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the feature 'Feature 1' badge should have <passed> passed scenarios
    Then the feature 'Feature 1' badge should have <failed> failed scenarios
    Then the feature 'Feature 1' badge should have <skipped> skipped scenarios

    Examples:
      | passed | failed | skipped |
      |      1 |      1 |       1 |
      |      2 |      0 |       0 |
      |      0 |      3 |       0 |
      |      3 |      7 |       0 |
      |      0 |      7 |       3 |
      |      3 |      0 |       7 |

    @load
    Examples:
      | passed | failed | skipped |
      |    150 |    300 |      50 |
