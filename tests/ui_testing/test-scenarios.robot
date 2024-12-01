*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library  String
Resource          common.resource

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
   
Check Passed Scenario Duration
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of a number
    Verify Scenario Duration Not Zero   ${scenario}

Check Failed Scenario Duration
    Open Report In Browser
    ${scenario}=    Get Scenario    Sum of two numbers
    Verify Scenario Duration Not Zero   ${scenario}

Check Skipped Scenario Duration
    Open Report In Browser
    ${scenario}=    Get Scenario    Shutdown
    Verify Scenario Duration Is Zero   ${scenario}

*** Keywords ***
Verify Scenario Duration Not Zero
    [Arguments]    ${scenario}
    ${text}=  Get Text     ${scenario}/div[1]/p
    ${text}=  Remove String     ${text}    Executed in      ms
    ${time}=  Convert To Number   ${text}
    ${zero}=  Convert To Number     0.0
    Should Not Be Equal As Numbers   ${time}    ${zero}

Verify Scenario Duration Is Zero
    [Arguments]    ${scenario}
    ${text}=  Get Text     ${scenario}/div[1]/p
    ${text}=  Remove String     ${text}    Executed in      ms
    ${time}=  Convert To Number   ${text}
    ${zero}=  Convert To Number     0.0
    Should Be Equal As Numbers   ${time}    ${zero}



