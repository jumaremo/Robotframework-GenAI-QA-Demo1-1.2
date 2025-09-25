*** Settings ***
Documentation     Tests híbridos de login para SIESA ERP - Lo mejor de Gemini + Claude
...               VERSIÓN v1.2: Sistema de configuración centralizada integrado
...               Las credenciales ahora se cargan desde config/credentials.json
Library           SeleniumLibrary
Library           ../../libraries/GeminiLibrary.py
Library           Collections
Library           String
Library           OperatingSystem

# 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar variables globales
Resource          ../../config/global_variables.robot

*** Variables ***
${URL_LOGIN}      https://erp-qa-beta.siesaerp.com/login?returnUrl=%2F
${BROWSER}        chrome
${TIMEOUT}        20s

# Localizadores estandarizados (consistentes entre ambos proyectos)
${CAMPO_USUARIO}    //input[1]
${CAMPO_CLAVE}     //input[@type='password']
${BOTON_LOGIN}     //*[@data-automation-id="SDKButton_submit"]

# Elementos de confirmación y errores
${ELEMENTO_CONFIRMACION_LOGIN}    //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]
${MENSAJE_CAMPOS_REQUERIDOS}    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]
${MENSAJE_CREDENCIALES_INVALIDAS}    //div[contains(@class, 'rz-notification-content') and contains(text(), 'Credenciales invalidas')]

# ⚠️ CREDENCIALES MIGRADAS A SISTEMA CENTRALIZADO v1.2
# Las credenciales ahora se cargan automáticamente desde config/credentials.json
# Estas variables se mantienen para compatibilidad pero serán cargadas dinámicamente

${USUARIO_EXITOSO}    ${EMPTY}    # ← Ahora cargado desde configuración central
${CLAVE_EXITOSA}      ${EMPTY}    # ← Ahora cargado desde configuración central

# 📝 NOTA v1.2: Para cambiar credenciales, editar ÚNICAMENTE:
# → config/credentials.json (archivo maestro)

*** Test Cases ***
Login With Valid Credentials
    [Tags]    login    success    priority_high
    [Documentation]    Verifica login exitoso con credenciales garantizadas desde configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar credenciales dinámicamente
    Cargar Configuracion Central
    
    # Obtener credencial prioritaria desde configuración central
    ${credencial_prioritaria}=    Obtener Credencial Prioritaria Keyword    qa

    # Verificar que obtuvimos credenciales válidas
    Should Not Be Empty    ${credencial_prioritaria}    No se pudo obtener credencial prioritaria desde configuración central

    ${usuario}=    Get From Dictionary    ${credencial_prioritaria}    usuario
    ${clave}=      Get From Dictionary    ${credencial_prioritaria}    clave

    Log    Usando credencial desde configuración central: ${usuario}

    Abrir Navegador En Login
    Sleep    2s

    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Input Text    ${CAMPO_USUARIO}    ${usuario}

    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}
    Input Text    ${CAMPO_CLAVE}    ${clave}

    Wait Until Element Is Visible    ${BOTON_LOGIN}    timeout=${TIMEOUT}
    Click Element    ${BOTON_LOGIN}

    # Verificación específica que sabemos que funciona
    Wait Until Element Is Visible    ${ELEMENTO_CONFIRMACION_LOGIN}    timeout=${TIMEOUT}
    Log    Login exitoso confirmado con credenciales desde configuración centralizada v1.2
    Capture Page Screenshot    login_exitoso_hibrido_v12.png

    Sleep    3s

    [Teardown]    Close Browser

Login Interface Validation
    [Tags]    ui    validation    interface
    [Documentation]    Valida que todos los elementos de la interfaz de login estén presentes

    Abrir Navegador En Login

    # Verificar elementos principales (adoptado de Claude)
    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${BOTON_LOGIN}    timeout=${TIMEOUT}

    # Verificar título de la página
    Wait Until Page Contains    Iniciar sesión    timeout=${TIMEOUT}

    # Verificar que los campos están habilitados
    Element Should Be Enabled    ${CAMPO_USUARIO}
    Element Should Be Enabled    ${CAMPO_CLAVE}
    Element Should Be Enabled    ${BOTON_LOGIN}

    Log    Interfaz de login validada correctamente

    [Teardown]    Close Browser

Login With Empty Fields
    [Tags]    validation    error    empty_fields
    [Documentation]    Valida comportamiento del sistema con campos vacíos

    Abrir Navegador En Login

    # Dejar campos vacíos deliberadamente
    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}

    Input Text    ${CAMPO_USUARIO}    ${EMPTY}
    Input Text    ${CAMPO_CLAVE}    ${EMPTY}

    Click Element    ${BOTON_LOGIN}

    # Verificar mensaje de campos requeridos
    Wait Until Element Is Visible    ${MENSAJE_CAMPOS_REQUERIDOS}    timeout=${TIMEOUT}
    Log    Mensaje de campos requeridos mostrado correctamente

    Capture Page Screenshot    login_campos_vacios_v12.png

    [Teardown]    Close Browser

