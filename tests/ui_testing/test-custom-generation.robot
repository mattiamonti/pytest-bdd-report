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
    common.Check Plot Widget Statistics   total_executed=2    total_passed=2 
    common.Scenario Background Color Should Be    Passato 1    ${passed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Passato 2    ${passed_scenario_rgb_color}

Verify a report with all tests passed in multiple features
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature A
    Generate Passed Scenario    name=Passato 1
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Feature B
    Generate Passed Scenario    name=Passato 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics   total_executed=2    total_passed=2 
    common.Scenario Background Color Should Be    Passato 1    ${passed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Passato 2    ${passed_scenario_rgb_color}

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
    common.Check Plot Widget Statistics    total_executed=2    total_failed=2
    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Fallito 2    ${failed_scenario_rgb_color}

Verify a report with all tests failed in multiple features
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature A
    Generate Failed Scenario    name=Fallito 1
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Feature B
    Generate Failed Scenario    name=Fallito 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics    total_executed=2    total_failed=2
    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Fallito 2    ${failed_scenario_rgb_color}
    
Verify a report with all tests skipped in a feature
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature di esempio
    Generate Skipped Scenario    name=Skipped 1
    Generate Skipped Scenario    name=Skipped 2
    Generate Passed Scenario    name=Passato 3
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics    total_executed=3    total_skipped=2    total_passed=1
#    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
#    common.Scenario Background Color Should Be    Fallito 2    ${failed_scenario_rgb_color}

Verify a report with all tests skipped in multiple features
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature A
    Generate Skipped Scenario    name=Skipped 1
    Generate Passed Scenario    name=Passato 1
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Feature B
    Generate Skipped Scenario    name=Skipped 2
    Generate Passed Scenario    name=Passato 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics    total_executed=4    total_skipped=2    total_passed=2
#    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
#    common.Scenario Background Color Should Be    Fallito 2    ${failed_scenario_rgb_color}

Verify a report with passed and failed in a feature
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature A
    Generate Failed Scenario    name=Fallito 1
    Generate Passed Scenario    name=Passato 1
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics    total_executed=2    total_failed=1    total_passed=1
    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Passato 1    ${passed_scenario_rgb_color}

Verify a report with passed and failed in multiple features
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Feature A
    Generate Failed Scenario    name=Fallito 1
    Generate Passed Scenario    name=Passato 1
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Create Feature    Feature B
    Generate Passed Scenario    name=Passato 2
    Generate Failed Scenario    name=Fallito 2
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    Open Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}
    common.Check Plot Widget Statistics    total_executed=4    total_failed=2    total_passed=2
    common.Scenario Background Color Should Be    Fallito 1    ${failed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Fallito 2    ${failed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Passato 1    ${passed_scenario_rgb_color}
    common.Scenario Background Color Should Be    Passato 2    ${passed_scenario_rgb_color}

*** Keywords ***
Custom Test Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}

Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}

