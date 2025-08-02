Feature: Check test file paths

  Background:
    Given a test builder with a feature named 'Feature 1'
    And 1 passed scenarios for the feature 'Feature 1'
    And 1 failed scenarios for the feature 'Feature 1'
    And 1 skipped scenarios for the feature 'Feature 1'
    And I build the feature
    When I create the report
    And I open the report

  @interaction
  Scenario: Open test file paths
    When I click on the test file paths button
    Then the test file paths should be visible

  @interaction
  Scenario: Close test file paths
    When I click on the test file paths button
    Then the test file paths should be visible
    When I click on the test file paths button
    Then the test file paths should be hidden

  @visual @smoke
  Scenario: Test file paths should contain all test files
    When I click on the test file paths button
    Then the test file paths should be visible
    Then the test file paths should contain the path 'generated_tests/test_steps.py'
