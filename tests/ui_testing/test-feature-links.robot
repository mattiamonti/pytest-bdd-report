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
    Click Link    xpath=//*[@id="feature-statistics"]/table/tbody/tr[3]/td[1]/a
    Wait Until Page Contains Element  id:Cucuber basket

Link To Feature Statistics
    Open Browser  ${URL}  ${BROWSER}
    Click Link    id:feature-statistics-button
    Wait Until Page Contains Element  id:feature-statistics

Open File list
    Open Browser  ${URL}  ${BROWSER}
    Click Button    xpath:/html/body/div[1]/div[2]/div[1]/button
    Wait Until Element Is Visible  id:test-file-uri

Close File list
    Open Browser  ${URL}  ${BROWSER}
    Click Button    xpath:/html/body/div[1]/div[2]/div[1]/button
    Wait Until Element Is Visible  id:test-file-uri
    Click Button    xpath:/html/body/div[1]/div[2]/div[1]/button
    Wait Until Element Is Not Visible  id:test-file-uri

Open Failed Scenario Error Message
    Open Browser  ${URL}  ${BROWSER}
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Element Is Visible  id:message-Sum of two numbers

Close Failed Scenario Error Message
    Open Browser  ${URL}  ${BROWSER}
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Element Is Visible  id:message-Sum of two numbers
    Click Button    xpath://*[@id="Sum of two numbers"]/div/button
    Wait Until Element Is Not Visible  id:message-Sum of two numbers

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
