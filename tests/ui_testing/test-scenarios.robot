*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Generate Report
    [Tags]  dev
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

Open failed scenario details
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${button}=    Set Variable      xpath=//*[@id="Sum of two numbers"]/div/button
    Click Button   ${button} 
    Element Should Contain  ${feature}   AssertionError
    ${style_result}=     Get Element Attribute   ${button}     style
    Should Contain    ${style_result}    rotate(0deg)

Close failed scenario details
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${button}=    Set Variable      xpath=//*[@id="Sum of two numbers"]/div/button
    Click Button     ${button} 
    Element Should Contain  ${feature}   AssertionError
    Click Button     ${button} 
    ${style_result}=     Get Element Attribute   ${button}     style
    Should Contain    ${style_result}    rotate(-90deg)
    Element Should Not Contain  ${feature}   AssertionError

Check tooltip for opening and closing scenario details
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${button}=    Set Variable      xpath=//*[@id="Sum of two numbers"]/div/button
    Element Attribute Value Should Be  ${button}   title    Open error message
    Click Button   ${button} 
    Element Should Contain  ${feature}   AssertionError
    Element Attribute Value Should Be  ${button}   title    Close error message
   

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
