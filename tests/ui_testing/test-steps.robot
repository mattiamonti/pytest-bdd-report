*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String
Resource          common.robot
Resource          step_keywords.robot

*** Variables ***
${BROWSER}        headlesschrome    #chrome
@{PASSED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I press the add button  Then: The result should be 7 on the screen
@{FAILED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I enter the number 3 into the calculator  And: I press the add button  Then: The result should be 101 on the screen

*** Test Cases ***
Passed Scenario Has Steps
    Open Report In Browser
    ${steps}=   Get Scenario Steps     Sum of a number
    Should Not Be Empty    ${steps}

Failed Scenario Has Steps
    Open Report In Browser
    ${steps}=   Get Scenario Steps     Sum of two numbers
    Should Not Be Empty    ${steps}

Skipped Scenario Has No Steps
    Open Report In Browser
    ${steps}=   Get Scenario Steps     Shutdown
    Should Be Empty    ${steps}

Check Passed Scenario Steps
    Open Report In Browser
    ${steps}=   Get Scenario Steps     Sum of a number
    Should Be Equal     ${steps}    ${PASSED_STEPS}
    
Check Failed Scenario Steps
    Open Report In Browser
    ${steps}=   Get Scenario Steps     Sum of two numbers
    Should Be Equal     ${steps}    ${FAILED_STEPS}

Check Durations For Passed Scenario
    Open Report In Browser
    ${durations}=   Get Scenario Steps Duration     Sum of a number
    List Should Not Contain Value   ${durations}    0.0

Check Durations For Failed Scenario
    Open Report In Browser
    ${durations}=   Get Scenario Steps Duration     Sum of two numbers
    List Should Not Contain Value   ${durations}    0.0

