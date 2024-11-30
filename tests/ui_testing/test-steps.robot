*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem
Library  Collections
Library  String

*** Variables ***
${BROWSER}    headlesschrome    #chrome
@{PASSED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I press the add button  Then: The result should be 7 on the screen
@{FAILED_STEPS}   Given: I have a calculator  When: I enter the number 7 into the calculator  And: I enter the number 3 into the calculator  And: I press the add button  Then: The result should be 101 on the screen

*** Test Cases ***
Generate Report
    ${path}=    Generate HTML Report    RFTest
    VAR  ${URL}    ${path}   scope=SUITE

Passed scenario has steps 
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of a number"]/div
    Element Should Contain  ${feature}   Scenario: Sum of a number
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/div
    Should Not Be Empty     ${steps}

Failed scenario has steps 
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/div
    Should Not Be Empty     ${steps}

Skipped scenario has no steps 
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Shutdown"]/div
    Element Should Contain  ${feature}   Scenario: Shutdown
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/div
    Should Be Empty     ${steps}

Check passed scenario steps
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of a number"]/div
    Element Should Contain  ${feature}   Scenario: Sum of a number
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    Should Be Equal     ${current_steps}    ${PASSED_STEPS}

Check failed scenario steps
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/div
    ${current_steps}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           Append To List   ${current_steps}    ${text}
    END
    Should Be Equal     ${current_steps}    ${FAILED_STEPS}

Check passed scenario steps duration
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of a number"]/div
    Element Should Contain  ${feature}   Scenario: Sum of a number
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/p
    ${current_durations}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           ${text}=    Remove String   ${text}     ms
           ${duration}=     Convert To Number   ${text}
           Append To List   ${current_durations}    ${duration}
    END
    List Should Not Contain Value   ${current_durations}    0.0

Check failed scenario steps duration
    Open Browser  ${URL}  ${BROWSER}
    ${feature}=    Set Variable     xpath=//*[@id="Sum of two numbers"]/div
    Element Should Contain  ${feature}   Scenario: Sum of two numbers
    ${steps}=   Get Web Elements    ${feature}/div[2]/*[@class="step-container"]/p
    ${current_durations}=   Create List
    FOR    ${element}    IN    @{steps}
           ${text}=    Get Text    ${element}
           ${text}=    Remove String   ${text}     ms
           ${duration}=     Convert To Number   ${text}
           Append To List   ${current_durations}    ${duration}
    END
    List Should Not Contain Value   ${current_durations}    0.0

*** Keywords ***
Generate HTML Report
    [Arguments]     ${title}
    Run    pytest --bdd-report="${title}" sample_tests/sample_test_calculator.py sample_tests/sample_test_controllo.py sample_tests/sample_test_outline.py
    File Should Exist  ./${title}.html
    ${result}=  Set Variable    file://${EXECDIR}/${title}.html
    Log     ${result}
    RETURN    ${result}
