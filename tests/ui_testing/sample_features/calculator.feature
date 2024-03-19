Feature: Calculator
	As an user i want to use the calculator app 
    Scenario: Sum of a number
        Given I have a calculator
        When I enter the number 7 into the calculator
        And I press the add button
        Then The result should be 7 on the screen
    
    Scenario: Sum of two numbers
        Given I have a calculator
        When I enter the number 7 into the calculator
        And I enter the number 3 into the calculator
        And I press the add button
        Then The result should be 101 on the screen

    Scenario: Sum of negative numbers
        Given I have a calculator
        When I enter the number 5 into the calculator
        And I enter the number -2 into the calculator
        And I press the add button
        Then The result should be 3 on the screen
