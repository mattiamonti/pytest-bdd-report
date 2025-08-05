Feature: Check feature statistics table

  @visual
  Scenario: Feature statistic table has row for one feature
    Given a test builder with a feature named 'Feature 1'
    And 1 passed scenarios for the feature 'Feature 1'
    And 1 failed scenarios for the feature 'Feature 1'
    And 1 skipped scenarios for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report
    Then the feature statistic table should have a row for the feature 'Feature 1'

  @visual
  Scenario: Feature statistic table has row for multiple features
    Given a report with multiple features and all type of scenarios inside
    When I create the report
    And I open the report
    Then the feature statistic table should have a row for the feature 'Feature all scenarios'
    Then the feature statistic table should have a row for the feature 'Feature passed scenarios'
    Then the feature statistic table should have a row for the feature 'Feature failed scenarios'
    Then the feature statistic table should have a row for the feature 'Feature skipped scenarios'

  @visual @smoke
  Scenario Outline: Feature statistic table has correct values
    Given a report with multiple features and all type of scenarios inside
    When I create the report
    And I open the report
    Then the feature statistic table row for the feature '<feature>' should have <total> in column 'Total'
    Then the feature statistic table row for the feature '<feature>' should have <passed> in column 'Passed'
    Then the feature statistic table row for the feature '<feature>' should have <failed> in column 'Failed'
    Then the feature statistic table row for the feature '<feature>' should have <skipped> in column 'Skipped'
    Then the feature statistic table row for the feature '<feature>' should have <success_rate> in column 'Success Rate'
    Then the feature statistic table row for the feature '<feature>' should have <duration> in column 'Duration'

    Examples:
      | feature                   | total | passed | failed | skipped | success_rate | duration |
      | Feature all scenarios     |     3 |      1 |      1 |       1 |          33% | >0       |
      | Feature passed scenarios  |     3 |      3 |      0 |       0 |         100% | >0       |
      | Feature failed scenarios  |     3 |      0 |      3 |       0 |           0% | >0       |
      | Feature skipped scenarios |     4 |      1 |      0 |       3 |          25% | >0       |
