*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Filter Out The Passed Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    id:show-passed
    Wait Until Page Does Not Contain  class:passed-scenario

Filter Out The skipped Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    id:show-skipped
    Wait Until Page Does Not Contain  class:skipped-scenario

Filter Out The Failed Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Click Button    id:show-failed
    Wait Until Page Does Not Contain  class:failed-scenario

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
