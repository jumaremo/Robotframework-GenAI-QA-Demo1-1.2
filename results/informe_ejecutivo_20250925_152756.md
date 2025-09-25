# 📊 Informe Ejecutivo de Pruebas Automatizadas
## Login_Tests_20250925_152624

**Generado:** 2025-09-25 15:27:56
**Motor de IA:** Gemini AI

## 📈 Resumen de Resultados

| Métrica | Resultado |
| ------- | --------- |
| Total de pruebas | **7** |
| ✅ Pruebas exitosas | **0** (0.0%) |
| ❌ Pruebas fallidas | **7** |
| ⏱️ Tiempo total de ejecución | **N/A** |
| 📅 Fecha de ejecución | **2025-09-25** |

**Distribución de resultados:** 🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 0.0%

## 🧪 Detalle de Casos de Prueba

### ❌ Tests Fallidos

#### 🔴 Login With Valid Credentials

**Tiempo de ejecución:** N/A

**Error:** ```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 137
Current browser version is 140.0.7339.128 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
Stacktrace:
	GetHandleVerifier [0x0x7ff7a42afea5+79173]
	GetHandleVerifier [0x0x7ff7a42aff00+79264]
	(No symbol) [0x0x7ff7a4069e5a]
	(No symbol) [0x0x7ff7a40ae26f]
	(No symbol) [0x0x7ff7a40ad2bb]
	(No symbol) [0x0x7ff7a40a68ed]
	(No symbol) [0x0x7ff7a40a2b1d]
	(No symbol) [0x0x7ff7a40f67de]
	(No symbol) [0x0x7ff7a40f5f70]
	(No symbol) [0x0x7ff7a40e8743]
	(No symbol) [0x0x7ff7a40b14c1]
	(No symbol) [0x0x7ff7a40b2253]
	GetHandleVerifier [0x0x7ff7a457a2dd+3004797]
	GetHandleVerifier [0x0x7ff7a457472d+2981325]
	GetHandleVerifier [0x0x7ff7a4593380+3107360]
	GetHandleVerifier [0x0x7ff7a42caa2e+188622]
	GetHandleVerifier [0x0x7ff7a42d22bf+219487]
	GetHandleVerifier [0x0x7ff7a42b8df4+115860]
	GetHandleVerifier [0x0x7ff7a42b8fa9+116297]
	GetHandleVerifier [0x0x7ff7a429f558+11256]
	BaseThreadInitThunk [0x0x7ff976dce8d7+23]
	RtlUserThreadStart [0x0x7ff977fe8d9c+44]

```

**Acciones principales:** Cargar Configuracion Central, Obtener Estado Biblioteca, Get From Dictionary, Run Keyword If, Log...

#### 🔴 Login Interface Validation

**Tiempo de ejecución:** N/A

**Error:** ```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 137
Current browser version is 140.0.7339.128 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
Stacktrace:
	GetHandleVerifier [0x0x7ff7a42afea5+79173]
	GetHandleVerifier [0x0x7ff7a42aff00+79264]
	(No symbol) [0x0x7ff7a4069e5a]
	(No symbol) [0x0x7ff7a40ae26f]
	(No symbol) [0x0x7ff7a40ad2bb]
	(No symbol) [0x0x7ff7a40a68ed]
	(No symbol) [0x0x7ff7a40a2b1d]
	(No symbol) [0x0x7ff7a40f67de]
	(No symbol) [0x0x7ff7a40f5f70]
	(No symbol) [0x0x7ff7a40e8743]
	(No symbol) [0x0x7ff7a40b14c1]
	(No symbol) [0x0x7ff7a40b2253]
	GetHandleVerifier [0x0x7ff7a457a2dd+3004797]
	GetHandleVerifier [0x0x7ff7a457472d+2981325]
	GetHandleVerifier [0x0x7ff7a4593380+3107360]
	GetHandleVerifier [0x0x7ff7a42caa2e+188622]
	GetHandleVerifier [0x0x7ff7a42d22bf+219487]
	GetHandleVerifier [0x0x7ff7a42b8df4+115860]
	GetHandleVerifier [0x0x7ff7a42b8fa9+116297]
	GetHandleVerifier [0x0x7ff7a429f558+11256]
	BaseThreadInitThunk [0x0x7ff976dce8d7+23]
	RtlUserThreadStart [0x0x7ff977fe8d9c+44]

```

