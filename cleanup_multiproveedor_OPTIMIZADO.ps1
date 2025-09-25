# LIMPIEZA OPTIMIZADA PARA ESTRUCTURA ACTUAL v1.2+
# Adaptado a la estructura real del proyecto según estructura_proyecto_v12.txt

param(
    [switch]$Force,           # No pedir confirmaciones
    [switch]$KeepResults,     # Mantener resultados de tests
    [switch]$KeepDocs,        # Mantener documentación adicional
    [switch]$DryRun          # Solo mostrar que se eliminaria
)

Write-Host "LIMPIEZA OPTIMIZADA PROYECTO MULTI-PROVEEDOR v1.2+" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "MODO DRY-RUN: Solo mostrando archivos a eliminar" -ForegroundColor Yellow
}

# Funcion para eliminar archivos de forma segura
function Remove-SafelyWithConfirm {
    param(
        [string]$Path,
        [string]$Description,
        [switch]$IsDirectory
    )

    if (Test-Path $Path) {
        if ($DryRun) {
            Write-Host "   [DRY-RUN] $Description : $Path" -ForegroundColor Gray
            return
        }

        if (-not $Force) {
            $response = Read-Host "Eliminar $Description ($Path)? (s/N)"
            if ($response -notmatch '^[sS]$') {
                Write-Host "   Omitido: $Description" -ForegroundColor Yellow
                return
            }
        }

        try {
            if ($IsDirectory) {
                Remove-Item -Path $Path -Recurse -Force
            } else {
                Remove-Item -Path $Path -Force
            }
            Write-Host "   OK Eliminado: $Description" -ForegroundColor Green
        } catch {
            Write-Host "   ERROR eliminando $Description : $_" -ForegroundColor Red
        }
    } else {
        Write-Host "   INFO No existe: $Description" -ForegroundColor Gray
    }
}

Write-Host "`nAnalizando estructura actual del proyecto..." -ForegroundColor Yellow

# ARCHIVOS A MANTENER SIEMPRE (CORE DEL SISTEMA)
$archivos_core = @(
    "config\ai_config.py",
    "config\ai_providers.json",
    "config\config.py",
    "config\credentials.json",
    "libraries\GeminiLibrary.py",
    "tools\switch_ai_provider.py",
    "tools\gemini_generator_siesa.py",
    ".env",
    "requirements.txt"
)

Write-Host "Archivos CORE que se mantendran:" -ForegroundColor Green
foreach ($file in $archivos_core) {
    if (Test-Path $file) {
        Write-Host "   OK $file" -ForegroundColor Green
    } else {
        Write-Host "   WARNING $file (no encontrado)" -ForegroundColor Yellow
    }
}

# 1. LIMPIEZA DE CACHE PYTHON
Write-Host "`n[1] Limpiando cache Python..." -ForegroundColor Yellow

$pycache_dirs = Get-ChildItem -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue
foreach ($dir in $pycache_dirs) {
    Remove-SafelyWithConfirm -Path $dir -Description "Cache Python ($dir)" -IsDirectory
}

# 2. SCRIPTS DE LIMPIEZA REDUNDANTES (basado en estructura actual)
Write-Host "`n[2] Limpiando scripts de limpieza redundantes..." -ForegroundColor Yellow

# Mantener solo el script optimizado actual, eliminar versiones anteriores
$scripts_limpieza_viejos = @(
    "cleanup_demo.ps1",                    # Version antigua
    "cleanup_proyecto_v12_final.ps1",     # Version v1.2
    "cleanup_multiproveedor_final.ps1"    # Version con errores
    # NO eliminamos cleanup_multiproveedor_final_FIXED.ps1 que es el actual
)

foreach ($script in $scripts_limpieza_viejos) {
    Remove-SafelyWithConfirm -Path $script -Description "Script de limpieza obsoleto ($script)"
}

