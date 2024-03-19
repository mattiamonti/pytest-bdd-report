*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Feature with failed scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    ${feature}=    Set Variable     xpath=//*[@id="Calculator"]/div[1]
    Element Should Contain  ${feature}   Feature: Calculator
    Element Should Contain  ${feature}   Description: As an user i want to use the calculator app
    Element Should Contain  ${feature}   sample_features/calculator.feature
    Element Should Contain  xpath=//*[@id="Calculator"]/div[1]/div/div/div/p[2]     1

Feature with skipped scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    ${feature}=    Set Variable     xpath=//*[@id="Controls"]/div[1]
    Element Should Contain  ${feature}   Feature: Controls
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/controllo.feature
    Element Should Contain  xpath=//*[@id="Controls"]/div[1]/div/div/div/p[2]   2

Feature with passed scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    ${feature}=    Set Variable     xpath=//*[@id="Cucuber basket"]/div[1]
    Element Should Contain  ${feature}   Feature: Cucuber basket
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/scenario_outlines.feature
    Element Should Contain  xpath=//*[@id="Cucuber basket"]/div[1]/div/div/div/p   2

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
