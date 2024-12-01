*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String

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

*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    ${url}=    Generate HTML Report    RFTest
    Open Browser    ${url}    ${BROWSER}

Get Scenario Steps
    [Arguments]    ${scenario_name}
    ${scenario}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div
    Element Should Contain    ${scenario}    Scenario: ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    RETURN  ${current_steps}

Get Scenario Steps Duration
    [Arguments]    ${scenario_name}
    ${scenario}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div
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

Generate HTML Report
    [Arguments]    ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}
