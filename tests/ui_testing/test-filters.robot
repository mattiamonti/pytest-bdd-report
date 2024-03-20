*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${BROWSER}    headlesschrome

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Filters Must Be Checked
    Open Browser  ${URL}  ${BROWSER}
    Checkbox Should Be Selected    id:show-passed
    Checkbox Should Be Selected    id:show-skipped
    Checkbox Should Be Selected    id:show-failed

Filter Out The Passed Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Click Button    id:show-passed
    Element Should Be Visible    class:skipped-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:passed-scenario

Filter Out The Skipped Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Click Button    id:show-skipped
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:skipped-scenario

Filter Out The Failed Scenarios
    Open Browser  ${URL}  ${BROWSER}
    Click Button    id:show-failed
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:skipped-scenario
    Element Should Not Be Visible    class:failed-scenario

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
