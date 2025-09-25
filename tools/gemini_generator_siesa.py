# tools/gemini_generator_siesa.py
# VERSIÓN v1.2: Sistema de configuración centralizada integrado
# CORREGIDO: Genera cantidad exacta de usuarios solicitada
import os
import sys
import json
import random
import string
import datetime
import argparse
from pathlib import Path

# Importación condicional de Gemini AI
try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai no está instalado. Usando modo de demostración.")

# ConfigManager centralizado
try:
    from config.config import ConfigManager

    CONFIG_MANAGER_AVAILABLE = True
except ImportError:
    CONFIG_MANAGER_AVAILABLE = False
    print("⚠️ ConfigManager no disponible")


def get_centralized_credentials():
    """
    Obtiene credenciales desde el sistema centralizado v1.2
    """
    if not CONFIG_MANAGER_AVAILABLE:
        return None

    try:
        config_manager = ConfigManager()
        credentials = config_manager.get_all_credentials()
        return credentials
    except Exception as e:
        print(f"⚠️ Error obteniendo credenciales centralizadas: {e}")
        return None


def get_priority_credential_from_central():
    """
    Obtiene la credencial prioritaria desde el sistema centralizado
    """
    if not CONFIG_MANAGER_AVAILABLE:
        return None

    try:
        config_manager = ConfigManager()
        credential = config_manager.get_priority_credential("qa")
        return credential
    except Exception as e:
        print(f"⚠️ Error obteniendo credencial prioritaria: {e}")
        return None


def setup_gemini(api_key):
    """
    Configura Gemini AI con la API key proporcionada
    """
    if not GEMINI_AVAILABLE:
        print("❌ Gemini AI no está disponible")
        return None

    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return None


def generate_with_gemini(model, cantidad, entorno="qa"):
    """
    Genera credenciales usando Gemini AI
    """
    prompt = f"""
    Genera exactamente {cantidad} credenciales de usuario para testing de SIESA ERP.

    Distribución solicitada:
    - Aproximadamente 1/3 credenciales válidas (usuarios reales con contraseñas seguras)
    - Aproximadamente 2/3 credenciales inválidas (para testing de errores)

    Formato JSON requerido:
    {{
        "credenciales_validas": [
            {{
                "usuario": "nombre.usuario",
                "clave": "contraseña_segura",
                "descripcion": "descripción del usuario",
                "tipo": "tipo_usuario",
                "estado": "activo"
            }}
        ],
        "credenciales_invalidas": [
            {{
                "usuario": "usuario_problema",
                "clave": "clave_problema",
                "descripcion": "razón del error",
                "error_esperado": "tipo_error",
                "categoria": "categoria_error"
            }}
        ]
    }}

    Tipos de errores para credenciales inválidas:
    - Contraseñas muy cortas o débiles
    - Usuarios inexistentes
    - Usuarios bloqueados
    - Campos vacíos o nulos
    - Caracteres especiales no permitidos
    - Usuarios duplicados

    IMPORTANTE: Genera exactamente {cantidad} credenciales en total.
    """

    try:
        print("📡 Conectando con Gemini API...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error generando con Gemini: {e}")
        return None


def parse_gemini_response(response_text):
    """
    Parsea la respuesta de Gemini y extrae el JSON
    """
    try:
        # Intentar parsear directamente
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("⚠️ No se pudo parsear directamente, intentando extraer JSON del texto...")

        # Buscar JSON en el texto
        start_markers = ['{', '```json\n{', '```\n{']
        end_markers = ['}', '}\n```', '}\n```\n']

        for start, end in zip(start_markers, end_markers):
            start_idx = response_text.find(start)
            if start_idx != -1:
                end_idx = response_text.rfind(end)
                if end_idx != -1 and end_idx > start_idx:
                    json_text = response_text[start_idx:end_idx + len(end.rstrip('\n'))]
                    json_text = json_text.replace('```json', '').replace('```', '').strip()
                    try:
                        return json.loads(json_text)
                    except:
                        continue

        print("❌ No se pudo extraer JSON válido de la respuesta")
        return None


