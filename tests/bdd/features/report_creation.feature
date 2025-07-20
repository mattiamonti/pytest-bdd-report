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
