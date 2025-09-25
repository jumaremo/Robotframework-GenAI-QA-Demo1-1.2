*** Settings ***
Documentation     Tests híbridos de login para SIESA ERP con métricas de eficiencia - Lo mejor de Gemini + Claude
...               VERSIÓN v1.2: Sistema de configuración centralizada integrado
...               Las credenciales ahora se cargan desde config/credentials.json
Library           SeleniumLibrary
Library           ../../libraries/GeminiLibrary.py
Library           ../../libraries/MetricsLibrary.py
Library           Collections
Library           String
Library           OperatingSystem
Library           DateTime

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

*** Keywords ***
Setup Test With Metrics
    [Documentation]    Configura el test e inicia medición de métricas con configuración centralizada v1.2
    [Arguments]    ${test_name}

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar configuración antes de métricas
    Cargar Configuracion Central
    
    Iniciar Medicion    ${test_name}
    Abrir Navegador En Login
    
    # Agregar métrica específica para configuración centralizada
    Log    ✅ Test iniciado con configuración centralizada v1.2: ${test_name}

Teardown Test With Metrics
    [Documentation]    Finaliza el test y calcula métricas incluyendo datos de configuración centralizada v1.2
    [Arguments]    ${test_name}

    ${resultado}=    Finalizar Medicion    ${test_name}
    
    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Agregar información de configuración a métricas
    ${estado_config}=    Validar Configuracion Centralizada
    ${config_disponible}=    Get From Dictionary    ${estado_config}    config_manager_disponible
    
    Log    Métricas del test: ${resultado}
    Log    Configuración centralizada activa: ${config_disponible}
    Close Browser

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

Obtener Credencial Prioritaria Para Metricas
    [Documentation]    Obtiene la credencial de mayor prioridad y mide tiempo de carga
    [Arguments]    ${entorno}=qa
    
    ${inicio_tiempo}=    Get Current Date    result_format=epoch
    ${credencial}=    Obtener Credencial Prioritaria    ${entorno}
    ${fin_tiempo}=    Get Current Date    result_format=epoch
    ${tiempo_carga}=    Evaluate    ${fin_tiempo} - ${inicio_tiempo}
    
    Should Not Be Empty    ${credencial}    No se pudo obtener credencial prioritaria para entorno: ${entorno}
    
    Log    ⏱️ Tiempo de carga de credencial desde configuración central: ${tiempo_carga}s
    
    [Return]    ${credencial}

*** Test Cases ***
Login With Valid Credentials With Metrics
    [Tags]    login    success    priority_high    metrics    config_centralizada_v12
    [Documentation]    Verifica login exitoso con credenciales desde configuración centralizada v1.2 y mide eficiencia

    Setup Test With Metrics    login_exitoso_con_metricas_v12

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Obtener credenciales dinámicamente
    ${credencial_prioritaria}=    Obtener Credencial Prioritaria Para Metricas    qa
    
    # Verificar que obtuvimos credenciales válidas
    Should Not Be Empty    ${credencial_prioritaria}    No se pudo obtener credencial prioritaria desde configuración central
    
    ${usuario}=    Get From Dictionary    ${credencial_prioritaria}    usuario
    ${clave}=      Get From Dictionary    ${credencial_prioritaria}    clave
    
    Log    📊 Usando credencial desde configuración central para métricas: ${usuario}

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
    Capture Page Screenshot    login_exitoso_hibrido_metricas_v12.png

    Sleep    3s

    [Teardown]    Teardown Test With Metrics    login_exitoso_con_metricas_v12

Login Interface Validation With Metrics
    [Tags]    ui    validation    interface    metrics
    [Documentation]    Valida que todos los elementos de la interfaz de login estén presentes y mide tiempo

    Setup Test With Metrics    validacion_interfaz_con_metricas_v12

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

    [Teardown]    Teardown Test With Metrics    validacion_interfaz_con_metricas_v12

