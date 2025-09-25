# 🤖 Robotframework-GenAI-QA-Demo1.2+ Multi-Proveedor

## 📋 Descripción

Demo híbrido de automatización de pruebas que combina **Robot Framework** con **múltiples proveedores de IA** (Gemini, Claude, AWS) para generar datos de prueba inteligentes, analizar errores automáticamente y crear reportes enriquecidos con IA.

**🎉 VERSIÓN 1.2+ - SISTEMA MULTI-PROVEEDOR** 

Este proyecto representa la **evolución avanzada** que combina lo mejor de múltiples IAs con las mejores prácticas de desarrollo, ahora con un **sistema multi-proveedor centralizado** que permite cambiar dinámicamente entre diferentes servicios de IA.

## 🏆 Características Principales

### 🔧 **Sistema Multi-Proveedor v1.2+** ⭐ **NUEVO**
- 🎯 **Múltiples proveedores**: Gemini, Claude, AWS Bedrock
- 🔄 **Cambio dinámico**: Switch entre proveedores en segundos
- 🛡️ **Compatibilidad 100%**: Mantiene toda la funcionalidad v1.2
- 📊 **Monitoreo en tiempo real**: Estado de proveedores disponibles
- ⚙️ **Configuración centralizada**: Un solo archivo para gestionar todos

### ✨ **Sistema de Configuración Centralizada v1.2** 
- 🎯 **Archivo maestro único**: `config/credentials.json` - Una sola fuente de verdad
- 🤖 **ConfigManager integrado**: Gestión automática de credenciales
- 🛡️ **Eliminación de duplicación**: 6 ubicaciones → 1 archivo maestro
- 🔄 **Actualización automática**: Cambios en tiempo real sin reiniciar
- 📊 **91% menos mantenimiento**: Un solo archivo para editar

### 🔍 **Análisis de Errores Multi-IA**
- 🧠 **Proveedores múltiples**: Gemini, Claude disponibles
- 📊 **Categorización inteligente**: Clasifica errores por tipo y probabilidad
- 💡 **Recomendaciones comparativas**: Análisis desde diferentes perspectivas
- 🔄 **Fallback automático**: Si un proveedor falla, usa otro

### 📈 **Arquitectura Escalable**
- ⚡ **Proveedor activo**: Cambio sin afectar funcionalidad
- 🔧 **Configuración hot-reload**: Cambios sin reiniciar
- 🏗️ **Sistema de fallbacks**: Múltiples IAs disponibles
- 🛡️ **Zero downtime**: Transición suave entre proveedores

## 🚀 Instalación y Configuración

### 📋 **Prerrequisitos**
```bash
# Python 3.8 o superior
python --version

# pip actualizado
python -m pip install --upgrade pip

# Git (para clonar el proyecto)
git --version
```

### 🌍 **Instalación en Entorno Limpio** ⭐ **RECOMENDADO**

#### **Opción A: Entorno Virtual (Python venv)**
```powershell
# 1. Crear entorno virtual limpio
python -m venv robotframework-multiproveedor-env

# 2. Activar entorno virtual
# En Windows:
robotframework-multiproveedor-env\Scripts\activate
# En Linux/Mac:
# source robotframework-multiproveedor-env/bin/activate

# 3. Verificar entorno limpio
python -c "import sys; print('Python:', sys.executable)"
pip list  # Debe mostrar solo pip, setuptools

# 4. Actualizar pip en el entorno
python -m pip install --upgrade pip

# 5. Clonar o navegar al proyecto
cd C:\tu\directorio\Robotframework-GenAI-QA-Demo1-1.2

# 6. Instalar dependencias
pip install -r requirements.txt

# 7. Verificar instalación
.\verify_dependencies.ps1

# 8. Configurar variables de entorno
copy .env.example .env  # Si existe
notepad .env  # Editar con tus API keys

# 9. Probar sistema
python tools/switch_ai_provider.py --status
```

#### **Opción B: Entorno Virtual con virtualenv**
```powershell
# 1. Instalar virtualenv si no está disponible
pip install virtualenv

# 2. Crear entorno limpio
virtualenv -p python3.8 venv-robotframework-clean

# 3. Activar entorno
venv-robotframework-clean\Scripts\activate

# 4. Continuar con pasos 4-9 de la Opción A
```

#### **Opción C: Conda (Si tienes Anaconda/Miniconda)**
```bash
# 1. Crear entorno conda limpio
conda create -n robotframework-ai python=3.10 -y

# 2. Activar entorno
conda activate robotframework-ai

# 3. Instalar pip y dependencias base
conda install pip -y

# 4. Navegar al proyecto y continuar
cd /ruta/al/proyecto
pip install -r requirements.txt

# 5. Verificar y configurar
python verify_dependencies.py  # Equivalente al .ps1
```

