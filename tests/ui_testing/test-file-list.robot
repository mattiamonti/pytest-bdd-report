*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Resource          common.resource
Test Setup        Open Report In Browser

*** Variables ***
${BROWSER}        headlesschrome    #chrome

*** Test Cases ***
Open File list
    Click File List Accordion
    Wait Until Element Is Visible  id:test-file-uri

Close File list
    Click File List Accordion
    Wait Until Element Is Visible  id:test-file-uri
    Click File List Accordion
    Wait Until Element Is Not Visible  id:test-file-uri

*** Keywords ***
Click File List Accordion
    Click Button    xpath:/html/body/div[1]/div[2]/div[1]/button



