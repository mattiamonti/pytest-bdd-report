*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library  String
Resource    common.resource

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

Feature With Passed Template Scenarios
    Open Report In Browser
    ${feature}=  Get Feature     Cucuber basket
    Element Should Contain  ${feature}/div/div/div/p   2
    ${scenarios}=   Get Feature Scenarios   Cucuber basket
    FOR    ${scenario}    IN    @{scenarios}
        ${class}=  Get Element Attribute    ${scenario}    class
        Should Contain   ${class}    passed
    END

Check Features Execution Time
    [Tags]  dev
    Open Report In Browser
    ${feature}=     Get Feature     Calculator
    Verify Feature Duration Not Zero    ${feature}
    ${feature}=     Get Feature     Controls
    Verify Feature Duration Not Zero    ${feature}
    ${feature}=     Get Feature     Cucuber basket
    Verify Feature Duration Not Zero    ${feature}

*** Keywords ***
Verify Feature Duration Not Zero
    [Arguments]    ${feature}
    ${text}=  Get Text     ${feature}/p
    ${text}=  Remove String     ${text}    Executed in      ms
    ${time}=  Convert To Number   ${text}
    ${zero}=  Convert To Number     0.0
    Should Not Be Equal As Numbers   ${time}    ${zero}