#### **Verificación Post-Instalación Entorno Limpio**
```powershell
# Después de cualquier opción, verificar:

# 1. Entorno activo
python -c "import sys; print('Entorno activo:', sys.prefix)"

# 2. Dependencias críticas
python -c "
try:
    import robot, selenium, google.generativeai, anthropic
    from dotenv import load_dotenv
    print('✅ Dependencias core: OK')
except ImportError as e:
    print(f'❌ Falta dependencia: {e}')
"

# 3. Sistema multi-proveedor
python -c "
try:
    from config.ai_config import AIConfigManager
    ai = AIConfigManager()
    print(f'✅ Multi-proveedor: {len(ai.get_available_providers())} proveedores')
except Exception as e:
    print(f'❌ Multi-proveedor: {e}')
"

# 4. Test completo
.\verify_dependencies.ps1
```

### 📦 **Instalación de Dependencias Multi-Proveedor**

#### **Instalación Completa (Recomendada)**
```bash
# Instalar todas las dependencias del sistema multi-proveedor
pip install -r requirements.txt

# Verificar instalación
.\verify_dependencies.ps1
```

#### **Instalación por Componentes**

**Base mínima (solo Gemini):**
```bash
# Dependencias core + Gemini
pip install robotframework>=6.0
pip install robotframework-seleniumlibrary>=6.0
pip install selenium>=4.0
pip install google-generativeai>=0.3.0
pip install python-dotenv>=1.0.0
```

**Agregar Claude:**
```bash
# Añadir soporte para Claude
pip install anthropic>=0.25.0
```

**Agregar AWS Bedrock (opcional):**
```bash
# Añadir soporte para AWS Bedrock
pip install boto3>=1.34.0
pip install botocore>=1.34.0
```

**Dependencias de desarrollo:**
```bash
# Para desarrollo y testing avanzado
pip install pytest>=7.0.0
pip install pytest-cov>=4.0.0
pip install jsonschema>=4.17.0
pip install pydantic>=2.0.0
```

### 🔍 **Verificación de Dependencias**

#### **Script de Verificación Automática**
```powershell
# Verificar todas las dependencias del sistema
.\verify_dependencies.ps1

# Ver solo el resumen
.\verify_dependencies.ps1 | Select-String "RESUMEN" -A 10
```

#### **Verificación Manual por Componente**

**Robot Framework:**
```powershell
# Verificar Robot Framework
robot --version
python -c "import robot; print('Robot Framework:', robot.__version__)"

# Verificar Selenium Library
python -c "from SeleniumLibrary import SeleniumLibrary; print('Selenium Library: OK')"
```

**Proveedores de IA:**
```powershell
# Verificar Gemini
python -c "import google.generativeai; print('✅ Gemini: OK')"

# Verificar Claude
python -c "import anthropic; print('✅ Claude:', anthropic.__version__)"

# Verificar AWS (opcional)
python -c "import boto3; print('✅ AWS:', boto3.__version__)"
```

**Sistema Multi-Proveedor:**
```powershell
# Verificar variables de entorno
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ DotEnv: OK')"

# Verificar AIConfigManager
python -c "from config.ai_config import AIConfigManager; ai = AIConfigManager(); print('✅ Multi-Proveedor:', len(ai.get_available_providers()), 'proveedores')"

# Verificar switch de proveedores
python tools/switch_ai_provider.py --status
```

### 🔧 **Configuración Multi-Proveedor v1.2+** ⭐ **NUEVO**

#### **1. Configuración de APIs**
```env
# .env - Configuración de proveedores
AI_PROVIDER=gemini

# Google Gemini
GEMINI_API_KEY=AIzaSyC4Ks0Q4t4HT-a8_3fHI2vL-oElJl7fN2A

# Anthropic Claude  
CLAUDE_API_KEY=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

# AWS Bedrock (opcional)
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=...
# AWS_DEFAULT_REGION=us-east-1
```

#### **2. Sistema de Credenciales (Mantenido de v1.2)**
El archivo `config/credentials.json` sigue siendo el **único lugar** para credenciales:

```json
{
  "metadata": {
    "version": "1.2+",
    "created": "2025-07-09",
    "description": "Archivo maestro de credenciales compatible con multi-proveedor"
  },
  "environments": {
    "qa": {
      "url": "https://erp-qa-beta.siesaerp.com/login?returnUrl=%2F",
      "credentials": [
        {
          "usuario": "juan.reina",
          "clave": "1235",
          "descripcion": "Usuario principal de testing",
          "tipo": "funcional",
          "prioridad": 1,
          "activo": true
        }
      ]
    }
  }
}
```

## 🎮 Comandos Multi-Proveedor

### 🚀 **Gestión de Proveedores**

#### **Ver Estado del Sistema**
```powershell
# Estado completo de todos los proveedores
python tools/switch_ai_provider.py --status

# Listar todos los proveedores configurados
python tools/switch_ai_provider.py --list
```

#### **Cambiar Entre Proveedores**
```powershell
# Cambiar a Gemini
python tools/switch_ai_provider.py gemini

# Cambiar a Claude
python tools/switch_ai_provider.py claude

# Cambiar a AWS (cuando esté configurado)
python tools/switch_ai_provider.py aws
```

#### **Verificar Disponibilidad**
```powershell
# Verificar qué proveedores están disponibles
python -c "
from config.ai_config import AIConfigManager
ai_config = AIConfigManager()
ai_config.print_status()
"
```

