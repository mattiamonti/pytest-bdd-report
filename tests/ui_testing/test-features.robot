*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library  String
Resource    common.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Feature with failed scenarios
    ${feature}=  Get Feature     Calculator
    Element Should Contain  ${feature}   Description: As an user i want to use the calculator app
    Element Should Contain  ${feature}   sample_features/calculator.feature
    Element Should Contain  ${feature}/div/div/div/p[2]     1

Feature with skipped scenarios
    ${feature}=  Get Feature     Controls
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/controllo.feature
    Element Should Contain  ${feature}/div/div/div/p[2]   2

Feature with passed scenarios
    ${feature}=  Get Feature     Cucuber basket
    Element Should Not Contain  ${feature}   Description:
    Element Should Contain  ${feature}   sample_features/scenario_outlines.feature
    Element Should Contain  ${feature}/div/div/div/p   2

Feature With Passed Template Scenarios
    ${feature}=  Get Feature     Cucuber basket
    Element Should Contain  ${feature}/div/div/div/p   2
    ${scenarios}=   Get Feature Scenarios   Cucuber basket
    FOR    ${scenario}    IN    @{scenarios}
        ${class}=  SeleniumLibrary.Get Element Attribute    ${scenario}    class
        Should Contain   ${class}    passed
    END

Check Features Execution Time
    [Tags]  dev
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