**Acciones principales:** Abrir Navegador En Login, Open Browser, Maximize Browser Window, Set Selenium Timeout, Wait Until Page Contains...

#### 🔴 Login With Empty Fields

**Tiempo de ejecución:** N/A

**Error:** ```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 137
Current browser version is 140.0.7339.128 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
Stacktrace:
	GetHandleVerifier [0x0x7ff7a42afea5+79173]
	GetHandleVerifier [0x0x7ff7a42aff00+79264]
	(No symbol) [0x0x7ff7a4069e5a]
	(No symbol) [0x0x7ff7a40ae26f]
	(No symbol) [0x0x7ff7a40ad2bb]
	(No symbol) [0x0x7ff7a40a68ed]
	(No symbol) [0x0x7ff7a40a2b1d]
	(No symbol) [0x0x7ff7a40f67de]
	(No symbol) [0x0x7ff7a40f5f70]
	(No symbol) [0x0x7ff7a40e8743]
	(No symbol) [0x0x7ff7a40b14c1]
	(No symbol) [0x0x7ff7a40b2253]
	GetHandleVerifier [0x0x7ff7a457a2dd+3004797]
	GetHandleVerifier [0x0x7ff7a457472d+2981325]
	GetHandleVerifier [0x0x7ff7a4593380+3107360]
	GetHandleVerifier [0x0x7ff7a42caa2e+188622]
	GetHandleVerifier [0x0x7ff7a42d22bf+219487]
	GetHandleVerifier [0x0x7ff7a42b8df4+115860]
	GetHandleVerifier [0x0x7ff7a42b8fa9+116297]
	GetHandleVerifier [0x0x7ff7a429f558+11256]
	BaseThreadInitThunk [0x0x7ff976dce8d7+23]
	RtlUserThreadStart [0x0x7ff977fe8d9c+44]

```

**Acciones principales:** Abrir Navegador En Login, Open Browser, Maximize Browser Window, Set Selenium Timeout, Wait Until Page Contains...

#### 🔴 Login With Invalid Username

**Tiempo de ejecución:** N/A

**Error:** ```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 137
Current browser version is 140.0.7339.128 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
Stacktrace:
	GetHandleVerifier [0x0x7ff7a42afea5+79173]
	GetHandleVerifier [0x0x7ff7a42aff00+79264]
	(No symbol) [0x0x7ff7a4069e5a]
	(No symbol) [0x0x7ff7a40ae26f]
	(No symbol) [0x0x7ff7a40ad2bb]
	(No symbol) [0x0x7ff7a40a68ed]
	(No symbol) [0x0x7ff7a40a2b1d]
	(No symbol) [0x0x7ff7a40f67de]
	(No symbol) [0x0x7ff7a40f5f70]
	(No symbol) [0x0x7ff7a40e8743]
	(No symbol) [0x0x7ff7a40b14c1]
	(No symbol) [0x0x7ff7a40b2253]
	GetHandleVerifier [0x0x7ff7a457a2dd+3004797]
	GetHandleVerifier [0x0x7ff7a457472d+2981325]
	GetHandleVerifier [0x0x7ff7a4593380+3107360]
	GetHandleVerifier [0x0x7ff7a42caa2e+188622]
	GetHandleVerifier [0x0x7ff7a42d22bf+219487]
	GetHandleVerifier [0x0x7ff7a42b8df4+115860]
	GetHandleVerifier [0x0x7ff7a42b8fa9+116297]
	GetHandleVerifier [0x0x7ff7a429f558+11256]
	BaseThreadInitThunk [0x0x7ff976dce8d7+23]
	RtlUserThreadStart [0x0x7ff977fe8d9c+44]

```

