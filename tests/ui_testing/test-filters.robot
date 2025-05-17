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
    Click Button    id:show-passed
    Element Should Be Visible    class:skipped-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:passed-scenario

Filter Out The Skipped Scenarios
    Click Button    id:show-skipped
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:failed-scenario
    Element Should Not Be Visible    class:skipped-scenario

Filter Out The Failed Scenarios
    Click Button    id:show-failed
    Element Should Be Visible    class:passed-scenario
    Element Should Be Visible    class:skipped-scenario
    Element Should Not Be Visible    class:failed-scenario
