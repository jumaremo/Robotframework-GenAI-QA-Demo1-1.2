*** Settings ***
Documentation     Demo de errores para mostrar el Listener IA con Gemini y SIESA ERP
Library           SeleniumLibrary
Library           ../../listeners/robot_ai_listener_gemini.py
Library           ../../libraries/GeminiLibrary.py
Library           Collections

*** Variables ***
${URL_SIESA}      https://erp-qa-beta.siesaerp.com/login?returnUrl=%2F
${BROWSER}        chrome
${TIMEOUT}        15s
${CAMPO_USUARIO}    //input[1]
${CAMPO_CLAVE}    //input[@type='password']
${BOTON_LOGIN}    //*[@data-automation-id="SDKButton_submit"]

*** Test Cases ***
Test Error Usuario Incorrecto Con Gemini Analysis
    [Tags]    error    demo    gemini
    [Documentation]    Demuestra análisis de errores con Gemini AI para usuario incorrecto

    # Generar credencial inválida específica usando Gemini
    ${credenciales}=    Generar Credenciales Siesa    cantidad=1
    ${cred_invalida}=    Set Variable    ${credenciales['credenciales_invalidas'][0]}
    ${usuario_test}=    Get From Dictionary    ${cred_invalida}    usuario
    ${clave_test}=    Get From Dictionary    ${cred_invalida}    clave

    # Si las credenciales están vacías, usar valores de prueba
    ${usuario_final}=    Set Variable If    '${usuario_test}' == ''    usuario_gemini_inexistente    ${usuario_test}
    ${clave_final}=    Set Variable If    '${clave_test}' == ''    password_gemini_123    ${clave_test}

    Open Browser    ${URL_SIESA}    ${BROWSER}
    Maximize Browser Window

    # Esperar a que la página cargue
    Wait Until Page Contains Element    ${CAMPO_USUARIO}    timeout=${TIMEOUT}

    # Ingresar credenciales generadas por Gemini
    Input Text    ${CAMPO_USUARIO}    ${usuario_final}
    Input Text    ${CAMPO_CLAVE}    ${clave_final}

    Log    Probando credenciales generadas por Gemini: ${usuario_final}

    # Hacer clic en el botón de login
    Click Element    ${BOTON_LOGIN}

    # Esperar mensaje de error - esto debe fallar y ser analizado por Gemini AI
    Wait Until Page Contains    Credenciales invalidas    timeout=${TIMEOUT}

    [Teardown]    Close Browser

Test Error Campo Vacio Con Gemini Analysis
    [Tags]    error    demo    gemini    validation
    [Documentation]    Demuestra análisis de errores de validación con Gemini AI

    Open Browser    ${URL_SIESA}    ${BROWSER}
    Maximize Browser Window

    # Esperar a que la página cargue
    Wait Until Page Contains Element    ${CAMPO_USUARIO}    timeout=${TIMEOUT}

    # Dejar campos vacíos deliberadamente para que Gemini analice el error
    Input Text    ${CAMPO_USUARIO}    ${EMPTY}
    Input Text    ${CAMPO_CLAVE}    ${EMPTY}

    # Hacer clic en el botón de login
    Click Element    ${BOTON_LOGIN}

    # Esperar mensaje de error de campos requeridos
    Wait Until Element Is Visible    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]    timeout=${TIMEOUT}

    [Teardown]    Close Browser

Test Error Credenciales Especiales Con Gemini Analysis
    [Tags]    error    demo    gemini    special_chars
    [Documentation]    Demuestra análisis de errores con caracteres especiales usando Gemini AI

    # Buscar credencial con caracteres especiales generada por Gemini
    ${credenciales}=    Generar Credenciales Siesa    cantidad=5
    ${invalidas}=    Get From Dictionary    ${credenciales}    credenciales_invalidas

    ${usuario_especial}=    Set Variable    user@#$%
    ${clave_especial}=    Set Variable    pass*&()

    # Buscar credencial con caracteres especiales
    FOR    ${cred}    IN    @{invalidas}
        ${categoria}=    Get From Dictionary    ${cred}    categoria
        ${usuario}=    Get From Dictionary    ${cred}    usuario
        ${clave}=    Get From Dictionary    ${cred}    clave

        Run Keyword If    '${categoria}' == 'caracteres_especiales'
        ...    Run Keywords
        ...    Set Test Variable    ${usuario_especial}    ${usuario}
        ...    AND    Set Test Variable    ${clave_especial}    ${clave}
        ...    AND    Exit For Loop
    END

    Open Browser    ${URL_SIESA}    ${BROWSER}
    Maximize Browser Window

    # Esperar a que la página cargue
    Wait Until Page Contains Element    ${CAMPO_USUARIO}    timeout=${TIMEOUT}

    # Ingresar credenciales con caracteres especiales
    Input Text    ${CAMPO_USUARIO}    ${usuario_especial}
    Input Text    ${CAMPO_CLAVE}    ${clave_especial}

    Log    Probando caracteres especiales generados por Gemini: ${usuario_especial}

    # Hacer clic en el botón de login
    Click Element    ${BOTON_LOGIN}

    # Esperar cualquier tipo de error
    ${error_campos}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]    timeout=5s

    ${error_credenciales}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Credenciales invalidas')]    timeout=5s

    # Debe haber algún tipo de error para que Gemini lo analice
    ${hay_error}=    Evaluate    ${error_campos} or ${error_credenciales}
    Should Be True    ${hay_error}    Se esperaba algún tipo de error para análisis de Gemini

    [Teardown]    Close Browser

*** Keywords ***
Esperar Y Manejar Error
    [Arguments]    ${tipo_esperado}=any
    [Documentation]    Espera y maneja diferentes tipos de errores para análisis de Gemini

    # Esperar diferentes tipos de mensajes de error
    ${error_campos}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]    timeout=5s

    ${error_credenciales}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Credenciales invalidas')]    timeout=5s

    # Determinar tipo de error detectado
    ${tipo_error}=    Set Variable If
    ...    ${error_campos}    campos_requeridos
    ...    ${error_credenciales}    credenciales_invalidas
    ...    no_detectado

    Log    Tipo de error detectado: ${tipo_error}

    # Cerrar notificación si está presente
    ${cerrar_notif}=    Run Keyword And Return Status
    ...    Click Element    //div[contains(@class, 'rz-notification-close')]

    RETURN    ${tipo_error}
