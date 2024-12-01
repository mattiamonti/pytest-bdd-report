*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Resource          common.robot
Resource    step_keywords.robot

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Failed scenario color
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of two numbers
    Element Style Should Contain    ${scenario}   rgb(249, 225, 229)

Skipped scenario color
    Open Report In Browser
    ${scenario}=    Get Scenario    Shutdown
    Element Style Should Contain    ${scenario}   rgb(255, 248, 231)

Passed scenario color
    Open Report In Browser
    ${scenario}=    Get Scenario    Eating cucumbers
    Element Style Should Contain    ${scenario}   rgb(214, 240, 224)

Open failed scenario details
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of two numbers
    ${button}=   Get Scenario Details Button    Sum of two numbers 
    Click Button   ${button} 
    Element Should Contain  ${scenario}   AssertionError
    Element Style Should Contain    ${button}   rotate(0deg)

Close failed scenario details
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of two numbers
    ${button}=   Get Scenario Details Button    Sum of two numbers 
    Click Button     ${button} 
    Element Should Contain  ${scenario}   AssertionError
    Click Button     ${button} 
    Element Style Should Contain    ${button}   rotate(-90deg)
    Element Should Not Contain  ${scenario}   AssertionError

Check tooltip for opening and closing scenario details
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of two numbers
    ${button}=   Get Scenario Details Button    Sum of two numbers 
    Element Tooltip Should Be   ${button}   Open error message 
    Click Button   ${button} 
    Element Should Contain  ${scenario}   AssertionError
    Element Tooltip Should Be   ${button}   Close error message 
   
*** Keywords ***
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



