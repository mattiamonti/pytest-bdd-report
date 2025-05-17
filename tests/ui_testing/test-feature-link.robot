*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String
Resource          common.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}        headlesschrome    #chrome

*** Test Cases ***
View Failed Feature By Link
    Click Feature Link In Feature Statistics     2
    Wait Until Element Is Visible   id:Calculator

View Skipped Feature By Link
    Click Feature Link In Feature Statistics     3
    Wait Until Element Is Visible   id:Controls

View Passed Feature By Link
    Click Feature Link In Feature Statistics     4
    Wait Until Element Is Visible   id:Cucuber basket

*** Keywords ***
Click Feature Link In Feature Statistics
    [Arguments]     ${row_number}
    Click Link    xpath=//*[@id="feature-statistics"]/table/tbody/tr[${row_number}]/td[1]/a



