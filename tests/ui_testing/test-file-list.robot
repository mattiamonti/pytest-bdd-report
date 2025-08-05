*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Resource          common.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}        headlesschrome    #chrome
${test_file_uri}=    xpath=//*[@id="test-file-uri"]
${test_file_uri_list}=    xpath=//*[@id="test-file-uri"]/div

*** Test Cases ***
Open File list
    Click File List Accordion
    Wait Until Element Is Visible  ${test_file_uri_list}

Close File list
    Click File List Accordion
    Wait Until Element Is Visible  ${test_file_uri_list}
    Click File List Accordion
    Wait Until Element Is Visible  ${test_file_uri_list}

*** Keywords ***
Click File List Accordion
    Click Element    ${test_file_uri}




