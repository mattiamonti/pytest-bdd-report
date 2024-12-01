*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    ${url}=    Generate HTML Report    RFTest
    Open Browser    ${url}    ${BROWSER}

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

Element Tooltip Should Be
    [Arguments]     ${element}   ${text}
    Element Attribute Value Should Be  ${element}   title    ${text}
    
Element Style Should Contain
    [Arguments]     ${element}   ${text}
    ${style_result}=     Get Element Attribute   ${element}     style
    Should Contain    ${style_result}    ${text}