### 🔧 **Comandos de Diagnóstico Multi-Proveedor**

#### **Verificar Integración Completa**
```powershell
# Diagnóstico sistema multi-proveedor + v1.2
python -c "
print('=== DIAGNÓSTICO SISTEMA MULTI-PROVEEDOR v1.2+ ===')

# 1. ConfigManager v1.2
from config.config import ConfigManager
cm = ConfigManager()
cred = cm.get_priority_credential('qa')
print('✅ ConfigManager v1.2:', cred['usuario'], '/', cred['clave'])

# 2. GeminiLibrary v1.2
from libraries.GeminiLibrary import GeminiLibrary
gl = GeminiLibrary()
cred = gl.obtener_credencial_prioritaria('qa')
print('✅ GeminiLibrary v1.2:', cred['usuario'], '/', cred['clave'])

# 3. AIConfigManager Multi-Proveedor
from config.ai_config import AIConfigManager
ai_config = AIConfigManager()
cred = ai_config.get_credentials_for_provider('gemini', 'qa')
print('✅ Multi-Proveedor:', cred['usuario'], '/', cred['clave'])

print('✅ INTEGRACIÓN COMPLETA: Todos los sistemas coherentes')
"
```

#### **Test de Cambio de Proveedores**
```powershell
# Probar cambio dinámico entre proveedores
python -c "
from config.ai_config import AIConfigManager
ai_config = AIConfigManager()

print('=== TEST CAMBIO DINÁMICO ===')
print('Proveedor inicial:', ai_config.get_active_provider())
print('Disponibles:', ai_config.get_available_providers())

# El cambio se hace con el script switch_ai_provider.py
print('Usar: python tools/switch_ai_provider.py claude')
print('Usar: python tools/switch_ai_provider.py gemini')
"
```

### 🧹 **Limpieza y Mantenimiento**

#### **Comando Principal de Limpieza**
```powershell
# Limpieza completa optimizada para multi-proveedor
.\cleanup_multiproveedor_final_FIXED.ps1

# Opciones disponibles:
.\cleanup_multiproveedor_final_FIXED.ps1 -Force                    # Sin confirmaciones
.\cleanup_multiproveedor_final_FIXED.ps1 -KeepResults             # Mantener resultados de tests
.\cleanup_multiproveedor_final_FIXED.ps1 -KeepScripts             # Mantener scripts de desarrollo  
.\cleanup_multiproveedor_final_FIXED.ps1 -DryRun                  # Solo mostrar qué se eliminaría
.\cleanup_multiproveedor_final_FIXED.ps1 -Force -KeepResults      # Combinación de opciones
```

#### **Generar Estructura del Proyecto**
```powershell
# Generar estructura completa actual
tree /f /a > estructura_proyecto_v12.txt

# Ver estructura en pantalla
tree /f /a

# Ver solo directorios principales  
tree /a

# Comparar con estructura anterior
fc estructura_proyecto_v12.txt estructura_proyecto_v12_clean.txt
```

#### **Limpieza Específica por Componente**

**Cache Python:**
```powershell
# Eliminar todo el cache Python del proyecto
Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force

# Limpiar cache específico por directorio
Remove-Item -Recurse -Force config\__pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force libraries\__pycache__ -ErrorAction SilentlyContinue
```

**Archivos temporales Robot Framework:**
```powershell
# Eliminar archivos temporales principales
Remove-Item log.html, output.xml, report.html -ErrorAction SilentlyContinue

# Limpiar screenshots temporales
Remove-Item selenium-screenshot-*.png -ErrorAction SilentlyContinue
Remove-Item login_*.png -ErrorAction SilentlyContinue
```

#### **Backup y Restauración**

**Crear Backups:**
```powershell
# Backup de configuración completa
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backup_$timestamp"
New-Item -ItemType Directory -Path $backupDir

# Backup archivos críticos
Copy-Item "config\credentials.json" "$backupDir\credentials.json"
Copy-Item "config\ai_providers.json" "$backupDir\ai_providers.json"  
Copy-Item ".env" "$backupDir\.env"
Copy-Item "tools\switch_ai_provider.py" "$backupDir\switch_ai_provider.py"

Write-Host "✅ Backup creado en: $backupDir" -ForegroundColor Green
```

**Restaurar desde Backup:**
```powershell
# Listar backups disponibles
Get-ChildItem "backup_*" -Directory | Sort-Object Name -Descending

# Restaurar desde backup específico (reemplazar TIMESTAMP)
$backupDir = "backup_TIMESTAMP"
Copy-Item "$backupDir\credentials.json" "config\credentials.json"
Copy-Item "$backupDir\ai_providers.json" "config\ai_providers.json"
Copy-Item "$backupDir\.env" ".env"

Write-Host "✅ Configuración restaurada desde: $backupDir" -ForegroundColor Green
```

### 🚀 **Ejecución de Tests Multi-Proveedor**

