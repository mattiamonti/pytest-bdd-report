Feature: Report creation

  Scenario Outline: Check report content
    Given a test builder with <feature> feature
    And <passed> passed scenarios
    And <failed> failed scenarios
    And <skipped> skipped scenarios
    When I generate the report
    Then the report should have <feature> feature
    And the report should have <total> scenarios
    And the report should have <passed> passed scenarios
    And the report should have <failed> failed scenarios
    And the report should have <skipped> skipped scenarios

    Examples:
      | feature | total | passed | failed | skipped |
      |       1 |     1 |      1 |      0 |       0 |
      |       1 |     1 |      0 |      1 |       0 |
      |       1 |     2 |      1 |      1 |       0 |
      |       1 |     2 |      1 |      0 |       1 |
      |       1 |     2 |      0 |      1 |       1 |
      |       1 |     3 |      1 |      1 |       1 |
      |       1 |    10 |      5 |      2 |       3 |

  Scenario: Verify a report with all the possible scenario status in multiple features
    Given a test builder with a feature named 'Feature ABC'
    And a passed scenario named 'Passing One' for the feature 'Feature ABC'
    And I build the feature
    Given a test builder with a feature named 'Feature 123'
    And a skipped scenario named 'Skipping One' for the feature 'Feature 123'
    And a failed scenario named 'Failing One' for the feature 'Feature 123'
    And I build the feature
    When I create the report
    Then the report should have 2 feature
    And the report should have 3 scenarios
    And the report should have 1 skipped scenarios
    And the report should have 1 failed scenarios
    And the report should have 1 passed scenarios

  @current
  Scenario: Verify a report with all tests passed in a feature
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Passing 1' for the feature 'Feature 1'
    And a passed scenario named 'Passing 2' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    Then the report should have 1 feature
    And the report should have 2 scenarios
    And the report should have 2 passed scenarios

  @current
  Scenario: Verify a report with tests passed in multiple features
    Given a test builder with a feature named 'Feature 1'
    And a passed scenario named 'Passing 1' for the feature 'Feature 1'
    And I build the feature
    Given a test builder with a feature named 'Feature 2'
    And a passed scenario named 'Passing 2' for the feature 'Feature 2'
    And I build the feature
    When I create the report
    Then the report should have 2 feature
    And the report should have 2 scenarios
    And the report should have 2 passed scenarios

  @current
  Scenario: Verify a report with all tests failed in a feature
    Given a test builder with a feature named 'Feature 1'
    And a failed scenario named 'Failing 1' for the feature 'Feature 1'
    And a failed scenario named 'Failing 2' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    Then the report should have 1 feature
    And the report should have 2 scenarios
    And the report should have 2 failed scenarios

  @current
  Scenario: Verify a report with tests failed in multiple features
    Given a test builder with a feature named 'Feature 1'
    And a failed scenario named 'Failing 1' for the feature 'Feature 1'
    And I build the feature
    Given a test builder with a feature named 'Feature 2'
    And a failed scenario named 'Failing 2' for the feature 'Feature 2'
    And I build the feature
    When I create the report
    Then the report should have 2 feature
    And the report should have 2 scenarios
    And the report should have 2 failed scenarios

  @current
  Scenario Outline: Verify a report with some skipped scenario in a feature
    Given a test builder with a feature named 'Feature 1'
    And a skipped scenario named 'Passing 1' for the feature 'Feature 1'
    And a skipped scenario named 'Passing 2' for the feature 'Feature 1'
    And a <type> scenario named 'Passing 3' for the feature 'Feature 1'
    And I build the feature
    When I create the report
    Then the report should have 1 feature
    And the report should have 3 scenarios
    And the report should have 2 skipped scenarios
    And the report should have 1 <type> scenarios

    Examples:
      | type   |
      | passed |
      | failed |
