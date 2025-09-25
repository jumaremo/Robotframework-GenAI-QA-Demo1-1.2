*** Settings ***
Documentation    Configuración global mejorada para Robotframework-GenAI-QA-Demo1.2-Gemini
...              Combina lo mejor de ambos proyectos (Claude y Gemini)
...              VERSIÓN v1.2: Sistema de configuración centralizada
...              Las credenciales ahora se cargan desde config/credentials.json

# 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Importar variables globales
Resource         global_variables.robot

*** Variables ***
# URLs y Ambientes
${BASE_URL}               https://erp-qa-beta.siesaerp.com/login?returnUrl=%2F
${BACKUP_URL}             https://erp-qa-beta.siesaerp.com/
${HEALTH_CHECK_URL}       https://erp-qa-beta.siesaerp.com/health

# Configuración de Browser mejorada
${BROWSER}                chrome
${HEADLESS}               False
${TIMEOUT}                20s
${IMPLICIT_WAIT}          10s
${PAGE_LOAD_TIMEOUT}      30s

# Configuración de red y rendimiento
${NETWORK_TIMEOUT}        30s
${RETRY_ATTEMPTS}         3
${RETRY_DELAY}           2s

# Directorios del proyecto con estructura mejorada
${PROJECT_ROOT}           ${CURDIR}/..
${DATA_DIR}               ${PROJECT_ROOT}/data/generated
${SCREENSHOTS_DIR}        ${PROJECT_ROOT}/results/screenshots
${REPORTS_DIR}            ${PROJECT_ROOT}/results/reports
${AI_ANALYSIS_DIR}        ${PROJECT_ROOT}/results/ai_analysis
${LOGS_DIR}               ${PROJECT_ROOT}/results/logs

# Archivos de datos y configuración
${CREDENTIALS_FILE}       ${DATA_DIR}/credenciales_siesa.json
${BACKUP_CREDENTIALS}     ${DATA_DIR}/credenciales_backup.json
${TEST_DATA_FILE}         ${DATA_DIR}/test_data.json
${CONFIG_FILE}           ${PROJECT_ROOT}/config/test_config.json

# ⚠️ CREDENCIALES MIGRADAS A SISTEMA CENTRALIZADO v1.2
# Las credenciales ahora se cargan automáticamente desde config/credentials.json
# Estas variables se mantienen para compatibilidad pero serán cargadas dinámicamente

# Credenciales de prueba válidas (CARGADAS AUTOMÁTICAMENTE)
${VALID_USER}         ${EMPTY}    # ← Ahora cargado desde config/credentials.json
${VALID_PASSWORD}     ${EMPTY}    # ← Ahora cargado desde config/credentials.json
${ADMIN_USER}         ${EMPTY}    # ← Ahora cargado desde config/credentials.json
${ADMIN_PASSWORD}     ${EMPTY}    # ← Ahora cargado desde config/credentials.json

# Credenciales de respaldo para casos críticos (CARGADAS AUTOMÁTICAMENTE)
${BACKUP_USER}        ${EMPTY}    # ← Ahora cargado desde config/credentials.json
${BACKUP_PASSWORD}    ${EMPTY}    # ← Ahora cargado desde config/credentials.json

# 📝 NOTA v1.2: Para cambiar credenciales, editar ÚNICAMENTE:
# → config/credentials.json (archivo maestro)
# Las credenciales se cargan automáticamente al iniciar las pruebas

# Localizadores mejorados con fallbacks
${LOGIN_USER_FIELD}       //input[1]
${LOGIN_PASSWORD_FIELD}   //input[@type='password']
${LOGIN_SUBMIT_BUTTON}    //*[@data-automation-id="SDKButton_submit"]

# Localizadores alternativos para robustez
${ALT_USER_FIELD}         //input[@placeholder='Usuario' or @name='username' or @id='username']
${ALT_PASSWORD_FIELD}     //input[@placeholder='Contraseña' or @name='password' or @id='password']
${ALT_SUBMIT_BUTTON}      //button[@type='submit' or contains(@class, 'login') or contains(text(), 'Iniciar')]

# Elementos de validación y confirmación
${DASHBOARD_ELEMENT}      //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]
${LOGIN_SUCCESS_ELEMENT}  //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]
${WELCOME_MESSAGE}        //div[contains(@class, 'welcome') or contains(text(), 'Bienvenido')]