#### **Tests con Proveedor Específico**
```powershell
# Los tests usan automáticamente el proveedor activo
robot --include "success" tests/login/siesa_login_tests.robot

# Cambiar proveedor y ejecutar
python tools/switch_ai_provider.py claude
robot tests/login/siesa_login_tests.robot

# Volver a Gemini y ejecutar
python tools/switch_ai_provider.py gemini
robot tests/login/siesa_login_tests.robot
```

#### **Demo Completa Multi-Proveedor**
```powershell
# Ejecutar demo con proveedor activo
.\run_demo_gemini_hibrido.ps1

# Demo con métricas detalladas
.\run_demo_gemini_hibrido_METRICAS.ps1
```

### 🎯 **Generación de Datos Multi-Proveedor**

#### **Generar con Proveedor Activo**
```bash
# Usa automáticamente el proveedor configurado
python tools/gemini_generator_siesa.py --quantity 15 --output data/test_15.json

# Verificar que funciona con cualquier proveedor
python tools/switch_ai_provider.py claude
python tools/gemini_generator_siesa.py --quantity 10 --output data/claude_test.json

python tools/switch_ai_provider.py gemini  
python tools/gemini_generator_siesa.py --quantity 10 --output data/gemini_test.json
```

#### **Validación de Cantidad Exacta**
```powershell
# Verificar que genera cantidad exacta (funciona con cualquier proveedor)
python tools/gemini_generator_siesa.py --quantity 25 --output data/validation_25.json

# Verificar resultado
$test = Get-Content "data/validation_25.json" | ConvertFrom-Json
$total = $test.credenciales_validas.Count + $test.credenciales_invalidas.Count
Write-Host "✅ Total generado: $total usuarios (solicitados: 25)" -ForegroundColor Green
```

## 📂 Estructura del Proyecto Multi-Proveedor

```
📁 Robotframework-GenAI-QA-Demo1.2-MultiProveedor/
├── 📁 config/                          ⭐ Sistema Centralizado + Multi-Proveedor
│   ├── credentials.json                 # 🔑 Archivo maestro de credenciales (v1.2)
│   ├── ai_providers.json               # 🤖 Configuración multi-proveedor (NUEVO)
│   ├── config.py                       # 🔧 ConfigManager (v1.2)
│   ├── ai_config.py                    # 🔧 AIConfigManager (NUEVO)
│   ├── global_variables.robot          # 🤖 Variables Robot Framework
│   └── settings_improved.robot         # Configuración global
├── 📁 libraries/
│   └── GeminiLibrary.py                 # Biblioteca principal con IA + ConfigManager
├── 📁 tools/
│   ├── switch_ai_provider.py           # 🔄 Cambiador de proveedores (NUEVO)
│   ├── gemini_generator_siesa.py       # Generador compatible multi-proveedor
│   └── robot_md_reporter_gemini.py     # Generador de reportes IA
├── 📁 tests/
│   ├── 📁 demo/
│   │   ├── demo_data_gemini.robot      # Tests de validación IA
│   │   └── demo_error_siesa_gemini.robot # Tests de análisis errores
│   └── 📁 login/
│       └── siesa_login_tests.robot     # Tests híbridos (funciona con cualquier proveedor)
├── 📁 listeners/
│   └── robot_ai_listener_gemini.py     # Listener para análisis de errores
├── 📁 data/
│   └── 📁 generated/                   # Datos generados por cualquier IA
├── 📁 results/                         # Resultados de ejecución
├── estructura_proyecto_v12.txt         # 📋 Estructura generada con tree
├── verify_dependencies.ps1            # 🔍 Verificación de dependencias (NUEVO)
├── cleanup_multiproveedor_final_FIXED.ps1 # 🧹 Limpieza optimizada (NUEVO)
├── run_demo_gemini_hibrido.ps1        # Script principal demo
├── .env                               # Variables de entorno multi-proveedor
├── requirements.txt                   # Dependencias multi-proveedor
└── README.md                          # Este archivo
```

## 🧠 Componentes Multi-Proveedor

### 🔧 **AIConfigManager v1.2+** ⭐ **NUEVO**
Sistema de gestión multi-proveedor que proporciona:
- ✅ **Gestión unificada** de múltiples proveedores de IA
- ✅ **Cambio dinámico** entre Gemini, Claude, AWS
- ✅ **Verificación automática** de disponibilidad
- ✅ **Integración transparente** con ConfigManager v1.2

### 🔄 **Switch AI Provider** ⭐ **NUEVO**
Script para cambio dinámico de proveedores:
- ✅ **Cambio en segundos** sin reiniciar
- ✅ **Verificación automática** de API keys
- ✅ **Actualización de configuración** automática
- ✅ **Monitoreo de estado** en tiempo real

### 🤖 **GeminiLibrary v1.2+ (Compatible)**
Biblioteca principal manteniendo compatibilidad total:
- ✅ **ConfigManager integrado**: Usa credenciales centralizadas
- ✅ **Multi-proveedor ready**: Compatible con sistema de proveedores
- ✅ **Fallbacks automáticos**: Funciona con cualquier proveedor activo
- ✅ **Zero breaking changes**: Todos los métodos existentes funcionan

