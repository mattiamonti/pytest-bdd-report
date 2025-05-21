*** Settings ***
Library           SeleniumLibrary
Library  OperatingSystem
Library    Collections
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource    common.resource

*** Variables ***
${BROWSER}    headlesschrome    #chrome

*** Test Cases ***
Verify a report with all tests passed in a feature
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    RF-Passed
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    Generate Passed Scenario    name=Passato 1
    Generate Passed Scenario    name=Passato 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    ${report_title}
    Element Should Contain    ${element_plot_widget}    2 Total tests executed
    Element Should Contain    ${element_plot_widget}    2 Passed tests
    Element Should Contain    ${element_plot_widget}    0 Failed tests
    Element Should Contain    ${element_plot_widget}    0 Skipped tests
    common.Scenario Background Color Should Be    Passato 1    214, 240, 224
    common.Scenario Background Color Should Be    Passato 2    214, 240, 224
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

Verify a report with all tests failed in a feature
    ${mock_dir}=    Set Variable    mock_generated_tests
    ${report_title}=    Set Variable    RF-Failed
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    Generate Failed Scenario    name=Fallito 1
    Generate Failed Scenario    name=Fallito 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Page Should Contain    ${report_title}
    Element Should Contain    ${element_plot_widget}    2 Total tests executed
    Element Should Contain    ${element_plot_widget}    0 Passed tests
    Element Should Contain    ${element_plot_widget}    2 Failed tests
    Element Should Contain    ${element_plot_widget}    0 Skipped tests
    common.Scenario Background Color Should Be    Fallito 1    249, 225, 229
    common.Scenario Background Color Should Be    Fallito 2    249, 225, 229
    Remove Test Directory And Files    ${mock_dir}    ${report_title}

    
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

Generate Passed Scenario
    [Arguments]    ${name}=${EMPTY}
    [Documentation]    The keyword generate a passed BDD scenario and attach it to the feature and the builder
    Run Keyword If    "${name}" == "${EMPTY}"
    ...    BDDGeneratorLibrary.Create Scenario   Scenario passato
    ...  ELSE
    ...    BDDGeneratorLibrary.Create Scenario   ${name}
    BDDGeneratorLibrary.Add Passed Step   Step 1 passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step 2 passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step 3 passato correttamente
    BDDGeneratorLibrary.Attach Scenario To Feature

Generate Failed Scenario
    [Arguments]    ${name}=${EMPTY}
    [Documentation]    The keyword generate a failed BDD scenario and attach it to the feature and the builder
    Run Keyword If    "${name}" == "${EMPTY}"
    ...    BDDGeneratorLibrary.Create Scenario   Scenario fallito
    ...  ELSE
    ...    BDDGeneratorLibrary.Create Scenario   ${name}
    BDDGeneratorLibrary.Add Passed Step   Step 1 passato correttamente
    BDDGeneratorLibrary.Add Passed Step   Step 2 passato correttamente
    BDDGeneratorLibrary.Add Failed Step   Step 3 fallito
    BDDGeneratorLibrary.Attach Scenario To Feature