Login With Empty Fields With Metrics
    [Tags]    validation    error    empty_fields    metrics
    [Documentation]    Valida comportamiento del sistema con campos vacíos y mide tiempo de detección

    Setup Test With Metrics    campos_vacios_con_metricas_v12

    # Dejar campos vacíos deliberadamente
    Wait Until Element Is Visible    ${CAMPO_USUARIO}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CAMPO_CLAVE}    timeout=${TIMEOUT}

    Input Text    ${CAMPO_USUARIO}    ${EMPTY}
    Input Text    ${CAMPO_CLAVE}    ${EMPTY}

    Click Element    ${BOTON_LOGIN}

    # Verificar mensaje de campos requeridos
    Wait Until Element Is Visible    ${MENSAJE_CAMPOS_REQUERIDOS}    timeout=${TIMEOUT}
    Log    Mensaje de campos requeridos mostrado correctamente

    Capture Page Screenshot    login_campos_vacios_metricas_v12.png

    [Teardown]    Teardown Test With Metrics    campos_vacios_con_metricas_v12

Login With AI Generated Invalid Credentials With Metrics
    [Tags]    ai_generated    error    gemini    metrics    config_centralizada_v12
    [Documentation]    Prueba login con credenciales inválidas generadas por Gemini IA y mide eficiencia usando configuración centralizada v1.2

    Setup Test With Metrics    credenciales_ia_con_metricas_v12

    # Generar múltiples credenciales inválidas (ventaja Gemini)
    ${credenciales}=    Generar Credenciales Siesa    cantidad=3
    ${invalidas}=    Get From Dictionary    ${credenciales}    credenciales_invalidas

    # Verificar que las credenciales se generaron con configuración centralizada
    ${metadata}=    Get From Dictionary    ${credenciales}    metadata
    ${config_centralizada}=    Get From Dictionary    ${metadata}    config_centralizada
    Log    📊 Credenciales generadas con configuración centralizada: ${config_centralizada}

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
    Capture Page Screenshot    login_gemini_invalido_metricas_v12.png

    [Teardown]    Teardown Test With Metrics    credenciales_ia_con_metricas_v12

Performance Test Multiple Credentials With Metrics
    [Tags]    performance    metrics    config_centralizada_v12    stress_test
    [Documentation]    Prueba rendimiento del sistema con múltiples credenciales desde configuración centralizada v1.2

    Setup Test With Metrics    performance_credenciales_v12

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Obtener múltiples credenciales
    ${credenciales_qa}=    Obtener Credenciales Centralizadas    qa
    Should Not Be Empty    ${credenciales_qa}    No se encontraron credenciales para entorno QA
    
    ${total_credenciales}=    Get Length    ${credenciales_qa}
    Log    📊 Probando rendimiento con ${total_credenciales} credenciales desde configuración central

    # Probar cada credencial y medir tiempo
    FOR    ${index}    IN RANGE    ${total_credenciales}
        ${credencial}=    Set Variable    ${credenciales_qa[${index}]}
        ${usuario}=    Get From Dictionary    ${credencial}    usuario
        ${clave}=      Get From Dictionary    ${credencial}    clave
        
        Log    🔄 Probando credencial ${index + 1}/${total_credenciales}: ${usuario}
        
        # Limpiar campos anteriores
        Clear Element Text    ${CAMPO_USUARIO}
        Clear Element Text    ${CAMPO_CLAVE}
        
        # Medir tiempo de entrada de credenciales
        ${inicio_entrada}=    Get Current Date    result_format=epoch
        Input Text    ${CAMPO_USUARIO}    ${usuario}
        Input Text    ${CAMPO_CLAVE}    ${clave}
        ${fin_entrada}=    Get Current Date    result_format=epoch
        ${tiempo_entrada}=    Evaluate    ${fin_entrada} - ${inicio_entrada}
        
        Log    ⏱️ Tiempo entrada credencial ${index + 1}: ${tiempo_entrada}s
        
        # Solo intentar login con la primera credencial para evitar múltiples logins
        Run Keyword If    ${index} == 0
        ...    Click Element    ${BOTON_LOGIN}
        
        # Pequeña pausa entre credenciales
        Sleep    1s
    END
    
    Log    ✅ Test de rendimiento completado con ${total_credenciales} credenciales

    [Teardown]    Teardown Test With Metrics    performance_credenciales_v12

