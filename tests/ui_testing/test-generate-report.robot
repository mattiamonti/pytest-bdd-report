*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Report Title
    Open Browser  ${URL}  ${BROWSER}
    Sleep   0.5s
    Wait Until Page Contains     Test report: RFTest.html

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
