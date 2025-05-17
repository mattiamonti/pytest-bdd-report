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
Generate a report with all tests passed
    ${mock_dir}=    Set Variable    mock_generated_tests
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    BDDGeneratorLibrary.Create Scenario   Scenario misto
    BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
    BDDGeneratorLibrary.Add Failed Step   Step che fallisce
    BDDGeneratorLibrary.Add Skipped Step  Step skippato
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Secondo esempio
    BDDGeneratorLibrary.Create Scenario   Secondo scenario
    BDDGeneratorLibrary.Add Failed Step   Secondo step fallito
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    Generate HTML Report From Directory    MockGenRFTest    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    MockGenRFTest
    Remove Test Directory And Files    ${mock_dir}    MockGenRFTest

    