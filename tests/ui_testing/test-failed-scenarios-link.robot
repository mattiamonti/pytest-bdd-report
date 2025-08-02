*** Settings ***
Library           SeleniumLibrary
Library           bdd_generator_library/BDDGeneratorLibrary.py
Library    ../../venv/lib/python3.12/site-packages/robot/libraries/XML.py
Resource    common.resource
Resource    generation.resource
Resource    resources/scenario.resource
Test Teardown    Custom Teardown

*** Variables ***
${BROWSER}    headlesschrome    #chrome
${mock_dir}    generated_bdd_cases_for_tests
${report_title}    generated_test
${modal}    xpath=//dialog
${modal_button}    xpath=//*[contains(@class, "failed-scenarios-link")]
${modal_close_button}    ${modal}//button[contains(@class, "modal-close")]

*** Test Cases ***
Failed Scenarios Link Should Be Present In Failed Feature
    Setup Report With Failed Scenario
    Element Should Be Visible    ${modal_button}

Failed Scenarios Link Should Not Be Present In Passed Feature
    Setup Report With Passed Scenario
    Element Should Not Be Visible    ${modal_button}

Open And Close Failed Scenarios Link Modal
    Setup Report With Failed Scenario
    Scroll Element Into View    ${modal_button}
    Click Element    ${modal_button}
    Wait Until Element Is Visible    ${modal}
    Click Element    ${modal_close_button}
    Wait Until Element Is Not Visible    ${modal}

Failed Scenarios Link Modal Should Contain All Failed Scenarios Of A Feature
    Setup Report With Multiple Failed Scenarios
    Scroll Element Into View    ${modal_button}
    Click Element    ${modal_button}
    ${links}=    Get WebElements    ${modal}//a
    @{expected_links}=    Create List    Test scenario 1    Test scenario 2    Test scenario 3
    ${current_links}=   Create List
    FOR    ${link}    IN    @{links}
        ${text}=    Get Text    ${link}
        Append To List   ${current_links}    ${text}
    END
    Should Be Equal    ${current_links}    ${expected_links}

Navigate To Failed Scenario From Failed Scenarios Link Modal
    Setup Report With Multiple Failed Scenarios
    Scroll Element Into View    ${modal_button}
    Click Element    ${modal_button}
    Click Element    ${modal}//a[contains(., "Test scenario 1")]
    Wait Until Element Is Not Visible    ${modal}
    ${scenario}=    scenario.Get Scenario    Test scenario 1
    Element Should Be Visible    ${scenario}

Navigate To Every Failed Scenario From Failed Scenarios Link Modal
    [Tags]    dev
    Setup Report With Multiple Failed Scenarios
    @{expected_links}=    Create List    Test scenario 1    Test scenario 2    Test scenario 3
    FOR    ${element}    IN    @{expected_links}
        Scroll Element Into View    ${modal_button}
        Click Element    ${modal_button}
        Click Element    ${modal}//a[contains(., "${element}")]
        Wait Until Element Is Not Visible    ${modal}
        ${scenario}=    scenario.Get Scenario    ${element}
        Element Should Be Visible    ${scenario}
        
    END


*** Keywords ***
Custom Teardown
    common.Remove Test Directory And Files    ${mock_dir}    ${report_title}

Setup Report With Failed Scenario
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

Setup Report With Multiple Failed Scenarios
    BDDGeneratorLibrary.Create Builder    ${mock_dir}
    BDDGeneratorLibrary.Create Feature    Test feature
    BDDGeneratorLibrary.Create Scenario   Test scenario 1
    BDDGeneratorLibrary.Add Failed Step   Step 1
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Create Scenario   Test scenario 2
    BDDGeneratorLibrary.Add Failed Step   Step 2
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Create Scenario   Test scenario 3
    BDDGeneratorLibrary.Add Failed Step   Step 3
    BDDGeneratorLibrary.Attach Scenario To Feature
    BDDGeneratorLibrary.Attach Feature To Builder
    BDDGeneratorLibrary.Build Tests 
    ${url}=    generation.Generate HTML Report From Directory    ${report_title}    ${mock_dir}
    common.Open Generated Report In Browser    ${url} 
    Wait Until Page Contains    ${report_title}


Setup Report With Passed Scenario
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