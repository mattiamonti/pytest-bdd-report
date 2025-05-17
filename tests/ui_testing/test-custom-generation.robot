*** Settings ***
Library           SeleniumLibrary
Library  OperatingSystem
Library    Collections
Library           bdd_generator_library/BDDGeneratorLibrary.py

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    Set Suite Variable    ${report_title}    RFTest
    ${url}=    Generate HTML Report    ${report_title}
    Open Browser    ${url}    ${BROWSER}
    Page Should Contain    ${report_title}

Generate HTML Report
    [Arguments]    ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}

*** Test Cases ***
Generate a report with all tests passed
    BDDGeneratorLibrary.Create Builder    mock/generated_tests
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
    