Login With Invalid Username
    [Tags]    error    invalid_credentials
    [Documentation]    Prueba login con usuario inexistente usando configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar configuración primero
    Cargar Configuracion Central

    # Generar credencial inválida usando Gemini (ventaja híbrida)
    ${credenciales}=    Generar Credenciales Siesa    cantidad=1
    ${invalidas}=    Get From Dictionary    ${credenciales}    credenciales_invalidas
    ${cred_test}=    Set Variable    ${invalidas[0]}

    # Extraer credenciales o usar fallback
    ${usuario_invalido}=    Get From Dictionary    ${cred_test}    usuario
    ${usuario_final}=    Set Variable If    '${usuario_invalido}' == ''    usuario_inexistente_hibrido_v12    ${usuario_invalido}

    Abrir Navegador En Login

    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}

    Input Text    ${CAMPO_USUARIO}    ${usuario_final}
    Input Text    ${CAMPO_CLAVE}    password123

    Click Element    ${BOTON_LOGIN}

    # Verificar algún tipo de error
    ${error_campos}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CAMPOS_REQUERIDOS}    timeout=10s
    ${error_credenciales}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CREDENCIALES_INVALIDAS}    timeout=10s

    ${hay_error}=    Evaluate    ${error_campos} or ${error_credenciales}
    Should Be True    ${hay_error}    Se esperaba algún mensaje de error

    Capture Page Screenshot    login_password_invalido_v12.png

    [Teardown]    Close Browser

Login With Generated Invalid Credentials
    [Tags]    ai_generated    error    gemini
    [Documentation]    Prueba login con credenciales inválidas generadas por Gemini IA usando configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar configuración primero
    Cargar Configuracion Central

    # Generar múltiples credenciales inválidas (ventaja Gemini)
    ${credenciales}=    Generar Credenciales Siesa    cantidad=3
    ${invalidas}=    Get From Dictionary    ${credenciales}    credenciales_invalidas

    Abrir Navegador En Login

    # Probar la primera credencial inválida generada
    ${cred_test}=    Set Variable    ${invalidas[0]}
    ${usuario_test}=    Get From Dictionary    ${cred_test}    usuario
    ${clave_test}=    Get From Dictionary    ${cred_test}    clave
    ${categoria}=    Get From Dictionary    ${cred_test}    categoria

    Log    Probando credencial generada por Gemini - Categoría: ${categoria}

    # Manejar campos vacíos
    ${usuario_final}=    Set Variable If    '${usuario_test}' == ''    usuario_vacio_v12    ${usuario_test}
    ${clave_final}=    Set Variable If    '${clave_test}' == ''    clave_vacia_v12    ${clave_test}

    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}

    Input Text    ${CAMPO_USUARIO}    ${usuario_final}
    Input Text    ${CAMPO_CLAVE}    ${clave_final}

    Click Element    ${BOTON_LOGIN}

    # Verificar que se produce algún error (flexible)
    ${error_campos}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CAMPOS_REQUERIDOS}    timeout=10s
    ${error_credenciales}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CREDENCIALES_INVALIDAS}    timeout=10s

    ${hay_error}=    Evaluate    ${error_campos} or ${error_credenciales}
    Should Be True    ${hay_error}    Se esperaba algún mensaje de error para credencial inválida

    Log    Credencial inválida generada por Gemini funcionó como se esperaba (configuración centralizada v1.2)
    Capture Page Screenshot    login_gemini_invalido_v12.png

    [Teardown]    Close Browser

Login With Multiple Environment Credentials
    [Tags]    config_centralizada    multiambiente    v12
    [Documentation]    Prueba login con credenciales de diferentes entornos usando configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Probar múltiples entornos
    Cargar Configuracion Central

    # Obtener credenciales para entorno QA
    ${credenciales_qa}=    Obtener Credenciales Centralizadas Keyword    qa
    Should Not Be Empty    ${credenciales_qa}    No se encontraron credenciales para entorno QA

    # Usar la primera credencial válida
    ${credencial_qa}=    Set Variable    ${credenciales_qa[0]}
    ${usuario_qa}=    Get From Dictionary    ${credencial_qa}    usuario
    ${clave_qa}=      Get From Dictionary    ${credencial_qa}    clave

    Log    Probando credencial de entorno QA desde configuración central: ${usuario_qa}

    Abrir Navegador En Login
    Sleep    2s

    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Input Text    ${CAMPO_USUARIO}    ${usuario_qa}

    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}
    Input Text    ${CAMPO_CLAVE}    ${clave_qa}

    Wait Until Element Is Visible    ${BOTON_LOGIN}    timeout=${TIMEOUT}
    Click Element    ${BOTON_LOGIN}

    # Verificación específica para credenciales de QA
    Wait Until Element Is Visible    ${ELEMENTO_CONFIRMACION_LOGIN}    timeout=${TIMEOUT}
    Log    Login exitoso con credencial de entorno QA desde configuración centralizada v1.2
    Capture Page Screenshot    login_qa_centralizado_v12.png

    Sleep    3s

    [Teardown]    Close Browser

