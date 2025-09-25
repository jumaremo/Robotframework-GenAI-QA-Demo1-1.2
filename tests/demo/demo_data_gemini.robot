*** Settings ***
Documentation     Demo de uso de GeminiLibrary con validaciones avanzadas
Library           ../../libraries/GeminiLibrary.py
Library           Collections
Library           String
Library           OperatingSystem

*** Test Cases ***
Validar Descripcion De Producto Con Gemini
    [Tags]    demo    validation    gemini
    [Documentation]    Demuestra capacidades de validación semántica con Gemini AI

    # Simulamos obtener una descripción de producto
    ${descripcion}=    Set Variable    Este producto es una batería externa de 10000mAh compatible con dispositivos iOS y Android. Incluye cable USB-C y adaptador Lightning.

    # Validamos que la descripción contiene la información requerida
    ${criterios}=    Create List    menciona capacidad de batería    menciona compatibilidad
    ${es_valido}=    Verificar Contenido Apropiado    ${descripcion}    criterios=${criterios}
    Should Be True    ${es_valido}    La descripción no cumple con los criterios requeridos

    # Validamos similitud semántica con un texto de referencia
    ${texto_referencia}=    Set Variable    Batería portátil de gran capacidad que funciona con teléfonos Apple y Android.
    ${es_similar}=    Validar Similitud Semantica    ${descripcion}    ${texto_referencia}    umbral=0.7
    Should Be True    ${es_similar}    Las descripciones no son semánticamente similares

    # Generamos variaciones de descripción para pruebas usando Gemini
    ${resultado}=    Generar Datos De Prueba    variaciones de esta descripción de producto    3    formato=dict

    # Verificamos el tipo de datos y ajustamos si es necesario
    ${tipo}=    Evaluate    type($resultado).__name__
    ${variaciones}=    Run Keyword If    '${tipo}' == 'dict' and 'variaciones' in $resultado
    ...    Set Variable    ${resultado['variaciones']}
    ...    ELSE IF    '${tipo}' == 'dict'
    ...    Set Variable    ${resultado.values()}
    ...    ELSE
    ...    Set Variable    ${resultado}

    # Mostramos las variaciones generadas por Gemini
    Log    Tipo de datos: ${tipo}
    Log    Generado con: ${resultado.get('metadata', {}).get('proveedor', 'desconocido')}

    FOR    ${variacion}    IN    @{variaciones}
        Log    Variación generada por Gemini: ${variacion}
    END

Generar Credenciales Con Gemini AI
    [Tags]    demo    generation    gemini
    [Documentation]    Demuestra generación de credenciales usando Gemini AI

    # Generar credenciales específicas para SIESA
    ${credenciales}=    Generar Credenciales Siesa    cantidad=3    incluir_validas=True

    # Validar estructura de respuesta
    Should Contain    ${credenciales}    credenciales_validas
    Should Contain    ${credenciales}    credenciales_invalidas
    Should Contain    ${credenciales}    metadata

    # Verificar metadata de Gemini
    ${metadata}=    Get From Dictionary    ${credenciales}    metadata
    ${proveedor}=    Get From Dictionary    ${metadata}    proveedor_ia
    Log    Credenciales generadas con: ${proveedor}

    # Validar credenciales válidas
    ${validas}=    Get From Dictionary    ${credenciales}    credenciales_validas
    ${total_validas}=    Get Length    ${validas}
    Should Be True    ${total_validas} >= 1    Debe haber al menos una credencial válida

    # Validar credenciales inválidas
    ${invalidas}=    Get From Dictionary    ${credenciales}    credenciales_invalidas
    ${total_invalidas}=    Get Length    ${invalidas}
    Should Be True    ${total_invalidas} >= 3    Debe haber al menos 3 credenciales inválidas

    # Validar formato de cada credencial inválida
    FOR    ${cred}    IN    @{invalidas}
        Should Contain    ${cred}    usuario
        Should Contain    ${cred}    clave
        Should Contain    ${cred}    descripcion
        Should Contain    ${cred}    error_esperado
        Should Contain    ${cred}    categoria

        ${categoria}=    Get From Dictionary    ${cred}    categoria
        Should Be True    '${categoria}' in ['campos_vacios', 'caracteres_especiales', 'formato_invalido', 'inexistente']
    END

Comparar Gemini vs Claude Capacidades
    [Tags]    demo    comparison    ai
    [Documentation]    Compara capacidades de generación entre diferentes proveedores de IA

    # Obtener estado de la biblioteca
    ${estado}=    Obtener Estado Biblioteca
    Log    Estado actual de GeminiLibrary: ${estado}

    # Verificar disponibilidad de Gemini
    ${gemini_disponible}=    Get From Dictionary    ${estado}    gemini_disponible
    ${modo}=    Get From Dictionary    ${estado}    modo

    Log    Gemini disponible: ${gemini_disponible}
    Log    Modo de operación: ${modo}

    # Generar datos de prueba con el proveedor disponible
    ${datos_prueba}=    Generar Datos De Prueba    casos de prueba para login con diferentes tipos de errores    5

    # Validar que se generaron datos
    Should Contain    ${datos_prueba}    variaciones
    Should Contain    ${datos_prueba}    metadata

    ${proveedor}=    Get From Dictionary    ${datos_prueba['metadata']}    proveedor
    Log    Datos generados por: ${proveedor}

    # Si es Gemini, debería tener mejor calidad
    Run Keyword If    '${proveedor}' == 'gemini-pro'
    ...    Log    ✅ Usando Gemini AI para generación inteligente
    ...    ELSE
    ...    Log    ⚠️ Usando fallback - considera configurar Gemini API

Validar Guardado De Credenciales
    [Tags]    demo    file    persistence
    [Documentation]    Valida el guardado y lectura de credenciales generadas

    # Generar credenciales
    ${credenciales}=    Generar Credenciales Siesa    cantidad=2

    # Guardar en archivo temporal
    ${archivo_temporal}=    Set Variable    ${TEMPDIR}/test_credenciales_gemini.json
    ${resultado}=    Guardar Credenciales Json    ${credenciales}    ${archivo_temporal}

    # Verificar que se guardó correctamente
    Should Contain    ${resultado}    Credenciales guardadas
    File Should Exist    ${archivo_temporal}

    # Leer y validar contenido
    ${contenido}=    Get File    ${archivo_temporal}
    ${datos_leidos}=    Evaluate    json.loads('''${contenido}''')    json

    # Validar estructura
    Should Contain    ${datos_leidos}    metadata
    Should Contain    ${datos_leidos}    credenciales_validas
    Should Contain    ${datos_leidos}    credenciales_invalidas

    # Limpiar archivo temporal
    Remove File    ${archivo_temporal}

    Log    ✅ Credenciales guardadas y validadas correctamente
