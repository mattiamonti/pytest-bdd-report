*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library    Collections
Library    ../../venv/lib/python3.12/site-packages/robot/libraries/XML.py

*** Variables ***
${BROWSER}    headlesschrome    #chrome
${element_plot_widget}=    xpath=/html/body/div[2]/div/div[1]
${passed_scenario_rgb_color}    220, 252, 231
${failed_scenario_rgb_color}    254, 226, 226





*** Keywords ***
Open Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    Set Suite Variable    ${report_title}    RFTest
    ${url}=    Generate HTML Report    ${report_title}
    Open Browser    ${url}    ${BROWSER}
    Page Should Contain    ${report_title}

Open Generated Report In Browser
    [Documentation]    Opens the browser and navigates to the target URL.
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}

Generate HTML Report
    [Arguments]    ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist    ./${title}.html
    ${result}=    Set Variable    file://${EXECDIR}/${title}.html
    Log    Generated report at: ${result}
    RETURN    ${result}

Remove HTML Report
    Remove File    ${EXECDIR}/${report_title}.html
    Remove File    ${EXECDIR}/.cucumber-data.json

Remove Test Directory And Files
    [Arguments]    ${path}    ${report_title}
    Remove Directory    ${path}    recursive=${True}
    Remove File    ${EXECDIR}/${report_title}.html
    Remove File    ${EXECDIR}/.cucumber-data.json

Get Feature
    [Arguments]    ${feature_name}
    ${feature}=    Set Variable    xpath=//*[@id="${feature_name}"]/div[1]
    Element Should Contain    ${feature}    Feature: ${feature_name}
    RETURN   ${feature}

Get Feature Scenarios
    [Arguments]    ${feature_name}
    ${scenarios}=    Get Web Elements    xpath=//*[@id="${feature_name}"]/div[2]/div
    RETURN    ${scenarios}

Get Scenario
    [Arguments]    ${scenario_name}
    ${scenario}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div
    Element Should Contain    ${scenario}    Scenario: ${scenario_name}
    RETURN   ${scenario}

Get Scenario Details Button
    [Arguments]    ${scenario_name}
    ${button}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div/button
    Element Should Be Visible   ${button}
    RETURN  ${button}

Get Scenario Steps
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    RETURN  ${current_steps}

Scenario Background Color Should Be
    [Arguments]    ${scenario_name}    ${rgb_color_code}
    [Documentation]    Example: Scenario Background Color Should Be    NomeScenario    214, 240, 224
    ${stile_scenario}=    SeleniumLibrary.Get Element Attribute    xpath=//*[@id="${scenario_name}"]/div    style
    Should Be True    "rgb(${rgb_color_code})" in "${stile_scenario}"

Element Tooltip Should Be
    [Arguments]     ${element}   ${text}
    Element Attribute Value Should Be  ${element}   title    ${text}
    
Element Style Should Contain
    [Arguments]     ${element}   ${text}
    ${style_result}=     SeleniumLibrary.Get Element Attribute   ${element}     style
    Should Contain    ${style_result}    ${text}

Count Scenarios In Report
    ${general_scenario_xpath}=    Set Variable    xpath=//div[contains(@class, "scenario-container")]
    ${elements}=    Get WebElements    ${general_scenario_xpath}
    ${count}=       Get Length         ${elements}
    RETURN        ${count}

Count Steps In Report
    ${general_scenario_xpath}=    Set Variable    xpath=//div[contains(@class, "step")]
    ${elements}=    Get WebElements    ${general_scenario_xpath}
    ${count}=       Get Length         ${elements}
    RETURN        ${count}

Count Feature In Report
    [Arguments]    ${feature_id_to_search_for}=${EMPTY}
    IF    '${feature_id_to_search_for}' == '${EMPTY}'
        ${general_scenario_xpath}=    Set Variable    xpath=//div[contains(@id, "Feature")]
    ELSE
        ${general_scenario_xpath}=    Set Variable    xpath=//div[contains(@id, "${feature_id_to_search_for}")]
    END
    ${elements}=    Get WebElements    ${general_scenario_xpath}
    ${count}=       Get Length         ${elements}
    RETURN        ${count}

Check Report Statistics
    [Arguments]    ${total_executed}=0    ${total_passed}=0    ${total_failed}=0    ${total_skipped}=0
    Element Should Contain    xpath=//*[@data-testid="tests-executed"]    ${total_executed}
    Element Should Contain    xpath=//*[@data-testid="tests-passed"]    ${total_passed}
    Element Should Contain    xpath=//*[@data-testid="tests-failed"]    ${total_failed}
    Element Should Contain    xpath=//*[@data-testid="tests-skipped"]    ${total_skipped}