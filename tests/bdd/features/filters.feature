Feature: Check filters

  Background:
    Given a test builder with a feature named 'Feature ABC'
    And a passed scenario named 'Passing One' for the feature 'Feature ABC'
    And a failed scenario named 'Failing One' for the feature 'Feature ABC'
    And a skipped scenario named 'Skipping One' for the feature 'Feature ABC'
    And I build the feature
    When I create the report
    When I open the report

  @interaction @smoke
  Scenario: Filters should be enabled by default
    Then the 'passed' filter should be enabled
    Then the 'failed' filter should be enabled
    Then the 'skipped' filter should be enabled

  @interaction @smoke
  Scenario Outline: Filter out the <type> scenarios
    When I toggle the '<type>' filter
    Then the '<type>' filter should not be enabled
    Then the <type> scenarios should be hidden

    Examples:
      | type    |
      | passed  |
      | failed  |
      | skipped |

  @interaction
  Scenario Outline: Filter out a combination of scenarios
    When I toggle the '<first>' filter
    When I toggle the '<second>' filter
    Then the '<first>' filter should not be enabled
    Then the '<second>' filter should not be enabled
    Then the <first> scenarios should be hidden
    Then the <second> scenarios should be hidden

    Examples:
      | first  | second  |
      | passed | failed  |
      | passed | skipped |
      | failed | skipped |

  @interaction
  Scenario: Filter out all the scenarios
    When I toggle the 'passed' filter
    When I toggle the 'failed' filter
    When I toggle the 'skipped' filter
    Then the 'passed' filter should not be enabled
    Then the 'failed' filter should not be enabled
    Then the 'skipped' filter should not be enabled
    Then the passed scenarios should be hidden
    Then the failed scenarios should be hidden
    Then the skipped scenarios should be hidden

  @interaction
  Scenario Outline: Filter out and remove filter from <type> scenario
    When I toggle the '<type>' filter
    Then the <type> scenarios should be hidden
    When I toggle the '<type>' filter
    Then the <type> scenarios should be visible

    Examples:
      | type    |
      | passed  |
      | failed  |
      | skipped |