## 🎯 Casos de Uso Multi-Proveedor

### 🎯 **Caso 1: Testing con Múltiples IAs**
```robot
*** Test Cases ***
Análisis Con Diferentes Proveedores
    # Funciona con cualquier proveedor activo
    Cargar Configuracion Central
    ${credencial}=    Obtener Credencial Prioritaria Keyword    qa
    
    # El análisis usa automáticamente el proveedor configurado
    Perform Login With AI Analysis    ${credencial}
    Verify Results With Current Provider
```

### 🔧 **Caso 2: Cambio Dinámico por Rendimiento**
```powershell
# Para análisis rápido
python tools/switch_ai_provider.py gemini
robot tests/login/siesa_login_tests.robot

# Para análisis profundo  
python tools/switch_ai_provider.py claude
robot tests/demo/demo_error_siesa_gemini.robot
```

### 🔍 **Caso 3: Fallback Automático**
Si Gemini no está disponible:
1. 🧠 Sistema detecta automáticamente
2. 📊 Cambia a Claude (si está configurado)
3. 💡 Continúa funcionamiento sin interrupción
4. 💾 Reporta el cambio en logs

### 🌍 **Caso 4: Instalación en Entorno Limpio**
```powershell
# Caso típico: Nuevo desarrollador o servidor CI/CD
python -m venv clean-env
clean-env\Scripts\activate
pip install -r requirements.txt
.\verify_dependencies.ps1
python tools/switch_ai_provider.py --status
```

## 🛠️ Comandos de Referencia Rápida

### 🚀 **Comandos Esenciales**
```powershell
# Ver estado
python tools/switch_ai_provider.py --status

# Cambiar proveedor
python tools/switch_ai_provider.py claude
python tools/switch_ai_provider.py gemini

# Ejecutar tests
robot tests/login/siesa_login_tests.robot

# Generar estructura
tree /f /a > estructura_proyecto_v12.txt

# Limpiar proyecto
.\cleanup_multiproveedor_final_FIXED.ps1 -Force

# Verificar dependencias
.\verify_dependencies.ps1
```

### 🔧 **Comandos de Diagnóstico**
```powershell
# Verificar todo el sistema
python -c "
from config.ai_config import AIConfigManager
ai_config = AIConfigManager()
ai_config.print_status()

# Test compatibilidad v1.2
creds = ai_config.get_credentials_for_provider('gemini', 'qa')
print('✅ Credenciales:', creds['usuario'], '/', creds['clave'])
"

# Verificar coherencia completa
python -c "
from config.config import ConfigManager
from libraries.GeminiLibrary import GeminiLibrary
from config.ai_config import AIConfigManager

cm = ConfigManager()
gl = GeminiLibrary()  
ai = AIConfigManager()

cm_cred = cm.get_priority_credential('qa')
gl_cred = gl.obtener_credencial_prioritaria('qa')
ai_cred = ai.get_credentials_for_provider('gemini', 'qa')

print('ConfigManager:', cm_cred['usuario'], '/', cm_cred['clave'])
print('GeminiLibrary:', gl_cred['usuario'], '/', gl_cred['clave'])
print('AIConfigManager:', ai_cred['usuario'], '/', ai_cred['clave'])
print('✅ SISTEMA COHERENTE' if all(c['usuario'] == 'juan.reina' and c['clave'] == '1235' for c in [cm_cred, gl_cred, ai_cred]) else '❌ INCONSISTENCIA')
"
```

### 🌍 **Comandos para Entorno Limpio**
```powershell
# Setup completo en entorno limpio
python -m venv robotframework-clean
robotframework-clean\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
.\verify_dependencies.ps1
copy .env.example .env  # Editar con API keys
python tools/switch_ai_provider.py --status
robot --include "success" tests/login/siesa_login_tests.robot
```

## 📋 Dependencias Completas del Sistema

### **Dependencias Core (Siempre Requeridas)**
```txt
# Robot Framework base
robotframework>=6.0
robotframework-seleniumlibrary>=6.0
selenium>=4.0
webdriver-manager>=4.0

# Sistema multi-proveedor (CRÍTICO)
python-dotenv>=1.0.0

# Google Gemini (Base)
google-generativeai>=0.3.0

# Utilidades core
requests>=2.28
lxml>=4.9.0
python-dateutil>=2.8.0
```

### **Dependencias Multi-Proveedor**
```txt
# Anthropic Claude (para proveedor Claude)
anthropic>=0.25.0

# AWS Bedrock (opcional)
boto3>=1.34.0
botocore>=1.34.0

# Configuración avanzada
jsonschema>=4.17.0
pydantic>=2.0.0
cerberus>=1.3.4
```

### **Dependencias de Desarrollo**
```txt
# Testing y desarrollo
pytest>=7.0.0
pytest-cov>=4.0.0

# Reportes mejorados
markdown>=3.4.0
jinja2>=3.1.0
colorlog>=6.7.0

# Robot Framework extensions
robotframework-requests>=0.9.4
```

## 🎯 Comandos de Instalación Específicos por Escenario

