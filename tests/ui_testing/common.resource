*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library    Collections

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    ${report_title}=    Set Variable    RFTest
    ${url}=    Generate HTML Report    ${report_title}
    Open Browser    ${url}    ${BROWSER}
    Page Should Contain    ${report_title}

Generate HTML Report
    [Arguments]    ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}

Get Feature
    [Arguments]    ${feature_name}
    ${feature}=    Set Variable    xpath=//*[@id="${feature_name}"]/div[1]
    Element Should Contain    ${feature}    Feature: ${feature_name}
    RETURN   ${feature}

Get Feature Scenarios
    [Arguments]    ${feature_name}
    ${scenarios}=    Get Web Elements    xpath=//*[@id="${feature_name}"]/div[2]/div
    RETURN    ${scenarios}

Get Scenario
    [Arguments]    ${scenario_name}
    ${scenario}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div
    Element Should Contain    ${scenario}    Scenario: ${scenario_name}
    RETURN   ${scenario}

Get Scenario Details Button
    [Arguments]    ${scenario_name}
    ${button}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div/button
    Element Should Be Visible   ${button}
    RETURN  ${button}

Get Scenario Steps
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    RETURN  ${current_steps}

Element Tooltip Should Be
    [Arguments]     ${element}   ${text}
    Element Attribute Value Should Be  ${element}   title    ${text}
    
Element Style Should Contain
    [Arguments]     ${element}   ${text}
    ${style_result}=     Get Element Attribute   ${element}     style
    Should Contain    ${style_result}    ${text}