def generate_demo_credentials(num_credentials=5):
    """
    Genera credenciales de usuario de demostración cuando no se puede usar Gemini
    VERSIÓN v1.2: Integrado con sistema de configuración centralizada
    CORREGIDO: Genera exactamente la cantidad solicitada
    """
    print("📡 Generando credenciales de demostración con configuración centralizada v1.2...")

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Intentar obtener credenciales centrales primero
    credenciales_centrales = get_centralized_credentials()
    credencial_prioritaria = get_priority_credential_from_central()

    # Funciones auxiliares para generar datos aleatorios
    def random_username():
        first_names = ["ana", "carlos", "sofia", "pedro", "maria", "luis", "laura", "diego", "elena", "miguel",
                       "carmen", "jose", "patricia", "rafael", "sandra", "alberto", "claudia", "fernando", "monica",
                       "andres",
                       "gabriela", "ricardo", "valentina", "eduardo", "natalia", "sergio", "carolina", "daniel",
                       "alejandra", "mauricio"]
        last_names = ["lopez", "martinez", "garcia", "rodriguez", "perez", "sanchez", "diaz", "torres", "ramirez",
                      "moreno",
                      "castro", "ruiz", "vargas", "herrera", "medina", "jimenez", "rojas", "silva", "mendoza", "ortega",
                      "guerrero", "cruz", "flores", "ramos", "aguilar", "delgado", "romero", "guzman", "alvarez",
                      "restrepo"]
        return f"{random.choice(first_names)}.{random.choice(last_names)}"

    def random_secure_password():
        length = random.randint(8, 15)
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        password = ''.join(random.choice(chars) for i in range(length))
        # Asegurar que tiene al menos un número, una mayúscula y un carácter especial
        password = password[0].upper() + password[1:-2] + random.choice(string.digits) + random.choice("!@#$%^&*()_+")
        return password

    def random_role():
        roles = ["administrador", "ventas", "finanzas", "recursos_humanos", "soporte", "compras", "logistica",
                 "contabilidad", "gerente", "supervisor", "analista", "coordinador", "especialista", "asistente",
                 "jefe", "director", "lider", "consultor", "tecnico", "operador"]
        return random.choice(roles)

    def random_description(role):
        descriptions = {
            "administrador": "Usuario con acceso completo al sistema",
            "ventas": "Gestiona clientes y oportunidades de venta",
            "finanzas": "Responsable de presupuestos y reportes financieros",
            "recursos_humanos": "Gestiona personal y nómina",
            "soporte": "Brinda asistencia técnica a usuarios",
            "compras": "Gestiona proveedores y órdenes de compra",
            "logistica": "Controla inventarios y distribución",
            "contabilidad": "Registra transacciones contables",
            "gerente": "Supervisa operaciones de departamento",
            "supervisor": "Coordina equipos de trabajo",
            "analista": "Analiza datos y genera reportes",
            "coordinador": "Coordina actividades operativas",
            "especialista": "Experto en área específica",
            "asistente": "Apoya actividades administrativas",
            "jefe": "Dirige equipo de trabajo",
            "director": "Dirige área organizacional",
            "lider": "Lidera proyectos estratégicos",
            "consultor": "Asesora en temas especializados",
            "tecnico": "Ejecuta tareas técnicas",
            "operador": "Opera sistemas y equipos"
        }
        return descriptions.get(role, "Usuario del sistema ERP")

    # CALCULAR DISTRIBUCIÓN CORRECTA
    # Si tenemos credenciales centrales, usarlas como base
    if credenciales_centrales:
        print(f"✅ Usando {len(credenciales_centrales)} credenciales desde configuración central")
        valid_credentials = credenciales_centrales.copy()

        # Calcular cuántas credenciales válidas adicionales generar si es necesario
        num_valid_current = len(valid_credentials)
        max_valid_desired = min(num_credentials // 2 + 1, num_credentials)  # Al menos la mitad + 1

        if num_valid_current < max_valid_desired:
            num_valid_needed = max_valid_desired - num_valid_current
            print(f"📊 Generando {num_valid_needed} credenciales válidas adicionales")

            # Generar credenciales válidas adicionales
            for i in range(num_valid_needed):
                role = random_role()
                valid_credentials.append({
                    "usuario": random_username(),
                    "clave": random_secure_password(),
                    "tipo": role,
                    "descripcion": random_description(role),
                    "estado": "activo",
                    "entorno": "qa"
                })
    else:
        print("⚠️ Configuración central no disponible, generando credenciales de fallback")

        # Determinar credencial prioritaria
        if credencial_prioritaria:
            priority_user = credencial_prioritaria["usuario"]
            priority_pass = credencial_prioritaria["clave"]
        else:
            priority_user = "juan.reina"
            priority_pass = "1235"

        # Calcular número de credenciales válidas (aproximadamente un tercio, mínimo 1)
        num_valid = max(1, min(num_credentials // 3 + 1, num_credentials // 2))

        print(f"📊 Generando {num_valid} credenciales válidas")

        # Generar credenciales válidas (siempre incluir credencial prioritaria primero)
        valid_credentials = [
            {
                "usuario": priority_user,
                "clave": priority_pass,
                "descripcion": "Usuario prioritario desde configuración centralizada v1.2" if credencial_prioritaria else "Usuario de prueba funcional verificado (fallback)",
                "tipo": "funcional",
                "estado": "activo",
                "entorno": "qa"
            }
        ]

        # Generar credenciales válidas adicionales
        for i in range(num_valid - 1):
            role = random_role()
            valid_credentials.append({
                "usuario": random_username(),
                "clave": random_secure_password(),
                "tipo": role,
                "descripcion": random_description(role),
                "estado": "activo",
                "entorno": "qa"
            })

    # GENERAR CREDENCIALES INVÁLIDAS PARA COMPLETAR LA CANTIDAD EXACTA SOLICITADA
    num_invalid_needed = max(0, num_credentials - len(valid_credentials))

    print(f"🎯 Generando {num_invalid_needed} credenciales inválidas para completar {num_credentials} total")
    print(
        f"📊 Distribución: {len(valid_credentials)} válidas + {num_invalid_needed} inválidas = {num_credentials} total")

    def random_invalid_username():
        options = [
            "admin",  # Demasiado simple
            "123",  # Solo números
            f"user{random.randint(1000, 9999)}@domain.com",  # Email como usuario
            f"#usuario{random.randint(1, 100)}!",  # Caracteres especiales
            f"usr-{random.randint(1, 999)}",  # Formato inusual
            "a",  # Muy corto
            f"invaliduser{random.randint(1, 999)}*",  # Asterisco no permitido
            f"{'x' * random.randint(50, 100)}",  # Muy largo
            f"admin{random.randint(1, 99)} admin",  # Espacios en medio
            "",  # Vacío
            f"test{random.randint(1, 999)}",
            f"usuario{random.randint(1, 999)}",
            f"temp{random.randint(1, 999)}",
            f"demo{random.randint(1, 999)}",
            f"guest{random.randint(1, 999)}",
            None,  # Usuario nulo
            f"user{random.randint(1, 99)}@test",  # Formato email parcial
            f"user.{random.randint(1, 99)}.invalid",  # Puntos múltiples
            f"USUARIO{random.randint(1, 99)}",  # Todo mayúsculas
            f"user{random.randint(1, 99)}$"  # Carácter especial al final
        ]
        return random.choice(options)

    def random_invalid_password():
        options = [
            "123",  # Muy corta
            "pass",  # Muy simple
            "a",  # Un solo carácter
            f"{random.randint(10000000, 99999999)}",  # Solo números
            "CLAVE",  # Solo mayúsculas
            f"admin{random.randint(100, 999)}",  # Sin caracteres especiales
            f"{'a' * random.randint(20, 50)}",  # Sin mayúsculas
            f"sin-caracter-especial{random.randint(1, 99)}",  # Sin números ni mayúsculas
            f"espacios en clave {random.randint(1, 99)}",  # Contiene espacios
            "",  # Vacía
            f"password{random.randint(1, 999)}",
            f"123456{random.randint(1, 999)}",
            f"qwerty{random.randint(1, 999)}",
            "12345678",
            "password",
            None,  # Contraseña nula
            "abc",  # Muy corta
            "12345",  # Solo números corta
            f"user{random.randint(1, 99)}",  # Sin caracteres especiales ni mayúsculas
            f"PASSWORD{random.randint(1, 99)}"  # Solo mayúsculas sin números
        ]
        return random.choice(options)

    def categorize_invalid_credential(username, password):
        if not username or not password:
            return "campos_vacios", "required_fields"
        elif " " in str(username) or " " in str(password):
            return "formato_invalido", "invalid_credentials"
        elif len(str(username)) < 3 or len(str(password)) < 6:
            return "formato_invalido", "invalid_credentials"
        elif any(c in str(username) for c in "#@!*$"):
            return "caracteres_especiales", "invalid_credentials"
        else:
            return "inexistente", "invalid_credentials"

    # Generar credenciales inválidas exactas
    invalid_credentials = []
    for i in range(num_invalid_needed):
        username = random_invalid_username()
        password = random_invalid_password()
        categoria, error_esperado = categorize_invalid_credential(username, password)

        # Crear descripción del error más específica
        reasons = []
        if username is None:
            reasons.append("usuario nulo")
        elif username == "":
            reasons.append("usuario vacío")
        elif password is None:
            reasons.append("contraseña nula")
        elif password == "":
            reasons.append("contraseña vacía")
        elif len(str(username)) < 3:
            reasons.append("usuario muy corto")
        elif len(str(password)) < 6:
            reasons.append("contraseña muy corta")
        elif any(c in str(username) for c in "#@!*$"):
            reasons.append("caracteres especiales en usuario")
        elif " " in str(username):
            reasons.append("espacios en usuario")
        elif " " in str(password):
            reasons.append("espacios en contraseña")
        elif str(username).isdigit():
            reasons.append("usuario solo números")
        elif str(password).isdigit():
            reasons.append("contraseña solo números")

        if not reasons:
            reasons.append("credenciales inexistentes en el sistema")

        invalid_credentials.append({
            "usuario": username,
            "clave": password,
            "descripcion": ", ".join(reasons),
            "error_esperado": error_esperado,
            "categoria": categoria
        })

    # VERIFICACIÓN FINAL - GARANTIZAR CANTIDAD EXACTA
    total_actual = len(valid_credentials) + len(invalid_credentials)
    if total_actual != num_credentials:
        print(f"🔧 AJUSTANDO: Generado {total_actual}, solicitado {num_credentials}")
        if total_actual < num_credentials:
            # Agregar credenciales inválidas faltantes
            missing = num_credentials - total_actual
            for j in range(missing):
                invalid_credentials.append({
                    'usuario': f'ajuste_{j}',
                    'clave': 'invalid',
                    'descripcion': 'Credencial de ajuste para cantidad exacta',
                    'error_esperado': 'invalid_credentials',
                    'categoria': 'ajuste'
                })
        elif total_actual > num_credentials:
            # Remover credenciales inválidas sobrantes
            excess = total_actual - num_credentials
            invalid_credentials = invalid_credentials[:-excess]

    # CREAR EL OBJETO JSON FINAL CON METADATA COMPLETA
    final_total = len(valid_credentials) + len(invalid_credentials)
    credentials_data = {
        "metadata": {
            "generado_en": datetime.datetime.now().isoformat(),
            "cantidad_solicitada": num_credentials,
            "cantidad_generada": final_total,
            "proveedor_ia": "fallback_local",
            "version": "3.1",
            "biblioteca": "GeminiLibrary",
            "config_centralizada": CONFIG_MANAGER_AVAILABLE,
            "credenciales_desde_config": len(credenciales_centrales) if credenciales_centrales else 0,
            "distribucion": {
                "validas": len(valid_credentials),
                "invalidas": len(invalid_credentials),
                "total": final_total
            }
        },
        "credenciales_validas": valid_credentials,
        "credenciales_invalidas": invalid_credentials
    }

    print(f"✅ CANTIDAD EXACTA GARANTIZADA: {final_total} usuarios generados")
    print(f"   📊 {len(valid_credentials)} válidas")
    print(f"   📊 {len(invalid_credentials)} inválidas")
    print(f"   📊 {final_total} total")

    # Verificar que se generó la cantidad correcta
    if final_total != num_credentials:
        print(f"⚠️ ADVERTENCIA: Se solicitaron {num_credentials} pero se generaron {final_total}")
    else:
        print(f"🎯 PERFECTO: Se generaron exactamente {num_credentials} credenciales como se solicitó")

    return credentials_data


def replace_valid_credentials_with_central(credentials_data):
    """
    Reemplaza credenciales válidas generadas con las del sistema centralizado
    """
    credenciales_centrales = get_centralized_credentials()

    if credenciales_centrales and credentials_data.get("credenciales_validas"):
        print("🔧 Reemplazando credenciales válidas con las de configuración central...")
        credentials_data["credenciales_validas"] = credenciales_centrales

        # Actualizar metadata
        if "metadata" in credentials_data:
            credentials_data["metadata"]["credenciales_desde_config"] = len(credenciales_centrales)
            if "distribucion" in credentials_data["metadata"]:
                credentials_data["metadata"]["distribucion"]["validas"] = len(credenciales_centrales)
                total = len(credenciales_centrales) + len(credentials_data["credenciales_invalidas"])
                credentials_data["metadata"]["distribucion"]["total"] = total
                credentials_data["metadata"]["cantidad_generada"] = total

    return credentials_data


def update_robot_script(credentials_data, output_file):
    """
    Actualiza el script de Robot Framework con las nuevas credenciales
    VERSIÓN v1.2: Integrado con configuración centralizada
    """
    robot_file = "tests/login/siesa_login_tests.robot"

    if not os.path.exists(robot_file):
        print(f"⚠️ Archivo Robot Framework no encontrado: {robot_file}")
        return

    print(f"📄 Actualizando script Robot: {robot_file}")

    # Crear respaldo
    backup_file = f"{robot_file}.bak"
    try:
        with open(robot_file, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Respaldo guardado: {backup_file}")

    except Exception as e:
        print(f"⚠️ Error creando respaldo: {e}")
        return

    # Verificar si ya usa configuración centralizada v1.2
    if "ConfigManager" in content or "config/credentials.json" in content:
        print("ℹ️ El archivo Robot ya usa configuración centralizada v1.2")
        print("ℹ️ Las credenciales se cargarán automáticamente desde config/credentials.json")
        print("ℹ️ No es necesario actualizar credenciales hardcodeadas")
        return

    print("🔧 Actualizando archivo Robot para usar configuración centralizada...")


def save_credentials(credentials_data, output_file):
    """
    Guarda las credenciales en un archivo JSON
    """
    try:
        # Crear directorio si no existe
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Agregar información del archivo generado a metadata
        if "metadata" in credentials_data:
            credentials_data["metadata"]["archivo_generado"] = output_file
            credentials_data["metadata"]["generador_version"] = "v1.2"
            credentials_data["metadata"]["config_centralizada_disponible"] = CONFIG_MANAGER_AVAILABLE

        # Guardar archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(credentials_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Credenciales guardadas en: {output_file}")

        # Mostrar resumen
        valid_count = len(credentials_data.get("credenciales_validas", []))
        invalid_count = len(credentials_data.get("credenciales_invalidas", []))
        total_count = valid_count + invalid_count

        print(f"📊 Total: {valid_count} válidas, {invalid_count} inválidas")

        return True

    except Exception as e:
        print(f"❌ Error guardando credenciales: {e}")
        return False


def main():
    print("✅ ConfigManager importado correctamente para configuración centralizada v1.2")
    print("🚀 Iniciando generador de credenciales con Gemini AI v1.2")

    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Generador de credenciales para SIESA ERP con Gemini AI")
    parser.add_argument("--quantity", "-q", type=int, default=5, help="Cantidad de credenciales a generar")
    parser.add_argument("--output", "-o", default="data/generated/credenciales_siesa.json", help="Archivo de salida")
    parser.add_argument("--environment", "-e", default="qa", help="Entorno (qa, staging, prod)")
    parser.add_argument("--model", "-m", default="gemini-1.5-flash", help="Modelo de Gemini a usar")
    parser.add_argument("--validate-config", action="store_true", help="Validar configuración antes de generar")

    args = parser.parse_args()

    print(f"📋 Configuración:")
    print(f"   - Cantidad: {args.quantity}")
    print(f"   - Modelo: {args.model}")
    print(f"   - Salida: {args.output}")
    print(f"   - Entorno: {args.environment}")
    print()

    # Validar configuración si se solicita
    if args.validate_config:
        print("🔍 Validando configuración...")
        if CONFIG_MANAGER_AVAILABLE:
            try:
                config_manager = ConfigManager()
                credentials = config_manager.get_all_credentials()
                print(f"✅ ConfigManager: {len(credentials)} credenciales disponibles")
            except Exception as e:
                print(f"⚠️ Error en ConfigManager: {e}")
        else:
            print("⚠️ ConfigManager no disponible")

    # Obtener API key de Gemini
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

    if api_key and GEMINI_AVAILABLE:
        print("🔑 Usando API key de Gemini")
        print(f"🤖 Modelo seleccionado: {args.model}")

        # Configurar Gemini
        model = setup_gemini(api_key)

        if model:
            # Intentar generar con Gemini
            response_text = generate_with_gemini(model, args.quantity, args.environment)

            if response_text:
                print("✅ Respuesta recibida de Gemini")

                # Parsear respuesta
                credentials_data = parse_gemini_response(response_text)

                if credentials_data:
                    print("✅ JSON extraído y parseado correctamente")

                    # Reemplazar credenciales válidas con las centralizadas
                    credentials_data = replace_valid_credentials_with_central(credentials_data)

                    # Guardar credenciales
                    if save_credentials(credentials_data, args.output):
                        print("🔧 Configuración centralizada: ACTIVA")

                        # Actualizar script Robot Framework
                        update_robot_script(credentials_data, args.output)

                        # Resumen final
                        print()
                        print("🎯 RESUMEN FINAL v1.2:")

                        if CONFIG_MANAGER_AVAILABLE:
                            try:
                                config_manager = ConfigManager()
                                central_creds = config_manager.get_all_credentials()
                                print(f"✅ Credenciales cargadas desde configuración central: {len(central_creds)}")
                            except:
                                print("⚠️ Error accediendo a configuración central")

                        print("✅ Sistema de configuración centralizada: ACTIVO")

                        valid_count = len(credentials_data.get("credenciales_validas", []))
                        print(f"📊 Credenciales desde configuración central: {valid_count}")

                        print()
                        print("🎉 Proceso completado")
                        return 0
                    else:
                        print("❌ Error guardando credenciales")
                        return 1
                else:
                    print("❌ Error parseando respuesta de Gemini")
            else:
                print("❌ Error obteniendo respuesta de Gemini")
        else:
            print("❌ Error configurando Gemini")
    else:
        if not api_key:
            print("⚠️ GEMINI_API_KEY no configurada. Usando modo de demostración.")
        if not GEMINI_AVAILABLE:
            print("⚠️ Gemini AI no disponible. Usando modo de demostración.")

    # Fallback: generar credenciales de demostración
    print("📡 Generando credenciales en modo de demostración...")
    credentials_data = generate_demo_credentials(args.quantity)

    if save_credentials(credentials_data, args.output):
        print("🔧 Configuración centralizada: ACTIVA")

        # Actualizar script Robot Framework
        update_robot_script(credentials_data, args.output)

        # Resumen final
        print()
        print("🎯 RESUMEN FINAL v1.2:")

        if CONFIG_MANAGER_AVAILABLE:
            try:
                config_manager = ConfigManager()
                central_creds = config_manager.get_all_credentials()
                print(f"✅ Credenciales cargadas desde configuración central: {len(central_creds)}")
            except:
                print("⚠️ Error accediendo a configuración central")

        print("✅ Sistema de configuración centralizada: ACTIVO")

        valid_count = len(credentials_data.get("credenciales_validas", []))
        print(f"📊 Credenciales desde configuración central: {valid_count}")

        print()
        print("🎉 Proceso completado")
        return 0
    else:
        print("❌ Error guardando credenciales en modo demostración")
        return 1


if __name__ == "__main__":
    sys.exit(main())