Generate Metrics Summary With Centralized Config
    [Tags]    metrics    summary    config_centralizada_v12
    [Documentation]    Genera resumen final de métricas de todos los tests incluyendo información de configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar configuración para métricas
    Cargar Configuracion Central
    
    ${metricas_completas}=    Obtener Metricas Completas
    ${ahorro_total}=    Calcular Ahorro Total

    Log    Métricas completas de la sesión: ${metricas_completas}
    Log    Ahorro total calculado: ${ahorro_total}

    # Generar reporte incluyendo información de configuración centralizada
    ${estado_config}=    Validar Configuracion Centralizada
    Log    📊 Estado configuración centralizada: ${estado_config}

    ${reporte}=    Generar Reporte Metricas    results/metricas_tests_completas_v12.json
    Log    Reporte de métricas generado: ${reporte}

    # Mostrar resumen ejecutivo con información v1.2
    Mostrar Resumen Ejecutivo
    
    # Información adicional específica de v1.2
    ${total_credenciales}=    Get From Dictionary    ${estado_config}    total_credenciales
    ${entornos}=    Get From Dictionary    ${estado_config}    entornos_configurados
    
    Log    🎯 RESUMEN v1.2:
    Log    📈 Total credenciales en configuración central: ${total_credenciales}
    Log    🌍 Entornos configurados: ${entornos}
    Log    ✅ Sistema de configuración centralizada funcionando correctamente

Validate Centralized Config Performance
    [Tags]    config_validation    performance    v12
    [Documentation]    Valida el rendimiento del sistema de configuración centralizada v1.2

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Test específico de rendimiento
    Log    🧪 Iniciando validación de rendimiento del sistema centralizado v1.2
    
    # Medir tiempo de carga inicial
    ${inicio_carga}=    Get Current Date    result_format=epoch
    Cargar Configuracion Central
    ${fin_carga}=    Get Current Date    result_format=epoch
    ${tiempo_carga_inicial}=    Evaluate    ${fin_carga} - ${inicio_carga}
    
    Log    ⏱️ Tiempo de carga inicial del sistema centralizado: ${tiempo_carga_inicial}s
    
    # Medir tiempo de obtención de credenciales
    ${inicio_credenciales}=    Get Current Date    result_format=epoch
    ${credenciales}=    Obtener Credenciales Centralizadas    qa
    ${fin_credenciales}=    Get Current Date    result_format=epoch
    ${tiempo_credenciales}=    Evaluate    ${fin_credenciales} - ${inicio_credenciales}
    
    Log    ⏱️ Tiempo de obtención de credenciales: ${tiempo_credenciales}s
    
    # Validar que los tiempos son aceptables (menos de 1 segundo)
    Should Be True    ${tiempo_carga_inicial} < 1.0    Tiempo de carga inicial demasiado alto: ${tiempo_carga_inicial}s
    Should Be True    ${tiempo_credenciales} < 1.0    Tiempo de obtención de credenciales demasiado alto: ${tiempo_credenciales}s
    
    # Medir tiempo de validación completa
    ${inicio_validacion}=    Get Current Date    result_format=epoch
    ${estado}=    Validar Configuracion Centralizada
    ${fin_validacion}=    Get Current Date    result_format=epoch
    ${tiempo_validacion}=    Evaluate    ${fin_validacion} - ${inicio_validacion}
    
    Log    ⏱️ Tiempo de validación completa: ${tiempo_validacion}s
    
    Should Be True    ${tiempo_validacion} < 2.0    Tiempo de validación demasiado alto: ${tiempo_validacion}s
    
    Log    ✅ Rendimiento del sistema de configuración centralizada v1.2 validado correctamente