Validar Sistema Configuracion Centralizada
    [Tags]    validacion    config_centralizada    sistema_v12
    [Documentation]    Valida que el sistema de configuración centralizada v1.2 esté funcionando correctamente

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Validar sistema completo
    Cargar Configuracion Central

    # Validar estado del sistema centralizado
    ${estado_config}=    Validar Configuracion Centralizada

    # Verificar que ConfigManager está disponible
    ${config_disponible}=    Get From Dictionary    ${estado_config}    config_manager_disponible
    Should Be True    ${config_disponible}    ConfigManager no está disponible

    # Verificar que el archivo de credenciales existe
    ${archivo_existe}=    Get From Dictionary    ${estado_config}    archivo_credenciales_existe
    Should Be True    ${archivo_existe}    Archivo de credenciales centrales no existe

    # Verificar que hay credenciales configuradas
    ${total_credenciales}=    Get From Dictionary    ${estado_config}    total_credenciales
    Should Be True    ${total_credenciales} > 0    No hay credenciales configuradas en el sistema central

    # Verificar entornos disponibles
    ${entornos}=    Get From Dictionary    ${estado_config}    entornos_configurados
    Should Not Be Empty    ${entornos}    No hay entornos configurados

    # Verificar que no hay errores críticos
    ${errores}=    Get From Dictionary    ${estado_config}    errores
    Should Be Empty    ${errores}    Errores encontrados en configuración centralizada: ${errores}

    Log    ✅ Sistema de configuración centralizada v1.2 validado correctamente
    Log    📊 Total credenciales: ${total_credenciales}
    Log    🌍 Entornos configurados: ${entornos}

*** Keywords ***
Abrir Navegador En Login
    [Documentation]    Abre el navegador y navega a la página de login con configuración robusta
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    # Esperar a que la página cargue completamente
    Wait Until Page Contains    Iniciar    timeout=${TIMEOUT}

Cargar Configuracion Central
    [Documentation]    Carga la configuración centralizada v1.2 y valida que esté disponible

    # Validar que el sistema de configuración centralizada esté funcionando
    ${estado_biblioteca}=    Obtener Estado Biblioteca
    ${config_info}=    Get From Dictionary    ${estado_biblioteca}    config_centralizada
    ${config_disponible}=    Get From Dictionary    ${config_info}    disponible

    Run Keyword If    not ${config_disponible}
    ...    Log    ⚠️ ADVERTENCIA: Sistema de configuración centralizada no disponible, usando fallback
    ...    ELSE
    ...    Log    ✅ Sistema de configuración centralizada v1.2 activo y funcionando

Obtener Credencial Prioritaria Keyword
    [Documentation]    Obtiene la credencial de mayor prioridad para un entorno específico
    [Arguments]    ${entorno}=qa

    ${credencial}=    Obtener Credencial Prioritaria    ${entorno}
    Should Not Be Empty    ${credencial}    No se pudo obtener credencial prioritaria para entorno: ${entorno}

    RETURN    ${credencial}

Obtener Credenciales Centralizadas Keyword
    [Documentation]    Obtiene todas las credenciales para un entorno específico
    [Arguments]    ${entorno}=qa

    ${credenciales}=    Obtener Credenciales Centralizadas    ${entorno}
    Should Not Be Empty    ${credenciales}    No se encontraron credenciales para entorno: ${entorno}

    RETURN    ${credenciales} (más flexible)
    ${error_campos}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CAMPOS_REQUERIDOS}    timeout=10s
    ${error_credenciales}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${MENSAJE_CREDENCIALES_INVALIDAS}    timeout=10s

    ${hay_error}=    Evaluate    ${error_campos} or ${error_credenciales}
    Should Be True    ${hay_error}    Se esperaba algún mensaje de error

    Run Keyword If    ${error_campos}    Log    Error de campos detectado
    Run Keyword If    ${error_credenciales}    Log    Error de credenciales detectado

    Capture Page Screenshot    login_usuario_invalido_v12.png

    [Teardown]    Close Browser

Login With Invalid Password
    [Tags]    error    invalid_credentials
    [Documentation]    Prueba login con contraseña incorrecta usando configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar configuración primero
    Cargar Configuracion Central

    # Obtener usuario válido desde configuración central
    ${credencial_prioritaria}=    Obtener Credencial Prioritaria Keyword    qa
    ${usuario_valido}=    Get From Dictionary    ${credencial_prioritaria}    usuario

    Abrir Navegador En Login

    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}

    # Usar usuario válido pero contraseña incorrecta
    Input Text    ${CAMPO_USUARIO}    ${usuario_valido}
    Input Text    ${CAMPO_CLAVE}    password_incorrecto_v12_123

    Click Element    ${BOTON_LOGIN}

    # Verificar algún tipo de error