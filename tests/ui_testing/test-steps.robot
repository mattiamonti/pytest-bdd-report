*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String
Resource          common.resource
Resource          resources/step.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}        headlesschrome    #chrome
@{PASSED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I press the add button  Then: The result should be 7 on the screen
@{FAILED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I enter the number 3 into the calculator  And: I press the add button  Then: The result should be 101 on the screen

*** Test Cases ***
Passed Scenario Has Steps
    ${steps}=   step.Get Scenario Steps     Sum of a number
    Should Not Be Empty    ${steps}

Failed Scenario Has Steps
    ${steps}=   step.Get Scenario Steps     Sum of two numbers
    Should Not Be Empty    ${steps}

Skipped Scenario Has No Steps
    ${steps}=   step.Get Scenario Steps     Shutdown
    Should Be Empty    ${steps}

Check Passed Scenario Steps
    ${steps}=   step.Get Scenario Steps     Sum of a number
    Should Be Equal     ${steps}    ${PASSED_STEPS}
    
Check Failed Scenario Steps
    ${steps}=   step.Get Scenario Steps     Sum of two numbers
    Should Be Equal     ${steps}    ${FAILED_STEPS}

Check Durations For Passed Scenario
    ${durations}=   step.Get Scenario Steps Duration     Sum of a number
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}

Check Durations For Failed Scenario
    ${durations}=   step.Get Scenario Steps Duration     Sum of two numbers
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}
