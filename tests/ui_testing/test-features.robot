*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Resource    common.robot

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Feature with failed scenarios
    Open Report In Browser
    ${feature}=  Get Feature     Calculator
    Element Should Contain  ${feature}   Description: As an user i want to use the calculator app
    Element Should Contain  ${feature}   sample_features/calculator.feature
    Element Should Contain  ${feature}/div/div/div/p[2]     1

Feature with skipped scenarios
    Open Report In Browser
    ${feature}=  Get Feature     Controls
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/controllo.feature
    Element Should Contain  ${feature}/div/div/div/p[2]   2

Feature with passed scenarios
    Open Report In Browser
    ${feature}=  Get Feature     Cucuber basket
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/scenario_outlines.feature
    Element Should Contain  ${feature}/div/div/div/p   2

