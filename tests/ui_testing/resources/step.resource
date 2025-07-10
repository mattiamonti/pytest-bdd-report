*** Settings ***
Library    SeleniumLibrary
Library    String
Library    ../../../venv/lib/python3.12/site-packages/robot/libraries/XML.py
Resource    ../common.resource
Resource    scenario.resource

*** Keywords ***
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

Get Scenario Steps Duration
    [Documentation]    Return the list of step's durations of the scenario
    [Arguments]    ${scenario_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    ${steps}=    Get Web Elements    ${scenario}//*[@data-testid="step-duration"]
    ${current_durations}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           ${text}=    Remove String   ${text}     ms
           ${duration}=     Convert To Number   ${text}
           Append To List   ${current_durations}    ${duration}
    END
    RETURN    ${current_durations}

Scenario Step Should Be Failed
    [Arguments]    ${scenario_name}    ${step_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    Page Should Contain Element    ${scenario}//*[@data-testid="step-failed"]//p[contains(.,"${step_name}")]

Scenario Step Should Be Passed
    [Arguments]    ${scenario_name}    ${step_name}
    ${scenario}=    Get Scenario    ${scenario_name}
    Page Should Contain Element    ${scenario}//*[@data-testid="step-passed"]//p[contains(.,"${step_name}")]