*** Settings ***
Library           SeleniumLibrary
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource    common.resource
Resource    generation.resource
Test Teardown    Custom Test Teardown

*** Variables ***
${BROWSER}    headlesschrome    #chrome
${mock_dir}    generated_bdd_cases_for_tests
${report_title}    generated_test

*** Test Cases ***
Verify a report with all tests passed in a feature
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    Generate Passed Scenario    name=Passato 1
    Generate Passed Scenario    name=Passato 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    Element Should Contain    ${element_plot_widget}    2 Total tests executed
    Element Should Contain    ${element_plot_widget}    2 Passed tests
    Element Should Contain    ${element_plot_widget}    0 Failed tests
    Element Should Contain    ${element_plot_widget}    0 Skipped tests
    common.Scenario Background Color Should Be    Passato 1    214, 240, 224
    common.Scenario Background Color Should Be    Passato 2    214, 240, 224

Verify a report with all tests failed in a feature
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    Generate Failed Scenario    name=Fallito 1
    Generate Failed Scenario    name=Fallito 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    Element Should Contain    ${element_plot_widget}    2 Total tests executed
    Element Should Contain    ${element_plot_widget}    0 Passed tests
    Element Should Contain    ${element_plot_widget}    2 Failed tests
    Element Should Contain    ${element_plot_widget}    0 Skipped tests
    common.Scenario Background Color Should Be    Fallito 1    249, 225, 229
    common.Scenario Background Color Should Be    Fallito 2    249, 225, 229

    
*** Keywords ***
Custom Test Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}

Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}

