*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library  String
Resource          common.resource
Resource    resources/scenario.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Failed scenario color
    ${scenario}=    scenario.Get Scenario    Sum of two numbers
    Element Style Should Be    ${scenario}    background-color   ${failed_scenario_rgb_color}

Skipped scenario color
    ${scenario}=    scenario.Get Scenario    Shutdown
    Element Style Should Be    ${scenario}    background-color   ${skipped_scenario_rgb_color}

Passed scenario color
    ${scenario}=    scenario.Get Scenario    Eating cucumbers
    Element Style Should Be    ${scenario}    background-color   ${passed_scenario_rgb_color}

Open failed scenario details
    ${scenario}=    scenario.Get Scenario    Sum of two numbers
    scenario.Toggle Error Message    Sum of two numbers
    Element Should Contain  ${scenario}   AssertionError

Close failed scenario details
    ${scenario}=    scenario.Get Scenario    Sum of two numbers
    scenario.Toggle Error Message    Sum of two numbers
    Element Should Contain  ${scenario}   AssertionError
    scenario.Toggle Error Message    Sum of two numbers
    Element Should Not Contain  ${scenario}   AssertionError

Check Passed Scenario Duration
    ${duration}=    scenario.Get Scenario Duration    Sum of a number
    ${zero}=  Convert To Number     0.0
    Should Not Be Equal As Numbers   ${duration}    ${zero}

Check Failed Scenario Duration
    ${duration}=    scenario.Get Scenario Duration    Sum of two numbers
    ${zero}=  Convert To Number     0.0
    Should Not Be Equal As Numbers   ${duration}    ${zero}

Check Skipped Scenario Duration
    ${duration}=    scenario.Get Scenario Duration    Shutdown
    ${zero}=  Convert To Number     0.0
    Should Be Equal As Numbers   ${duration}    ${zero}
