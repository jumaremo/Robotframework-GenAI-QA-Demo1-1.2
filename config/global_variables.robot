*** Settings ***
Documentation    Variables globales centralizadas para Robotframework-GenAI-QA-Demo1.2-Gemini
...              VERSIÓN v1.2: Sistema de configuración centralizada

Library          ../libraries/GeminiLibrary.py
Library          Collections

*** Variables ***
${CENTRAL_CONFIG_AVAILABLE}    ${TRUE}
${CONFIG_VERSION}              v1.2
${USUARIO_PRINCIPAL}           ${EMPTY}
${CLAVE_PRINCIPAL}             ${EMPTY}
${USUARIO_ADMIN}               ${EMPTY}
${CLAVE_ADMIN}                 ${EMPTY}
${USUARIO_BACKUP}              ${EMPTY}
${CLAVE_BACKUP}                ${EMPTY}
${CONFIG_MANAGER_STATUS}       ${EMPTY}
${TOTAL_CREDENCIALES}          0

*** Keywords ***
Cargar Variables Centralizadas
    [Documentation]    Carga variables desde configuración centralizada
    ${estado_biblioteca}=    Obtener Estado Biblioteca
    ${config_info}=    Get From Dictionary    ${estado_biblioteca}    config_centralizada
    ${config_disponible}=    Get From Dictionary    ${config_info}    disponible
    Set Global Variable    ${CONFIG_MANAGER_STATUS}    ${config_disponible}
    Log    Variables centralizadas cargadas: ${config_disponible}

Obtener Credencial Por Tipo
    [Documentation]    Obtiene una credencial específica por tipo
    [Arguments]    ${tipo_usuario}=funcional    ${entorno}=qa
    
    ${todas_credenciales}=    Obtener Credenciales Centralizadas    ${entorno}
    
    FOR    ${cred}    IN    @{todas_credenciales}
        ${tipo}=    Get From Dictionary    ${cred}    tipo    
        IF    '${tipo}' == '${tipo_usuario}'
            RETURN    ${cred}
        END
    END
    
    # Si no se encuentra el tipo específico, devolver la primera credencial
    ${primera_credencial}=    Set Variable    ${todas_credenciales[0]}
    Log    Tipo '${tipo_usuario}' no encontrado, usando primera credencial disponible
    
    RETURN    ${primera_credencial}

Mostrar Estado Configuracion Central
    [Documentation]    Muestra el estado actual del sistema de configuración centralizada
    
    Log    Estado configuracion centralizada v1.2
    Log    ConfigManager disponible: ${CONFIG_MANAGER_STATUS}
    Log    Usuario principal: ${USUARIO_PRINCIPAL}
    Log    Total credenciales: ${TOTAL_CREDENCIALES}
    Log    Version configuracion: ${CONFIG_VERSION}