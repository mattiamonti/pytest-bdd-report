*** Settings ***
Library           SeleniumLibrary
Library  OperatingSystem
Library    Collections
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource    common.resource

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}

Generate HTML Report From Directory
    [Arguments]    ${title}    ${directory}
    Run    pytest --bdd-report="${title}" ${directory}
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}

Remove Test Directory And Files
    [Arguments]    ${path}    ${report_title}
    Remove Directory    ${path}    recursive=${True}
    Remove File    ${EXECDIR}/${report_title}.html
    Remove File    ${EXECDIR}/.cucumber-data.json

*** Test Cases ***
Verify a report with all tests passed
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    RF-Passed
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    BDDGeneratorLibrary.Create Scenario   Scenario passato
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Scenario   Secondo Scenario passato
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    ${report_title}
    Element Should Contain    xpath=//*[@id="passed"]    2
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

Verify a report with all tests failed
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    RF-Failed
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    BDDGeneratorLibrary.Create Scenario   Scenario fallito
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Add Failed Step   Step fallito
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Scenario   Secondo Scenario fallito
    BDDGeneratorLibrary.Add Failed Step   Step fallito
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    ${report_title}
    Element Should Contain    xpath=//*[@id="failed"]    2
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

    