# 3. DOCUMENTACION REDUNDANTE (si no se especifica mantener)
if (-not $KeepDocs) {
    Write-Host "`n[3] Limpiando documentacion redundante..." -ForegroundColor Yellow

    # Eliminar documentos duplicados o versiones anteriores
    $docs_redundantes = @(
        "requirements_multiproveedor.txt",    # Versión separada, usar requirements.txt
        "verify_dependencies.txt"             # Debería ser .ps1, no .txt
    )

    foreach ($doc in $docs_redundantes) {
        Remove-SafelyWithConfirm -Path $doc -Description "Documentacion redundante ($doc)"
    }

    # Mantener solo README principal, eliminar versiones múltiples
    $readme_files = Get-ChildItem "Readme*.md" -ErrorAction SilentlyContinue
    if ($readme_files.Count -gt 1) {
        Write-Host "   INFO: Multiples archivos README encontrados:" -ForegroundColor Cyan
        foreach ($readme in $readme_files) {
            Write-Host "      - $($readme.Name)" -ForegroundColor Gray
        }

        # Eliminar versiones específicas, mantener README.md principal
        $readme_especificos = @(
            "Readme_Multiprovedor_Completo_V1.2.md"  # Version específica, integrar en README.md
        )

        foreach ($readme_esp in $readme_especificos) {
            Remove-SafelyWithConfirm -Path $readme_esp -Description "README especifico ($readme_esp)"
        }
    }
} else {
    Write-Host "`n[3] Manteniendo toda la documentacion..." -ForegroundColor Green
}

# 4. ARCHIVOS TEMPORALES ROBOT FRAMEWORK (basado en estructura actual)
Write-Host "`n[4] Limpiando archivos temporales Robot Framework..." -ForegroundColor Yellow

# Archivos temporales en directorio raíz (según estructura actual)
$robot_temp_files = @(
    "selenium-screenshot-1.png",
    "selenium-screenshot-2.png",
    "selenium-screenshot-3.png",
    "selenium-screenshot-4.png"
)

foreach ($file in $robot_temp_files) {
    Remove-SafelyWithConfirm -Path $file -Description "Screenshot temporal RF ($file)"
}

# 5. BACKUPS Y DUPLICADOS (según estructura actual)
Write-Host "`n[5] Limpiando backups y duplicados..." -ForegroundColor Yellow

$backups_duplicados = @(
    "results\log_backup.html",
    "results\output_backup.xml",
    "results\report_backup.html",
    "tools\gemini_generator_siesa_backup_final_20250709_134820.py"
)

foreach ($backup in $backups_duplicados) {
    Remove-SafelyWithConfirm -Path $backup -Description "Backup/duplicado ($backup)"
}

# 6. RESULTADOS HISTORICOS (si no se especifica mantener)
if (-not $KeepResults) {
    Write-Host "`n[6] Limpiando resultados historicos..." -ForegroundColor Yellow

    # Mantener solo el resultado más reciente según estructura actual
    $result_dirs = @("results\debug_credenciales", "results\debug_keyword", "results\final_fix")

    foreach ($dir in $result_dirs) {
        if (Test-Path $dir) {
            Remove-SafelyWithConfirm -Path $dir -Description "Resultado debug/historico ($dir)" -IsDirectory
        }
    }

    # Para directorios con timestamp, mantener solo el más reciente
    $timestamp_dirs = Get-ChildItem -Path "results" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "^\d{8}_\d{6}$" } | Sort-Object Name -Descending

    if ($timestamp_dirs.Count -gt 1) {
        Write-Host "   INFO Manteniendo resultado mas reciente: $($timestamp_dirs[0].Name)" -ForegroundColor Cyan

        for ($i = 1; $i -lt $timestamp_dirs.Count; $i++) {
            Remove-SafelyWithConfirm -Path $timestamp_dirs[$i].FullName -Description "Resultado historico ($($timestamp_dirs[$i].Name))" -IsDirectory
        }
    }
} else {
    Write-Host "`n[6] Manteniendo todos los resultados de tests..." -ForegroundColor Green
}

