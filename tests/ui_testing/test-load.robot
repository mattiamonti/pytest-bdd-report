*** Settings ***
Library           SeleniumLibrary
Library  OperatingSystem
Library    Collections
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource    common.resource
# TODO aggiungere test teardown per rimuovere i file, non ci devono essere variabili?

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Verify Report Renders Many Scenarios
    [Template]    Test Counting Scenario Elements
    1
    10
    100
    1000
    5000

Verify Report Renders Many Features
    [Template]    Test Counting Feature Elements
    1
    10
    100
    1000
    5000

Verify Report Renders Many Steps
    [Tags]    dev
    [Template]    Test Counting Step Elements
    1
    10
    100
    1000
    5000
    

*** Keywords ***
Test Counting Scenario Elements
    [Arguments]    ${expected_count}
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    Load-test-scenarios
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    FOR    ${i}    IN RANGE    0    ${expected_count}
        BDDGeneratorLibrary.Create Scenario   Scenario ${i}
        BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
        BDDGeneratorLibrary.Attach Scenario To Feature
    END
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    Generate Report And Open It    ${report_title}    ${mock_dir}
    ${actual_count}=    common.Count Scenarios In Report
    Log    Trovati ${actual_count} elementi, attesi: ${expected_count}
    # TODO migliroare gestione log solo se check sotto fallisce, magari metter in una keyword
    Should Be Equal As Integers    ${actual_count}    ${expected_count}
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

Test Counting Feature Elements
    [Arguments]    ${expected_count}
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    Load-test-features
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    FOR    ${i}    IN RANGE    0    ${expected_count}
        BDDGeneratorLibrary.Create Feature    FEATURE DI CARICO ${i}
        BDDGeneratorLibrary.Create Scenario   Scenario ${i}
        BDDGeneratorLibrary.Add Passed Step   Step passato correttamente
        BDDGeneratorLibrary.Attach Scenario To Feature
        BDDGeneratorLibrary.Attach Feature To Builder
    END
    BDDGeneratorLibrary.Build Tests 
    Generate Report And Open It    ${report_title}    ${mock_dir}
    ${actual_count}=    common.Count Feature In Report    feature_id_to_search_for=FEATURE DI CARICO
    Log    Trovati ${actual_count} elementi, attesi: ${expected_count}
    Should Be Equal As Integers    ${actual_count}    ${expected_count}
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

Test Counting Step Elements
    [Arguments]    ${expected_count}
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    Load-test-steps
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature per test di carico steps
    BDDGeneratorLibrary.Create Scenario   Scenario per test di carico steps
    FOR    ${i}    IN RANGE    0    ${expected_count}
        BDDGeneratorLibrary.Add Passed Step   Step di carico ${i}
    END
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    Generate Report And Open It    ${report_title}    ${mock_dir}
    ${actual_count}=    common.Count Steps In Report 
    Log    Trovati ${actual_count} elementi, attesi: ${expected_count}
    Should Be Equal As Integers    ${actual_count}    ${expected_count}
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

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

Generate Report And Open It
    [Arguments]    ${report_title}    ${mock_dir}
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    ${report_title}