**Acciones principales:** Cargar Configuracion Central, Obtener Estado Biblioteca, Get From Dictionary, Run Keyword If, Log...

#### 🔴 Login With Generated Invalid Credentials

**Tiempo de ejecución:** N/A

**Error:** ```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 137
Current browser version is 140.0.7339.128 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
Stacktrace:
	GetHandleVerifier [0x0x7ff7a42afea5+79173]
	GetHandleVerifier [0x0x7ff7a42aff00+79264]
	(No symbol) [0x0x7ff7a4069e5a]
	(No symbol) [0x0x7ff7a40ae26f]
	(No symbol) [0x0x7ff7a40ad2bb]
	(No symbol) [0x0x7ff7a40a68ed]
	(No symbol) [0x0x7ff7a40a2b1d]
	(No symbol) [0x0x7ff7a40f67de]
	(No symbol) [0x0x7ff7a40f5f70]
	(No symbol) [0x0x7ff7a40e8743]
	(No symbol) [0x0x7ff7a40b14c1]
	(No symbol) [0x0x7ff7a40b2253]
	GetHandleVerifier [0x0x7ff7a457a2dd+3004797]
	GetHandleVerifier [0x0x7ff7a457472d+2981325]
	GetHandleVerifier [0x0x7ff7a4593380+3107360]
	GetHandleVerifier [0x0x7ff7a42caa2e+188622]
	GetHandleVerifier [0x0x7ff7a42d22bf+219487]
	GetHandleVerifier [0x0x7ff7a42b8df4+115860]
	GetHandleVerifier [0x0x7ff7a42b8fa9+116297]
	GetHandleVerifier [0x0x7ff7a429f558+11256]
	BaseThreadInitThunk [0x0x7ff976dce8d7+23]
	RtlUserThreadStart [0x0x7ff977fe8d9c+44]

```

**Acciones principales:** Cargar Configuracion Central, Obtener Estado Biblioteca, Get From Dictionary, Run Keyword If, Log...

#### 🔴 Login With Multiple Environment Credentials

**Tiempo de ejecución:** N/A

**Error:** ```
TypeError: Expected argument 1 to be a dictionary, got string instead.
```

**Acciones principales:** Cargar Configuracion Central, Obtener Estado Biblioteca, Get From Dictionary, Run Keyword If, Log...

#### 🔴 Validar Sistema Configuracion Centralizada

**Tiempo de ejecución:** N/A

**Error:** ```
ConfigManager no está disponible
```

**Acciones principales:** Cargar Configuracion Central, Obtener Estado Biblioteca, Get From Dictionary, Run Keyword If, Log...

## 🤖 Recomendaciones de IA para Tests Fallidos

A continuación se presentan sugerencias generadas con IA para solucionar los problemas encontrados:

### 🔍 Test: Login With Valid Credentials

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports...`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Login Interface Validation

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports...`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Login With Empty Fields

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports...`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Login With Invalid Username

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports...`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Login With Generated Invalid Credentials

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports...`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Login With Multiple Environment Credentials

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `TypeError: Expected argument 1 to be a dictionary, got string instead.`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

### 🔍 Test: Validar Sistema Configuracion Centralizada

**🎯 Causa probable:** Error no categorizado automáticamente

**📋 Categoría:** `general`

**❌ Error detectado:** `ConfigManager no está disponible`

**🛠️ Recomendaciones:**
1. Revisar el log completo para más detalles
2. Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)
3. Verificar si ha habido cambios recientes en la aplicación
4. Comprobar la configuración del entorno de pruebas

## 📚 Recursos Adicionales

- [Informe HTML Detallado](./log.html)
- [Reporte General de Robot Framework](./report.html)
- [Capturas de Pantalla](./screenshots)
- [Análisis de IA con Gemini](./ai_analysis)

---

*Informe generado automáticamente por RobotFramework-Gemini-Demo con Gemini AI - 2025-09-25*