# 7. ARCHIVOS TEMPORALES VARIOS
Write-Host "`n[7] Limpiando archivos temporales varios..." -ForegroundColor Yellow

$temp_patterns = @(
    "*.tmp",
    "*.temp",
    "*.pyc",
    "~*"
)

foreach ($pattern in $temp_patterns) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-SafelyWithConfirm -Path $_.FullName -Description "Archivo temporal ($($_.Name))"
    }
}

# 8. REGENERAR ESTRUCTURA ACTUALIZADA
Write-Host "`n[8] Regenerando estructura del proyecto..." -ForegroundColor Yellow

if (-not $DryRun) {
    try {
        # Crear backup de estructura actual
        if (Test-Path "estructura_proyecto_v12.txt") {
            Copy-Item "estructura_proyecto_v12.txt" "estructura_proyecto_v12_backup.txt"
        }

        # Generar nueva estructura
        tree /f /a > estructura_proyecto_v12_clean.txt

        # Reemplazar estructura principal
        if (Test-Path "estructura_proyecto_v12_clean.txt") {
            Remove-Item "estructura_proyecto_v12.txt" -Force -ErrorAction SilentlyContinue
            Rename-Item "estructura_proyecto_v12_clean.txt" "estructura_proyecto_v12.txt"
            Write-Host "   OK Estructura actualizada: estructura_proyecto_v12.txt" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ERROR generando estructura: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   [DRY-RUN] Se regeneraria estructura_proyecto_v12.txt" -ForegroundColor Gray
}

# VERIFICACION POST-LIMPIEZA
Write-Host "`n[9] Verificando sistema post-limpieza..." -ForegroundColor Yellow

if (-not $DryRun) {
    # Verificar que archivos core siguen presentes
    $missing_core = @()
    foreach ($file in $archivos_core) {
        if (-not (Test-Path $file)) {
            $missing_core += $file
        }
    }

    if ($missing_core.Count -eq 0) {
        Write-Host "   OK Todos los archivos core presentes" -ForegroundColor Green

        # Test básico del sistema
        try {
            $test_result = python tools/switch_ai_provider.py --status 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   OK Sistema multi-proveedor funcionando" -ForegroundColor Green
            } else {
                Write-Host "   WARNING Sistema multi-proveedor con problemas" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "   WARNING No se pudo verificar sistema" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ERROR Archivos core faltantes:" -ForegroundColor Red
        foreach ($missing in $missing_core) {
            Write-Host "      - $missing" -ForegroundColor Red
        }
    }
}

# RESUMEN FINAL
Write-Host "`nLIMPIEZA OPTIMIZADA COMPLETADA!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "`nARCHIVOS CORE MANTENIDOS:" -ForegroundColor Cyan
foreach ($file in $archivos_core) {
    if (Test-Path $file) {
        Write-Host "   OK $file" -ForegroundColor Green
    } else {
        Write-Host "   WARNING $file (FALTA)" -ForegroundColor Red
    }
}

Write-Host "`nSISTEMA MULTI-PROVEEDOR OPTIMIZADO" -ForegroundColor Green
Write-Host "   - Cache Python eliminado" -ForegroundColor White
Write-Host "   - Scripts obsoletos eliminados" -ForegroundColor White
Write-Host "   - Documentacion redundante limpia" -ForegroundColor White
Write-Host "   - Archivos core preservados" -ForegroundColor White
Write-Host "   - Estructura actualizada" -ForegroundColor White

Write-Host "`nPROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "   python tools/switch_ai_provider.py --status" -ForegroundColor White
Write-Host "   robot tests/login/siesa_login_tests.robot" -ForegroundColor White
Write-Host "   type estructura_proyecto_v12.txt" -ForegroundColor White

if ($DryRun) {
    Write-Host "`nMODO DRY-RUN: No se elimino nada. Ejecutar sin -DryRun para limpiar." -ForegroundColor Yellow
}

Write-Host "`nESTRUCTURA OPTIMIZADA LISTA!" -ForegroundColor Green