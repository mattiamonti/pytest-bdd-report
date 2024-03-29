*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Failed scenario color
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${style_result}=     Get Element Attribute   ${feature}     style
    Should Contain    ${style_result}    rgb(249, 225, 229)

Skipped scenario color
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Shutdown"]/div
    Element Should Contain  ${feature}   Scenario: Shutdown
    ${style_result}=     Get Element Attribute   ${feature}     style
    Should Contain    ${style_result}    rgb(255, 248, 231)

Passed scenario color
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Eating cucumbers"]/div
    Element Should Contain  ${feature}   Scenario: Eating cucumbers
    ${style_result}=     Get Element Attribute   ${feature}     style
    Should Contain    ${style_result}    rgb(214, 240, 224)

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
