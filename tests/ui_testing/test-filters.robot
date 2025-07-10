*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Resource          common.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}    headlesschrome

*** Test Cases ***
Filters Must Be Checked
    Checkbox Should Be Selected    id:show-passed
    Checkbox Should Be Selected    id:show-skipped
    Checkbox Should Be Selected    id:show-failed

Filter Out The Passed Scenarios
    Scroll To Filters
    Click Element    xpath=//label[@for="show-passed"]
    Element Should Be Visible    class:skipped-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:passed-scenario

Filter Out The Skipped Scenarios
    Scroll To Filters
    Click Element    xpath=//label[@for="show-skipped"]
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:skipped-scenario

Filter Out The Failed Scenarios
    Scroll To Filters
    Click Element    xpath=//label[@for="show-failed"]
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:skipped-scenario
    Element Should Not Be Visible    class:failed-scenario


*** Keywords ***
Scroll To Filters
    Wait Until Page Contains Element    id:filters
    Scroll Element Into View    id:filters
