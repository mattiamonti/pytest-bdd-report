*** Settings ***
Library    SeleniumLibrary
Library    String
Resource    ../common.resource


*** Keywords ***
Get Scenario
    [Documentation]    Get the scenario element
    [Arguments]    ${scenario_name}
    ${scenario}=    Set Variable    xpath=//*[@id="${scenario_name}"]/div
    Element Should Contain    ${scenario}    ${scenario_name}
    RETURN   ${scenario}

Get Scenario Steps
    [Documentation]    Get the steps of the scenario
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    RETURN  ${current_steps}
Toggle Error Message
    [Documentation]
    ...    Expand the error message of the scenario.
    ...    If the error message is open, it closes it
    [Arguments]    ${scenario_name}
    ${details_button}=    Get Scenario Details Button    ${scenario_name}
    Expand Scenario Details    ${details_button}

Get Scenario Details Button
    [Arguments]    ${scenario_name}
    ${xpath}=    Set Variable    xpath=//*[@id="${scenario_name}"]//details
    RETURN    ${xpath}


Expand Scenario Details
    [Arguments]    ${button}
    Scroll Element Into View    ${button}
    Element Should Be Visible   ${button}
    Click Element    ${button}

Get Scenario Duration
    [Documentation]    Return the duration of the scenario
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    ${text}=  Get Text    ${scenario}//*[@data-testid="scenario-duration"] 
    ${text}=  Remove String     ${text}    Executed in      ms
    ${duration}=  Convert To Number   ${text}
    RETURN    ${duration}