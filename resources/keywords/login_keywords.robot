*** Settings ***
Documentation    Keywords reutilizables para manejo de login en SIESA ERP - LOGICA DE CLAUDE
Resource         ../../config/settings_improved.robot
Resource         ../locators/siesa_locators.robot
Library          SeleniumLibrary
Library          DateTime

*** Keywords ***
Setup Browser
    [Documentation]    Configura y abre el navegador con configuraciones optimizadas
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Implicit Wait    ${IMPLICIT_WAIT}

Wait For Login Page
    [Documentation]    EXACTAMENTE como Claude - solo espera elementos
    Wait Until Element Is Visible    ${LOGIN_USER_FIELD}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${LOGIN_PASSWORD_FIELD}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${LOGIN_SUBMIT_BUTTON}    timeout=${TIMEOUT}

Perform Login
    [Documentation]    EXACTAMENTE como Claude funciona
    [Arguments]    ${username}    ${password}

    Wait Until Element Is Visible    ${LOGIN_USER_FIELD}    timeout=${TIMEOUT}
    Input Text    ${LOGIN_USER_FIELD}    ${username}

    Wait Until Element Is Visible    ${LOGIN_PASSWORD_FIELD}    timeout=${TIMEOUT}
    Input Text    ${LOGIN_PASSWORD_FIELD}    ${password}

    Wait Until Element Is Visible    ${LOGIN_SUBMIT_BUTTON}    timeout=${TIMEOUT}
    Click Element    ${LOGIN_SUBMIT_BUTTON}

Verify Login Success
    [Documentation]    EXACTAMENTE como Claude - usando el XPath especifico que funciona
    ${ELEMENTO_CONFIRMACION}=    Set Variable    //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]
    Wait Until Element Is Visible    ${ELEMENTO_CONFIRMACION}    timeout=${TIMEOUT}
    Log    Login exitoso - Elemento de confirmacion encontrado
    Capture Page Screenshot    login_exitoso.png

Verify Login Error
    [Documentation]    Verifica errores como Claude
    [Arguments]    ${expected_error}=any

    ${required_fields_error}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${ERROR_REQUIRED_FIELDS}    timeout=5s

    ${invalid_credentials_error}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${ERROR_INVALID_CREDENTIALS}    timeout=5s

    ${error_type}=    Set Variable If
    ...    ${required_fields_error}    required_fields
    ...    ${invalid_credentials_error}    invalid_credentials
    ...    no_error

    Run Keyword If    '${expected_error}' != 'any'
    ...    Should Be Equal    ${error_type}    ${expected_error}

    RETURN    ${error_type}

Close Notification If Present
    [Documentation]    Cierra notificaciones de error si estan presentes
    ${notification_present}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${NOTIFICATION_CLOSE}    timeout=2s

    Run Keyword If    ${notification_present}
    ...    Click Element    ${NOTIFICATION_CLOSE}

    Sleep    1s

Take Screenshot With Timestamp
    [Documentation]    Toma captura de pantalla con timestamp unico
    [Arguments]    ${base_name}

    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${screenshot_name}=    Set Variable    ${base_name}_${timestamp}.png
    Capture Page Screenshot    ${screenshot_name}
    RETURN    ${screenshot_name}

Complete Login Flow
    [Documentation]    Flujo completo de login (setup + login + verificacion)
    [Arguments]    ${username}    ${password}    ${should_succeed}=True

    Setup Browser
    Wait For Login Page
    Perform Login    ${username}    ${password}

    Run Keyword If    ${should_succeed}
    ...    Verify Login Success
    ...    ELSE
    ...    Verify Login Error

Teardown Browser
    [Documentation]    Cierra el navegador limpiamente
    Close Browser

Abrir Navegador En Login
    [Documentation]    EXACTAMENTE como Claude - keyword compatible
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    Wait Until Page Contains    Iniciar    timeout=${TIMEOUT}

