*** Settings ***
Library           SeleniumLibrary
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource          generation.resource
Resource          common.resource
Test Setup        Custom Test Setup
Test Teardown     Custom Test Teardown

*** Variables ***
${BROWSER}        headlesschrome    #chrome
${mock_dir}    generated_bdd_cases_for_tests
${report_title}    generated_test

*** Test Cases ***
View Failed Feature By Link
    Click Feature Link In Feature Table    Failed feature
    Wait Until Element Is Visible   id:Failed feature

View Skipped Feature By Link
    Click Feature Link In Feature Table    Skipped feature
    Wait Until Element Is Visible   id:Skipped feature

View Passed Feature By Link
    Click Feature Link In Feature Table    Passed feature
    Wait Until Element Is Visible   id:Passed feature

*** Keywords ***
Click Feature Link In Feature Table
    [Arguments]     ${feature_name}
    ${feature_row}=    Set Variable    xpath=//tr[contains(@data-testid, "feature-table-row-for-${feature_name}")]
    Scroll Element Into View    ${feature_row}
    Click Link    ${feature_row}/td[1]/a

Custom Test Setup
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Skipped feature
    Generate Passed Scenario    name=Passed scenario skipped feature
    Generate Skipped Scenario    name=Skipped scenario
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Passed feature
    Generate Passed Scenario    name=Passed scenario
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Failed feature
    Generate Failed Scenario    name=Failed scenario
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}


Custom Test Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}