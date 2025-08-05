Feature: Feature table

  @navigation @smoke
  Scenario Outline: Navigate to a feature by link
    Given a test builder with a feature named 'Feature passed'
    And a passed scenario named 'Passed 1' for the feature 'Feature passed'
    And I build the feature
    Given a test builder with a feature named 'Feature failed'
    And a failed scenario named 'Failed 2' for the feature 'Feature failed'
    And I build the feature
    Given a test builder with a feature named 'Feature skipped'
    And a skipped scenario named 'Skipped 3' for the feature 'Feature skipped'
    And a passed scenario named 'Passed 4' for the feature 'Feature skipped'
    And I build the feature
    When I create the report
    And I open the report
    When I click on the feature link '<feature>'
    Then the feature '<feature>' should be visible

    Examples:
      | feature         |
      | Feature failed  |
      | Feature skipped |
      | Feature passed  |

  @navigation @regression
  Scenario Outline: Navigate to a long named feature by link
    Given a test builder with a feature named '<feature>'
    And a passed scenario named 'Passed 1' for the feature '<feature>'
    And I build the feature
    When I create the report
    And I open the report
    When I click on the feature link '<feature>'
    Then the feature '<feature>' should be visible

    Examples:
      | feature                                                                                                 |
      | Feature that has the longer name ever created in the realm of software engineering and testing combined |