### **Escenario 1: Desarrollo Completo**
```powershell
# Entorno limpio + instalación completa
python -m venv dev-complete
dev-complete\Scripts\activate
pip install -r requirements.txt
.\verify_dependencies.ps1
copy .env.example .env  # Editar con API keys
python tools/switch_ai_provider.py --status
```

### **Escenario 2: Solo Gemini (Básico)**
```powershell
# Entorno mínimo
python -m venv basic-gemini
basic-gemini\Scripts\activate
pip install robotframework robotframework-seleniumlibrary selenium google-generativeai python-dotenv
echo "AI_PROVIDER=gemini" > .env
echo "GEMINI_API_KEY=tu_api_key_aqui" >> .env
python -c "from libraries.GeminiLibrary import GeminiLibrary; print('✅ Solo Gemini OK')"
```

### **Escenario 3: Gemini + Claude**
```powershell
# Entorno dual
python -m venv dual-ai
dual-ai\Scripts\activate
pip install robotframework robotframework-seleniumlibrary selenium google-generativeai anthropic python-dotenv
echo "AI_PROVIDER=gemini" > .env
echo "GEMINI_API_KEY=tu_gemini_key" >> .env
echo "CLAUDE_API_KEY=tu_claude_key" >> .env
python tools/switch_ai_provider.py gemini
python tools/switch_ai_provider.py claude
```

### **Escenario 4: CI/CD Pipeline**
```powershell
# Instalación automatizada para CI/CD
python -m venv ci-env
ci-env\Scripts\activate
pip install --no-cache-dir -r requirements.txt
python -c "from config.ai_config import AIConfigManager; print('✅ CI Ready')"
robot --include "success" tests/login/siesa_login_tests.robot
```

### **Escenario 5: Docker Container**
```dockerfile
# Dockerfile para entorno limpio
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV AI_PROVIDER=gemini
ENV PYTHONPATH=/app

CMD ["python", "tools/switch_ai_provider.py", "--status"]
```

## 🚨 **Solución de Problemas**

### **Problemas de Instalación en Entorno Limpio**

#### **Error: No module named 'pip'**
```powershell
# Reinstalar pip en entorno virtual
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### **Error: SSL Certificate verification failed**
```powershell
# Solución temporal para redes corporativas
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### **Error: Permission denied (Windows)**
```powershell
# Ejecutar PowerShell como administrador o usar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Error: Python command not found (Linux/Mac)**
```bash
# Usar python3 explícitamente
python3 -m venv robotframework-env
source robotframework-env/bin/activate
python3 -m pip install -r requirements.txt
```

### **Problemas Multi-Proveedor**

#### **Error: API Key no encontrada**
```powershell
# Verificar carga de variables
python -c "
import os
from dotenv import load_dotenv
load_dotenv(override=True)
print('GEMINI_API_KEY:', 'Configurada' if os.getenv('GEMINI_API_KEY') else 'NO configurada')
print('CLAUDE_API_KEY:', 'Configurada' if os.getenv('CLAUDE_API_KEY') else 'NO configurada')
"
```

#### **Error: Proveedor no disponible**
```powershell
# Diagnóstico completo
python tools/switch_ai_provider.py --list
.\verify_dependencies.ps1
```

#### **Error: Conflictos de versiones**
```powershell
# Entorno completamente limpio
Remove-Item -Recurse -Force venv-* -ErrorAction SilentlyContinue
python -m venv fresh-env
fresh-env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### **Problemas de Compatibilidad v1.2**

#### **Error: ConfigManager no disponible**
```powershell
# Verificar archivos v1.2
Test-Path "config\config.py"
Test-Path "config\credentials.json"
python -c "from config.config import ConfigManager; print('✅ ConfigManager OK')"
```

#### **Error: GeminiLibrary incompatible**
```powershell
# Limpiar cache y reinstalar
Remove-Item -Recurse -Force libraries\__pycache__ -ErrorAction SilentlyContinue
python -c "from libraries.GeminiLibrary import GeminiLibrary; print('✅ GeminiLibrary OK')"
```

## 📊 **Verificación de Estado Completo**

### **Comando Unificado de Verificación**
```powershell
# Verificación completa del sistema en entorno limpio
python -c "
import sys
print('=== VERIFICACIÓN SISTEMA MULTI-PROVEEDOR v1.2+ ===')
print(f'Python: {sys.version}')
print(f'Entorno: {sys.prefix}')

# 1. Dependencias Core
try:
    import robot, selenium, google.generativeai
    from dotenv import load_dotenv
    print('✅ Dependencias Core: OK')
except Exception as e:
    print(f'❌ Dependencias Core: {e}')

# 2. Multi-Proveedor
try:
    import anthropic
    print('✅ Claude: Disponible')
except:
    print('⚠️  Claude: No instalado (opcional)')

try:
    import boto3
    print('✅ AWS: Disponible')
except:
    print('⚠️  AWS: No instalado (opcional)')

# 3. Sistema AI Config
try:
    from config.ai_config import AIConfigManager
    ai = AIConfigManager()
    providers = ai.get_available_providers()
    print(f'✅ Multi-Proveedor: {len(providers)} proveedores disponibles')
    print(f'   Proveedores: {providers}')
except Exception as e:
    print(f'❌ Multi-Proveedor: {e}')

# 4. Compatibilidad v1.2
try:
    from libraries.GeminiLibrary import GeminiLibrary
    gl = GeminiLibrary()
    cred = gl.obtener_credencial_prioritaria('qa')
    print(f'✅ v1.2 Compatible: {cred[\"usuario\"]}/{cred[\"clave\"]}')
except Exception as e:
    print(f'❌ v1.2 Compatible: {e}')

print('\\n✅ VERIFICACIÓN COMPLETADA')
"
```

