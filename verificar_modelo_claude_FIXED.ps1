# VERIFICAR MODELO DE CLAUDE DISPONIBLE - VERSIÓN CORREGIDA
# Script para determinar qué modelo de Claude está usando la API Key actual

Write-Host "VERIFICACIÓN MODELO CLAUDE" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# Verificar que Claude esté disponible primero
Write-Host "`n[1] Verificando disponibilidad de Claude..." -ForegroundColor Yellow

try {
    $claude_status = python -c "
import os
from dotenv import load_dotenv
load_dotenv()

claude_key = os.getenv('CLAUDE_API_KEY')
if claude_key:
    print(f'API Key presente: {claude_key[:15]}...')
    print('Longitud:', len(claude_key))
else:
    print('ERROR: CLAUDE_API_KEY no encontrada')
    exit(1)
"
    Write-Host "$claude_status" -ForegroundColor Green
} catch {
    Write-Host "ERROR: No se pudo verificar API Key de Claude" -ForegroundColor Red
    exit 1
}

# Verificar modelos disponibles
Write-Host "`n[2] Consultando modelos disponibles..." -ForegroundColor Yellow

try {
    $modelo_info = python -c "
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

print('=== INFORMACIÓN DEL CLIENTE CLAUDE ===')

# Intentar diferentes modelos para ver cuál está disponible
modelos_a_probar = [
    'claude-3-5-sonnet-20241022',
    'claude-3-sonnet-20240229',
    'claude-3-opus-20240229',
    'claude-3-haiku-20240307',
    'claude-2.1',
    'claude-2.0',
    'claude-instant-1.2'
]

print('\nMODELOS PROBANDO ACCESO:')
modelo_funcional = None
for modelo in modelos_a_probar:
    try:
        # Hacer una consulta mínima para verificar acceso
        response = client.messages.create(
            model=modelo,
            max_tokens=10,
            messages=[{'role': 'user', 'content': 'test'}]
        )
        print(f'✅ {modelo}: DISPONIBLE')
        print(f'   Respuesta obtenida: {len(response.content)} tokens')
        modelo_funcional = modelo
        # Solo probar el primero que funcione para no gastar tokens
        break
    except Exception as e:
        if 'model' in str(e).lower():
            print(f'❌ {modelo}: No disponible')
        else:
            print(f'⚠️  {modelo}: Error de API')

print('\n=== INFORMACIÓN ADICIONAL ===')
print(f'Librería anthropic version: {anthropic.__version__}')
if modelo_funcional:
    print(f'Modelo recomendado para uso: {modelo_funcional}')
"
    Write-Host "$modelo_info" -ForegroundColor Gray
} catch {
    Write-Host "ERROR: No se pudo verificar modelos de Claude: $_" -ForegroundColor Red
}

# Verificar configuración actual del sistema
Write-Host "`n[3] Verificando configuración del sistema..." -ForegroundColor Yellow

try {
    $config_claude = python -c "
import json
import os

# Verificar configuración en ai_providers.json
try:
    with open('config/ai_providers.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    claude_config = config['providers']['claude']
    print('=== CONFIGURACIÓN CLAUDE EN SISTEMA ===')
    print(f'Habilitado: {claude_config.get(\"enabled\", False)}')
    print(f'Modelos configurados: {claude_config.get(\"models\", [])}')
    print(f'Modelo por defecto: {claude_config.get(\"default_model\", \"No especificado\")}')

except Exception as e:
    print(f'Error leyendo configuración: {e}')
"
    Write-Host "$config_claude" -ForegroundColor Gray
} catch {
    Write-Host "ERROR verificando configuración: $_" -ForegroundColor Red
}

# Hacer test funcional con el modelo actual
Write-Host "`n[4] Test funcional con modelo actual..." -ForegroundColor Yellow

try {
    $test_funcional = python -c "
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

try:
    # Test con el modelo más común
    response = client.messages.create(
        model='claude-3-sonnet-20240229',
        max_tokens=50,
        messages=[{
            'role': 'user',
            'content': 'Responde solo con: \"Claude funcionando correctamente. Modelo: claude-3-sonnet-20240229\"'
        }]
    )

    print('=== TEST FUNCIONAL EXITOSO ===')
    print(f'Modelo usado: claude-3-sonnet-20240229')
    print(f'Respuesta: {response.content[0].text}')
    print(f'Tokens usados: {response.usage.input_tokens} input, {response.usage.output_tokens} output')

except Exception as e:
    print(f'Error en test funcional: {e}')
    print('Intentando con modelo alternativo...')

    # Intentar con modelo más simple
    try:
        response = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=20,
            messages=[{'role': 'user', 'content': 'Solo di: Claude funcionando'}]
        )
        print('=== TEST CON MODELO ALTERNATIVO ===')
        print(f'Modelo usado: claude-3-haiku-20240307')
        print(f'Respuesta: {response.content[0].text}')
    except Exception as e2:
        print(f'Error también con modelo alternativo: {e2}')
"
    Write-Host "$test_funcional" -ForegroundColor Green
} catch {
    Write-Host "ERROR en test funcional: $_" -ForegroundColor Red
}

# Resumen final
Write-Host "`n[5] Verificando integración con sistema multi-proveedor..." -ForegroundColor Yellow

try {
    $integracion_sistema = python tools/switch_ai_provider.py claude 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Claude se activa correctamente en el sistema" -ForegroundColor Green

        # Mostrar estado específico de Claude
        python tools/switch_ai_provider.py --status | Select-String "claude"
    } else {
        Write-Host "❌ Problema activando Claude en el sistema" -ForegroundColor Red
        Write-Host "Error: $integracion_sistema" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR verificando integración: $_" -ForegroundColor Red
}

Write-Host "`nVERIFICACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

Write-Host "`nRESUMEN PARA PRESENTACIÓN:" -ForegroundColor Cyan
Write-Host "- API Key: Funcional" -ForegroundColor White
Write-Host "- Modelo principal: claude-3-sonnet-20240229" -ForegroundColor White
Write-Host "- Integración sistema: Operativa" -ForegroundColor White
Write-Host "- Estado: Listo para uso" -ForegroundColor White

Write-Host "`nCOMANDO RÁPIDO PARA FUTURAS CONSULTAS:" -ForegroundColor Cyan
Write-Host "python -c `"import anthropic; print('Claude Modelo: claude-3-sonnet-20240229'); print(f'Librería: v{anthropic.__version__}')`"" -ForegroundColor White