# Mensajes de error y notificaciones
${ERROR_REQUIRED_FIELDS}      //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]
${ERROR_INVALID_CREDENTIALS}  //div[contains(@class, 'rz-notification-content') and contains(text(), 'Credenciales invalidas')]
${ERROR_NETWORK}              //div[contains(@class, 'error') and contains(text(), 'red')]
${ERROR_TIMEOUT}              //div[contains(@class, 'timeout')]
${NOTIFICATION_CLOSE}         //div[contains(@class, 'rz-notification-close')]

# Navegación general y elementos comunes
${SIDEBAR_MENU}           //div[contains(@class, 'sidebar-menu')]
${MAIN_CONTENT}           //div[contains(@class, 'main-content')]
${LOADING_INDICATOR}      //div[contains(@class, 'loading') or contains(@class, 'spinner')]
${PAGE_TITLE}             //title | //h1 | //h2[contains(@class, 'title')]

# Configuración de IA y análisis
${AI_PROVIDER}            gemini
${AI_MODEL}               gemini-1.5-flash
${AI_ANALYSIS_ENABLED}    True
${SEMANTIC_VALIDATION}    True

# Configuración de reportes
${GENERATE_SCREENSHOTS}   True
${DETAILED_LOGS}          True
${AI_REPORTS}            True
${MARKDOWN_REPORTS}      True

# Configuración de pruebas
${PARALLEL_EXECUTION}     False
${MAX_WORKERS}           2
${TEST_ISOLATION}        True
${CLEANUP_AFTER_TEST}    True

# Tags para organización de pruebas
${SMOKE_TAGS}            smoke,critical
${REGRESSION_TAGS}       regression,full
${AI_TAGS}               ai,gemini,analysis
${UI_TAGS}               ui,interface,validation

# Configuración de entorno
${ENVIRONMENT}           qa
${REGION}                us-east-1
${LOCALE}                es-CO
${TIMEZONE}              America/Bogota

# Configuración de logging mejorada
${LOG_LEVEL}             INFO
${CONSOLE_LOG_LEVEL}     INFO
${AI_LOG_LEVEL}          DEBUG

# Timeouts específicos por tipo de operación
${LOGIN_TIMEOUT}         15s
${NAVIGATION_TIMEOUT}    10s
${ELEMENT_TIMEOUT}       8s
${AJAX_TIMEOUT}          20s
${DOWNLOAD_TIMEOUT}      60s

# Configuración de reintentos
${MAX_LOGIN_RETRIES}     3
${MAX_ELEMENT_RETRIES}   2
${MAX_NETWORK_RETRIES}   3

# Configuración de datos de prueba
${MIN_CREDENTIALS}       5
${MAX_CREDENTIALS}       20
${DATA_GENERATION_MODE}  ai_enhanced
${FALLBACK_MODE}         local_generation

# URLs de servicios adicionales (si los hay)
${API_BASE_URL}          https://api-qa.siesaerp.com
${DOCS_URL}              https://docs.siesaerp.com
${SUPPORT_URL}           https://support.siesaerp.com

# Configuración de integración con CI/CD
${CI_MODE}               False
${HEADLESS_CI}           True
${PARALLEL_CI}           True
${SKIP_UI_TESTS_CI}      False

# Configuración de base de datos (si se requiere)
${DB_HOST}               localhost
${DB_PORT}               5432
${DB_NAME}               siesa_test
${DB_USER}               test_user
${DB_TIMEOUT}            30s

# Configuración de archivos temporales
${TEMP_DIR}              ${PROJECT_ROOT}/temp
${DOWNLOAD_DIR}          ${PROJECT_ROOT}/downloads
${UPLOAD_DIR}            ${PROJECT_ROOT}/uploads

# Configuración de monitoreo y métricas
${PERFORMANCE_MONITORING}    True
${MEMORY_MONITORING}         True
${NETWORK_MONITORING}        True
${AI_USAGE_TRACKING}         True

# Variables de estado y control
${TEST_SESSION_ID}       ${EMPTY}
${CURRENT_USER}          ${EMPTY}
${LAST_ERROR_TYPE}       ${EMPTY}
${AI_ANALYSIS_COUNT}     0

# 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Rutas de archivos centrales
${CENTRAL_CONFIG_DIR}     ${PROJECT_ROOT}/config
${CENTRAL_CREDENTIALS}    ${CENTRAL_CONFIG_DIR}/credentials.json
${GLOBAL_VARIABLES_FILE}  ${CENTRAL_CONFIG_DIR}/global_variables.robot
${CONFIG_MANAGER_FILE}    ${CENTRAL_CONFIG_DIR}/config.py