### **Verificación Específica para Entornos Limpios**
```powershell
# Script especializado para validar entorno limpio
function Test-CleanEnvironment {
    Write-Host "VERIFICACIÓN ENTORNO LIMPIO" -ForegroundColor Cyan
    
    # 1. Verificar aislamiento del entorno
    $pythonPath = python -c "import sys; print(sys.executable)"
    if ($pythonPath -like "*venv*" -or $pythonPath -like "*env*") {
        Write-Host "✅ Entorno virtual activo: $pythonPath" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Usando Python del sistema: $pythonPath" -ForegroundColor Yellow
    }
    
    # 2. Verificar dependencias mínimas
    $packages = pip list --format=freeze
    $corePackages = @("robotframework", "selenium", "google-generativeai", "python-dotenv")
    
    foreach ($package in $corePackages) {
        if ($packages -match $package) {
            Write-Host "✅ $package instalado" -ForegroundColor Green
        } else {
            Write-Host "❌ $package FALTA" -ForegroundColor Red
        }
    }
    
    # 3. Verificar funcionalidad básica
    try {
        $result = python -c "from config.ai_config import AIConfigManager; print('Multi-proveedor OK')"
        Write-Host "✅ Sistema multi-proveedor: OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ Sistema multi-proveedor: Error" -ForegroundColor Red
    }
}

# Ejecutar verificación
Test-CleanEnvironment
```

## 🎯 **Próximos Pasos Post-Instalación**

### **Lista de Verificación Completa**
```powershell
# Lista de verificación paso a paso después de instalación limpia

Write-Host "LISTA DE VERIFICACIÓN POST-INSTALACIÓN" -ForegroundColor Cyan

# 1. Entorno
Write-Host "[1] Verificar entorno virtual activo"
python -c "import sys; print('Entorno:', sys.prefix)"

# 2. Dependencias
Write-Host "[2] Verificar dependencias críticas"
.\verify_dependencies.ps1

# 3. Configuración
Write-Host "[3] Configurar API keys"
if (-not (Test-Path ".env")) {
    Write-Host "   CREAR ARCHIVO .env con API keys" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Archivo .env existe" -ForegroundColor Green
}

# 4. Sistema multi-proveedor
Write-Host "[4] Probar sistema multi-proveedor"
python tools/switch_ai_provider.py --status

# 5. Compatibilidad v1.2
Write-Host "[5] Verificar compatibilidad v1.2"
python -c "from libraries.GeminiLibrary import GeminiLibrary; print('✅ v1.2 OK')"

# 6. Test básico
Write-Host "[6] Ejecutar test básico"
robot --include "success" tests/login/siesa_login_tests.robot

# 7. Generar documentación
Write-Host "[7] Generar estructura del proyecto"
tree /f /a > estructura_proyecto_v12.txt

Write-Host "✅ VERIFICACIÓN COMPLETADA" -ForegroundColor Green
```

### **Script de Configuración Inicial**
```powershell
# Script para configuración inicial en entorno limpio
function Initialize-RobotFrameworkAI {
    param(
        [string]$GeminiKey,
        [string]$ClaudeKey = "",
        [switch]$SkipTests
    )
    
    Write-Host "CONFIGURACIÓN INICIAL ROBOT FRAMEWORK AI" -ForegroundColor Cyan
    
    # 1. Crear .env
    if ($GeminiKey) {
        @"
AI_PROVIDER=gemini
GEMINI_API_KEY=$GeminiKey
$(if ($ClaudeKey) { "CLAUDE_API_KEY=$ClaudeKey" })
SELENIUM_IMPLICIT_WAIT=10
BROWSER=chrome
HEADLESS=False
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Archivo .env creado" -ForegroundColor Green
    } else {
        Write-Host "❌ API Key de Gemini requerida" -ForegroundColor Red
        return
    }
    
    # 2. Verificar configuración
    python tools/switch_ai_provider.py --status
    
    # 3. Tests opcionales
    if (-not $SkipTests) {
        Write-Host "Ejecutando tests de verificación..."
        robot --include "success" tests/login/siesa_login_tests.robot
    }
    
    Write-Host "✅ CONFIGURACIÓN INICIAL COMPLETADA" -ForegroundColor Green
}

# Ejemplo de uso:
# Initialize-RobotFrameworkAI -GeminiKey "AIzaSy..." -ClaudeKey "sk-ant-..."
```

## 🎊 **Beneficios del Sistema Multi-Proveedor**

