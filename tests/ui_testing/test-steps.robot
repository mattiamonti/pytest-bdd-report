*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String
Resource          common.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}        headlesschrome    #chrome
@{PASSED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I press the add button  Then: The result should be 7 on the screen
@{FAILED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I enter the number 3 into the calculator  And: I press the add button  Then: The result should be 101 on the screen

*** Test Cases ***
Passed Scenario Has Steps
    ${steps}=   Get Scenario Steps     Sum of a number
    Should Not Be Empty    ${steps}

Failed Scenario Has Steps
    ${steps}=   Get Scenario Steps     Sum of two numbers
    Should Not Be Empty    ${steps}

Skipped Scenario Has No Steps
    ${steps}=   Get Scenario Steps     Shutdown
    Should Be Empty    ${steps}

Check Passed Scenario Steps
    ${steps}=   Get Scenario Steps     Sum of a number
    Should Be Equal     ${steps}    ${PASSED_STEPS}
    
Check Failed Scenario Steps
    ${steps}=   Get Scenario Steps     Sum of two numbers
    Should Be Equal     ${steps}    ${FAILED_STEPS}

Check Durations For Passed Scenario
    ${durations}=   Get Scenario Steps Duration     Sum of a number
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}

Check Durations For Failed Scenario
    ${durations}=   Get Scenario Steps Duration     Sum of two numbers
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}

*** Keywords ***
Get Scenario Steps Duration
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    Element Should Contain    ${scenario}    Scenario: ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}/div[2]/*[@class="step-container"]/p
    ${current_durations}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           ${text}=    Remove String   ${text}     ms
           ${duration}=     Convert To Number   ${text}
           Append To List   ${current_durations}    ${duration}
    END
    RETURN    ${current_durations}

