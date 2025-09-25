*** Settings ***
Documentation    Localizadores EXACTOS como Claude para elementos de la interfaz SIESA ERP

*** Variables ***
# Pagina de Login - EXACTOS como Claude
${LOGIN_USER_FIELD}       //input[1]
${LOGIN_PASSWORD_FIELD}   //input[@type='password']
${LOGIN_SUBMIT_BUTTON}    //*[@data-automation-id="SDKButton_submit"]

# Dashboard y confirmacion de login exitoso - EXACTOS como Claude
${DASHBOARD_ELEMENT}      //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]
${LOGIN_SUCCESS_ELEMENT}  //*[@id="2038724f-1299-4948-8ec5-41cff6d44a3b"]/div/div[3]/div/div[2]/p[1]

# Mensajes de error y notificaciones - EXACTOS como Claude
${ERROR_REQUIRED_FIELDS}      //div[contains(@class, 'rz-notification-content') and contains(text(), 'Diligencie todos los campos requeridos')]
${ERROR_INVALID_CREDENTIALS}  //div[contains(@class, 'rz-notification-content') and contains(text(), 'Credenciales invalidas')]
${NOTIFICATION_CLOSE}         //div[contains(@class, 'rz-notification-close')]

# Navegacion general
${SIDEBAR_MENU}           //div[contains(@class, 'sidebar-menu')]
${MAIN_CONTENT}           //div[contains(@class, 'main-content')]