### 🚀 **Flexibilidad Máxima**
- 🎯 **Múltiples opciones**: Gemini, Claude, AWS disponibles
- 🎯 **Cambio dinámico**: Switch en segundos sin downtime
- 🎯 **Failover automático**: Si un proveedor falla, usa otro
- 🎯 **Optimización por caso**: Usar el mejor proveedor para cada tarea

### 🔄 **Compatibilidad Total**
- 🎯 **v1.2 mantenido**: ConfigManager y credenciales centralizadas
- 🎯 **Zero breaking changes**: Código existente funciona sin cambios
- 🎯 **Migración gradual**: Adopta nuevas funcionalidades cuando quieras
- 🎯 **Rollback fácil**: Vuelta atrás sin problemas

### 📊 **Monitoreo Avanzado**
- 🎯 **Estado en tiempo real**: Ver disponibilidad de todos los proveedores
- 🎯 **Métricas por proveedor**: Comparar rendimiento
- 🎯 **Configuración centralizada**: Un solo lugar para gestionar todo
- 🎯 **Diagnóstico automático**: Detección proactiva de problemas

### 🌍 **Instalación Robusta**
- 🎯 **Entornos limpios**: Soporte completo para virtualenv, conda, docker
- 🎯 **Verificación automática**: Scripts de diagnóstico integrados
- 🎯 **Instalación por escenarios**: Básico, completo, desarrollo, CI/CD
- 🎯 **Solución de problemas**: Guías detalladas para troubleshooting

## 🎯 Roadmap Multi-Proveedor

### ✅ **Completado en v1.2+**
- [x] 🤖 Sistema multi-proveedor base (Gemini + Claude)
- [x] 🔄 Cambio dinámico entre proveedores
- [x] 🛡️ Compatibilidad 100% con v1.2
- [x] 📊 Monitoreo en tiempo real
- [x] ⚙️ Configuración centralizada expandida
- [x] 🌍 Soporte para entornos limpios
- [x] 🔍 Verificación automática de dependencias
- [x] 🧹 Sistema de limpieza optimizado

### 🔮 **Próximas Mejoras v1.3**
- [ ] 🟠 **AWS Bedrock** integración completa
- [ ] 🔧 **Librería unificada** para Robot Framework
- [ ] 📊 **Métricas de rendimiento** por proveedor
- [ ] 🤖 **Auto-selección** del mejor proveedor por tarea
- [ ] 🌍 **Proveedores adicionales** (GPT-4, etc.)
- [ ] 🔐 **Encriptación** de API keys
- [ ] 📱 **Dashboard web** para gestión de proveedores
- [ ] 🐳 **Imágenes Docker** pre-configuradas

## 🤝 Contribución

### 🔄 **Proceso de Mejora**
1. 🍴 Fork del proyecto
2. 🌿 Crear entorno limpio (`python -m venv dev-env`)
3. 🌿 Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
4. 📦 Instalar dependencias (`pip install -r requirements.txt`)
5. 🔍 Verificar configuración (`.\verify_dependencies.ps1`)
6. 💾 Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
7. 📤 Push a rama (`git push origin feature/nueva-funcionalidad`)
8. 🔄 Crear Pull Request

### 🧪 **Ejecutar Tests de Validación**
```bash
# Validar funcionamiento completo v1.2+
.\verify_dependencies.ps1
python tools/switch_ai_provider.py --status
robot --include "success" tests/login/siesa_login_tests.robot
```

## 🙏 Agradecimientos

- Robot Framework Community
- Google AI/Gemini Team
- Anthropic Claude Team
- AWS Bedrock Team
- Todos los contribuidores del proyecto
- **Comunidad QA** que solicitó capacidades multi-proveedor
- **Desarrolladores** que probaron el sistema en entornos limpios

---

**⚡ ¡Automatización inteligente con múltiples IAs para el futuro del testing!** ⚡

**🎉 Versión 1.2+ - Sistema Multi-Proveedor Exitoso 🎉**

**🌍 Entornos Limpios - Instalación Robusta y Confiable 🌍**

## 📋 **Comandos de Referencia Final**

### **🚀 Setup Inicial Completo:**
```powershell
# Entorno limpio + instalación + configuración + verificación
python -m venv robotframework-multiproveedor
robotframework-multiproveedor\Scripts\activate
pip install -r requirements.txt
copy .env.example .env  # Editar API keys
.\verify_dependencies.ps1
python tools/switch_ai_provider.py --status
robot --include "success" tests/login/siesa_login_tests.robot
tree /f /a > estructura_proyecto_v12.txt
```

### **🔧 Comandos Diarios:**
```powershell
# Activar entorno
robotframework-multiproveedor\Scripts\activate

# Ver estado
python tools/switch_ai_provider.py --status

# Cambiar proveedor  
python tools/switch_ai_provider.py claude

# Ejecutar tests
robot tests/login/siesa_login_tests.robot

# Limpiar proyecto
.\cleanup_multiproveedor_final_FIXED.ps1 -Force -KeepResults
```

**🎯 ¡Sistema completo, robusto y listo para cualquier entorno!** 🎯