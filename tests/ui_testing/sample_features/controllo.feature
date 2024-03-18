Feature: Controls
    Scenario: Startup
        Given I need a calculator
        When I press the on button
        Then The calculator is ready

    Scenario: Shutdown
        Given I have a calculator
        When I press the off button
        Then The calculator is off

    Scenario: Activation
        Given I have a calculator
        When I press the off button
        Then The calculator is off
