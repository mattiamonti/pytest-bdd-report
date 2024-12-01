*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String

*** Variables ***
${BROWSER}        headlesschrome    #chrome

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
