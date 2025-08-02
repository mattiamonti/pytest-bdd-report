*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           String
Resource          common.resource
Resource          resources/step.resource
Library           bdd_generator_library/BDDGeneratorLibrary.py
Resource          generation.resource
Test Setup        common.Open Report In Browser
Test Teardown     common.Remove HTML Report   

*** Variables ***
${BROWSER}        headlesschrome    #chrome
@{PASSED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I press the add button  Then: The result should be 7 on the screen
@{FAILED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I enter the number 3 into the calculator  And: I press the add button  Then: The result should be 101 on the screen
${mock_dir}    generated_bdd_cases_for_tests
${report_title}    generated_test

*** Test Cases ***
Passed Scenario Has Steps
    ${steps}=   step.Get Scenario Steps     Sum of a number
    Should Not Be Empty    ${steps}

Failed Scenario Has Steps
    ${steps}=   step.Get Scenario Steps     Sum of two numbers
    Should Not Be Empty    ${steps}

Skipped Scenario Has No Steps
    ${steps}=   step.Get Scenario Steps     Shutdown
    Should Be Empty    ${steps}

Check Passed Scenario Steps
    ${steps}=   step.Get Scenario Steps     Sum of a number
    Should Be Equal     ${steps}    ${PASSED_STEPS}
    
Check Failed Scenario Steps
    ${steps}=   step.Get Scenario Steps     Sum of two numbers
    Should Be Equal     ${steps}    ${FAILED_STEPS}

Check Durations For Passed Scenario
    ${durations}=   step.Get Scenario Steps Duration     Sum of a number
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}

Check Durations For Failed Scenario
    ${durations}=   step.Get Scenario Steps Duration     Sum of two numbers
    ${zero}=    Convert To Number   0.0
    List Should Not Contain Value   ${durations}    ${zero}

Check Failed Steps After The First Failed
    Setup Report With Mixed Steps
    ${steps}=   step.Get Scenario Steps     Test scenario
    @{expected_steps}=    Create List    Given: Step 1    Given: Step 2    Given: Step 3    Given: Step 4    Given: Step 5
    Should Be Equal    ${steps}    ${expected_steps}
    step.Scenario Step Should Be Passed    Test scenario    Step 1
    step.Scenario Step Should Be Passed    Test scenario    Step 2
    step.Scenario Step Should Be Failed    Test scenario    Step 3
    step.Scenario Step Should Be Failed    Test scenario    Step 4
    step.Scenario Step Should Be Failed    Test scenario    Step 5
    Custom Teardown

Check All Step Failed
    Setup Report With Failed Steps
    ${steps}=   step.Get Scenario Steps     Test scenario
    FOR    ${step}    IN    @{steps}
        step.Scenario Step Should Be Failed    Test scenario    ${step}
    END
    Custom Teardown

Check All Step Failed
    Setup Report With Passed Steps
    ${steps}=   step.Get Scenario Steps     Test scenario
    FOR    ${step}    IN    @{steps}
        step.Scenario Step Should Be Passed    Test scenario    ${step}
    END
    Custom Teardown

*** Keywords ***
Setup Report With Passed Steps
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Test feature
    BDDGeneratorLibrary.Create Scenario   Test scenario
    BDDGeneratorLibrary.Add Passed Step   Step 1
    BDDGeneratorLibrary.Add Passed Step   Step 2
    BDDGeneratorLibrary.Add Passed Step   Step 3
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}

Setup Report With Failed Steps
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Test feature
    BDDGeneratorLibrary.Create Scenario   Test scenario
    BDDGeneratorLibrary.Add Failed Step   Step 1
    BDDGeneratorLibrary.Add Failed Step   Step 2
    BDDGeneratorLibrary.Add Failed Step   Step 3
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}

Setup Report With Mixed Steps
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Test feature
    BDDGeneratorLibrary.Create Scenario   Test scenario
    BDDGeneratorLibrary.Add Passed Step   Step 1
    BDDGeneratorLibrary.Add Passed Step   Step 2
    BDDGeneratorLibrary.Add Failed Step   Step 3
    BDDGeneratorLibrary.Add Passed Step   Step 4
    BDDGeneratorLibrary.Add Passed Step   Step 5
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}

Custom Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}