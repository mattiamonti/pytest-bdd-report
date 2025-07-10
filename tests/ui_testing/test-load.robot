*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    bdd_generator_library/BDDGeneratorLibrary.py
Resource    common.resource
Test Teardown    Custom Test Teardown

*** Variables ***
${BROWSER}    headlesschrome    #chrome
${mock_dir}    generated_bdd_cases_for_tests
${report_title}    generated_test

*** Test Cases ***
Verify Report Renders Many Scenarios
    [Tags]    dev
    [Template]    Test Counting Scenario Elements
    1
    10
    100
    1000

Verify Report Renders Many Features
    [Template]    Test Counting Feature Elements
    1
    10
    100
    1000

Verify Report Renders Many Steps
    [Template]    Test Counting Step Elements
    1
    10
    100
    1000
    

*** Keywords ***
Test Counting Scenario Elements
    [Arguments]    ${expected_count}
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
    Should Be Equal As Integers    ${actual_count}    ${expected_count}

Test Counting Feature Elements
    [Arguments]    ${expected_count}
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

Test Counting Step Elements
    [Arguments]    ${expected_count}
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

Custom Test Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}

Generate HTML Report From Directory
    [Arguments]    ${title}    ${directory}
    Run    pytest --bdd-report="${title}" ${directory}
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}

Generate Report And Open It
    [Arguments]    ${report_title}    ${mock_dir}
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Page Should Contain    ${report_title}