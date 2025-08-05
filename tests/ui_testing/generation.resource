*** Settings ***
Library           bdd_generator_library/BDDGeneratorLibrary.py
Library  OperatingSystem


*** Keywords ***
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

Generate Skipped Scenario
    [Arguments]    ${name}=${EMPTY}
    [Documentation]    The keyword generate a skipped BDD scenario and attach it to the feature and the builder
    Run Keyword If    "${name}" == "${EMPTY}"
    ...    BDDGeneratorLibrary.Create Scenario   Scenario skippato
    ...  ELSE
    ...    BDDGeneratorLibrary.Create Scenario   ${name}
    BDDGeneratorLibrary.Add Passed Step   Step 1 passato correttamente
    BDDGeneratorLibrary.Add Skipped Step    Step 2 skippato
    BDDGeneratorLibrary.Attach Scenario To Feature

Generate HTML Report From Directory
    [Arguments]    ${title}    ${directory}
    Run    pytest --bdd-report="${title}" ${directory}
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}