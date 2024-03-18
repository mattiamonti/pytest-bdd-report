*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Link To A Feature
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Link    xpath=//*[@id="feature-statistics"]/table/tbody/tr[4]/td[1]/a
    Wait Until Page Contains Element  id:Cucuber basket

Link To Feature Statistics
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Link    id:feature-statistics-button
    Wait Until Page Contains Element  id:feature-statistics

File list
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    xpath:/html/body/div[1]/div[2]/div[1]/button
    Wait Until Page Contains Element  id:test-file-uri

Open Failed Scenario Error Message
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Page Contains Element  id:message-Sum of two numbers

Close Failed Scenario Error Message
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Page Contains Element  id:message-Sum of two numbers
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Page Does Not Contain  id:message-Sum of two numbers

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
