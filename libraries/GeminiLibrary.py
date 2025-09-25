"""
GeminiLibrary v4 - Librería híbrida mejorada para generación de datos de prueba con IA
Combina lo mejor de Gemini AI con mejoras adoptadas de Claude
VERSIÓN v1.2: Sistema de configuración centralizada integrado
Para uso con Robot Framework y Gemini AI
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

# 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Importar ConfigManager
try:
    from config.config import ConfigManager
    CONFIG_MANAGER_AVAILABLE = True
except ImportError:
    CONFIG_MANAGER_AVAILABLE = False
    print("⚠️ ConfigManager no disponible. Usando método tradicional para credenciales.")

# Importación condicional de Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class GeminiLibrary:
    """Librería Robot Framework híbrida para generar datos de prueba usando Gemini AI"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '4.0'  # ← Incrementado para v1.2

    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        """
        Inicializa la librería con configuración de Gemini

        Args:
            api_key: API Key de Gemini. Si no se proporciona, busca en GEMINI_API_KEY
            model: Modelo de Gemini a utilizar (adoptado de Claude - configurabilidad)
        """
        self.model_name = model
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.model = None
        
        # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Inicializar ConfigManager
        self.config_manager = None
        if CONFIG_MANAGER_AVAILABLE:
            try:
                self.config_manager = ConfigManager()
                print("✅ ConfigManager inicializado - Credenciales centralizadas disponibles")
            except Exception as e:
                print(f"⚠️ Error inicializando ConfigManager: {e}")
                self.config_manager = None

        # Validación estricta de API key (adoptado de Claude)
        self._validate_api_key()

        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✅ GeminiLibrary v1.2 inicializada correctamente con {self.model_name}")
            except Exception as e:
                print(f"⚠️ Error inicializando Gemini: {e}")
                self.model = None
        else:
            if not GEMINI_AVAILABLE:
                print("⚠️ Gemini AI no disponible. Instalar: pip install google-generativeai")
            if not self.api_key:
                print("⚠️ GEMINI_API_KEY no configurada. Usando datos de fallback")

    def _validate_api_key(self):
        """Valida la API key de Gemini con formato específico (adoptado de Claude)"""
        if not self.api_key:
            print("⚠️ ADVERTENCIA: No se encontró GEMINI_API_KEY. El análisis de errores no estará disponible.")
            print("💡 Configura GEMINI_API_KEY en tu archivo .env o como variable de entorno")
            return

        # Validación específica para Gemini API keys
        if not (self.api_key.startswith('AIza') and len(self.api_key) >= 20):
            print("⚠️ ADVERTENCIA: La API key de Gemini parece tener un formato incorrecto.")
            print("💡 Las API keys de Gemini deben comenzar con 'AIza' y tener al menos 20 caracteres")

    def _extract_json_from_text(self, text):
        """
        Extrae JSON de un texto robusto (híbrido: limpieza markdown + regex de Claude)
        """
        # Primero intentar limpiar markdown (método Gemini)
        if text.startswith('```'):
            lines = text.split('\n')
            # Encontrar la primera línea que empiece con {
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    start_idx = i
                    break
            # Encontrar la última línea que termine con }
            end_idx = len(lines) - 1
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().endswith('}'):
                    end_idx = i
                    break
            text = '\n'.join(lines[start_idx:end_idx + 1])

        # Luego usar regex como fallback (método Claude)
        json_pattern = r'(\{[\s\S]*\})'
        match = re.search(json_pattern, text)

        if match:
            json_text = match.group(1)
            return json_text

        return text  # Devolver el texto original si no se encuentra JSON

    def generar_credenciales_siesa(self, cantidad=5, incluir_validas=True):
        """
        Genera credenciales específicamente para SIESA ERP (método único de Gemini)
        VERSIÓN v1.2: Integrado con sistema de configuración centralizada

        Args:
            cantidad: Número de credenciales inválidas a generar
            incluir_validas: Si incluir credenciales válidas conocidas

        Returns:
            dict: Estructura con credenciales válidas e inválidas
        """
        resultado = {
            "metadata": {
                "generado_en": datetime.now().isoformat(),
                "cantidad_solicitada": cantidad,
                "proveedor_ia": self.model_name if self.model else "fallback",
                "version": "4.0",  # ← Actualizado para v1.2
                "biblioteca": "GeminiLibrary",
                "config_centralizada": bool(self.config_manager)  # ← NUEVO: Indicador de config centralizada
            },
            "credenciales_validas": [],
            "credenciales_invalidas": []
        }

        # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Cargar credenciales desde ConfigManager
        if incluir_validas:
            if self.config_manager:
                try:
                    # Obtener todas las credenciales válidas desde configuración central
                    credenciales_centrales = self.config_manager.get_all_valid_credentials()
                    
                    # Convertir al formato esperado
                    for cred in credenciales_centrales:
                        resultado["credenciales_validas"].append({
                            "usuario": cred["usuario"],
                            "clave": cred["clave"], 
                            "descripcion": cred.get("descripcion", "Usuario desde configuración centralizada"),
                            "tipo": cred.get("tipo", "funcional"),
                            "estado": "activo",
                            "prioridad": cred.get("prioridad", 999),
                            "entorno": cred.get("entorno", "qa")
                        })
                    
                    print(f"✅ Credenciales válidas cargadas desde configuración central: {len(credenciales_centrales)}")
                    
                except Exception as e:
                    print(f"⚠️ Error cargando credenciales centrales: {e}")
                    # Fallback a credenciales hardcodeadas
                    resultado["credenciales_validas"] = self._get_fallback_valid_credentials()
            else:
                # Usar credenciales hardcodeadas como fallback
                resultado["credenciales_validas"] = self._get_fallback_valid_credentials()

        # Generar credenciales inválidas usando IA o fallback
        if self.model and cantidad > 0:
            try:
                credenciales_ia = self._generar_con_ia(cantidad)
                resultado["credenciales_invalidas"] = credenciales_ia
            except Exception as e:
                print(f"Error generando con IA: {e}. Usando fallback.")
                resultado["credenciales_invalidas"] = self._get_fallback_credentials(cantidad)
        else:
            resultado["credenciales_invalidas"] = self._get_fallback_credentials(cantidad)

        return resultado

    def _get_fallback_valid_credentials(self):
        """
        Credenciales válidas de fallback cuando ConfigManager no está disponible
        VERSIÓN v1.2: Método de compatibilidad
        """
        print("⚠️ Usando credenciales válidas de fallback (no centralizadas)")
        return [
            {
                "usuario": "juan.reina",
                "clave": "1235",  # ← CORREGIDO: Cambiado de 1234 a 1235
                "descripcion": "Usuario de prueba funcional verificado (fallback)",
                "tipo": "funcional",
                "estado": "activo",
                "prioridad": 1,
                "entorno": "qa"
            }
        ]

    def _generar_con_ia(self, cantidad):
        """Genera credenciales usando Gemini AI con extracción JSON híbrida"""
        prompt = f"""
        Genera {cantidad} credenciales inválidas para testing de un sistema ERP empresarial SIESA.
        Incluye diferentes tipos de errores realistas:
        1. Campos vacíos (usuario="", clave="")
        2. Usuarios con caracteres especiales problemáticos
        3. Contraseñas demasiado simples o complejas
        4. Combinaciones que no existen en el sistema
        5. Formatos incorrectos típicos en formularios web
        
        IMPORTANTE: Responde SOLO con JSON válido en este formato exacto:
        [
            {{
                "usuario": "valor_usuario",
                "clave": "valor_clave", 
                "descripcion": "descripción del tipo de error",
                "error_esperado": "required_fields o invalid_credentials",
                "categoria": "campos_vacios/caracteres_especiales/formato_invalido/inexistente"
            }}
        ]
        
        NO agregues texto adicional, solo el JSON.
        """

        response = self.model.generate_content(prompt)
        credenciales_text = response.text.strip()

        # Usar extracción JSON híbrida (Gemini + Claude)
        json_text = self._extract_json_from_text(credenciales_text)

        try:
            credenciales_invalidas = json.loads(json_text)
            return credenciales_invalidas
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON de IA: {e}")
            return self._get_fallback_credentials(cantidad)

    def _get_fallback_credentials(self, cantidad):
        """Credenciales de fallback robustas cuando la IA no está disponible"""
        fallback_credentials = [
            {
                "usuario": "",
                "clave": "",
                "descripcion": "Campos completamente vacíos",
                "error_esperado": "required_fields",
                "categoria": "campos_vacios"
            },
            {
                "usuario": "usuario_inexistente_2025",
                "clave": "password_incorrecto_123",
                "descripcion": "Usuario y contraseña inexistentes en el sistema",
                "error_esperado": "invalid_credentials",
                "categoria": "inexistente"
            },
            {
                "usuario": "admin",
                "clave": "contraseña_incorrecta_456",
                "descripcion": "Usuario común con contraseña incorrecta",
                "error_esperado": "invalid_credentials",
                "categoria": "inexistente"
            },
            {
                "usuario": "test@#$%&*()",
                "clave": "test123",
                "descripcion": "Usuario con caracteres especiales problemáticos",
                "error_esperado": "invalid_credentials",
                "categoria": "caracteres_especiales"
            },
            {
                "usuario": "usuario_normal",
                "clave": "",
                "descripcion": "Usuario válido pero contraseña vacía",
                "error_esperado": "required_fields",
                "categoria": "campos_vacios"
            },
            {
                "usuario": "",
                "clave": "password123",
                "descripcion": "Contraseña válida pero usuario vacío",
                "error_esperado": "required_fields",
                "categoria": "campos_vacios"
            },
            {
                "usuario": "a",
                "clave": "b",
                "descripcion": "Credenciales demasiado cortas",
                "error_esperado": "invalid_credentials",
                "categoria": "formato_invalido"
            },
            {
                "usuario": "usuario_con_espacios ",
                "clave": " password_con_espacios",
                "descripcion": "Credenciales con espacios al inicio/final",
                "error_esperado": "invalid_credentials",
                "categoria": "formato_invalido"
            }
        ]

        return fallback_credentials[:cantidad]

    def guardar_credenciales_json(self, credenciales, archivo_destino):
        """
        Guarda las credenciales en archivo JSON con formato legible

        Args:
            credenciales: Dict con credenciales generadas
            archivo_destino: Ruta del archivo donde guardar

        Returns:
            str: Mensaje de confirmación
        """
        # Crear directorio padre si no existe
        Path(archivo_destino).parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(archivo_destino, 'w', encoding='utf-8') as f:
                json.dump(credenciales, f, ensure_ascii=False, indent=2)

            total_validas = len(credenciales.get('credenciales_validas', []))
            total_invalidas = len(credenciales.get('credenciales_invalidas', []))

            return f"✅ Credenciales guardadas en: {archivo_destino} ({total_validas} válidas, {total_invalidas} inválidas)"

        except Exception as e:
            return f"❌ Error guardando credenciales: {e}"

    # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Nuevos métodos para acceso a credenciales
    def obtener_credenciales_centralizadas(self, entorno="qa"):
        """
        Obtiene credenciales desde el sistema centralizado

        Args:
            entorno: Entorno para el cual obtener credenciales (qa, dev, prod)

        Returns:
            list: Lista de credenciales para el entorno especificado
        """
        if not self.config_manager:
            print("⚠️ ConfigManager no disponible. Usando credenciales de fallback.")
            return self._get_fallback_valid_credentials()

        try:
            credenciales = self.config_manager.get_credentials_by_environment(entorno)
            print(f"✅ Credenciales cargadas para entorno '{entorno}': {len(credenciales)}")
            return credenciales
        except Exception as e:
            print(f"⚠️ Error obteniendo credenciales para entorno '{entorno}': {e}")
            return self._get_fallback_valid_credentials()

    def obtener_credencial_prioritaria(self, entorno="qa"):
        """
        Obtiene la credencial de mayor prioridad para un entorno

        Args:
            entorno: Entorno para buscar credencial prioritaria

        Returns:
            dict: Credencial de mayor prioridad o None
        """
        if not self.config_manager:
            fallback = self._get_fallback_valid_credentials()
            print(f"✅ Credencial prioritaria obtenida para entorno '{entorno}': {fallback[0]['usuario'] if fallback else 'ninguna'}")
            return fallback[0] if fallback else None
        
        try:
            credencial = self.config_manager.get_priority_credential(entorno)
            print(f"✅ Credencial prioritaria obtenida para entorno '{entorno}': {credencial['usuario'] if credencial else 'ninguna'}")
            return credencial
        except Exception as e:
            print(f"⚠️ Error obteniendo credencial prioritaria: {e}")
            fallback = self._get_fallback_valid_credentials()
            return fallback[0] if fallback else None

    def validar_configuracion_centralizada(self):
        """
        Valida que el sistema de configuración centralizada esté funcionando
        
        Returns:
            dict: Estado de la configuración centralizada
        """
        resultado = {
            "config_manager_disponible": bool(self.config_manager),
            "archivo_credenciales_existe": False,
            "total_credenciales": 0,
            "entornos_configurados": [],
            "errores": []
        }
        
        if self.config_manager:
            try:
                # Verificar archivo de credenciales
                if hasattr(self.config_manager, 'credentials_file') and os.path.exists(self.config_manager.credentials_file):
                    resultado["archivo_credenciales_existe"] = True
                
                # Obtener estadísticas
                todas_credenciales = self.config_manager.get_all_valid_credentials()
                resultado["total_credenciales"] = len(todas_credenciales)
                
                # Obtener entornos configurados
                entornos = set()
                for cred in todas_credenciales:
                    entornos.add(cred.get("entorno", "qa"))
                resultado["entornos_configurados"] = list(entornos)
                
            except Exception as e:
                resultado["errores"].append(f"Error validando configuración: {e}")
        else:
            resultado["errores"].append("ConfigManager no inicializado")
        
        return resultado

    def generar_datos_de_prueba(self, descripcion, cantidad=1, formato="dict"):
        """
        Método genérico para generar datos de prueba (compatibilidad híbrida)

        Args:
            descripcion: Descripción de los datos a generar
            cantidad: Cantidad de elementos a generar
            formato: Formato de salida (dict por defecto)

        Returns:
            dict: Datos generados con metadata
        """
        if not self.model:
            return {
                "error": "Gemini AI no disponible",
                "variaciones": [f"Datos de ejemplo para: {descripcion}"],
                "metadata": {
                    "generado_en": datetime.now().isoformat(),
                    "descripcion": descripcion,
                    "cantidad": cantidad,
                    "proveedor": "fallback"
                }
            }

        try:
            prompt = f"""
            Genera {cantidad} ejemplos diferentes de: {descripcion}. 
            
            IMPORTANTE: Tu respuesta debe ser EXCLUSIVAMENTE un objeto JSON válido sin texto adicional.
            No incluyas ninguna explicación, introducción ni conclusión. Solo devuelve el JSON puro.

            Formato JSON requerido:
            {{
                "variaciones": [
                    "Variación 1",
                    "Variación 2",
                    "Variación 3"
                ]
            }}
            """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Usar extracción JSON híbrida
            json_text = self._extract_json_from_text(response_text)

            try:
                datos = json.loads(json_text)

                # Agregar metadata
                resultado = {
                    "variaciones": datos.get("variaciones", [response_text]),
                    "metadata": {
                        "generado_en": datetime.now().isoformat(),
                        "descripcion": descripcion,
                        "cantidad": cantidad,
                        "proveedor": self.model_name
                    }
                }

                # Devolver según el formato solicitado (adoptado de Claude)
                if formato.lower() == 'json':
                    return json.dumps(resultado, indent=2, ensure_ascii=False)
                elif formato.lower() == 'dict':
                    return resultado
                elif formato.lower() == 'list':
                    return resultado.get('variaciones', [])

            except json.JSONDecodeError:
                return {
                    "variaciones": [response_text],
                    "metadata": {
                        "generado_en": datetime.now().isoformat(),
                        "descripcion": descripcion,
                        "cantidad": cantidad,
                        "proveedor": self.model_name,
                        "nota": "JSON no válido, respuesta directa"
                    }
                }

        except Exception as e:
            return {
                "error": str(e),
                "variaciones": [f"Error generando: {descripcion}"],
                "metadata": {
                    "generado_en": datetime.now().isoformat(),
                    "descripcion": descripcion,
                    "error": str(e)
                }
            }

    def verificar_contenido_apropiado(self, contenido, criterios=None):
        """
        Verifica si el contenido cumple con criterios básicos (mejorado híbrido)

        Args:
            contenido: Texto a verificar
            criterios: Lista de criterios que debe cumplir

        Returns:
            bool: True si cumple todos los criterios
        """
        if not contenido or not isinstance(contenido, str):
            return False

        # Si hay IA disponible, usar análisis inteligente
        if self.model and criterios:
            try:
                criterios_texto = "\n".join([f"- {criterio}" for criterio in criterios])
                prompt = f"""
                Analiza si el siguiente texto cumple con TODOS estos criterios:
                {criterios_texto}

                El texto a analizar es:
                "{contenido}"

                Responde SOLAMENTE con un objeto JSON con la siguiente estructura:
                {{
                    "cumple": true o false,
                    "razones": ["razón 1", "razón 2", ...] (lista de razones por las que cumple o no cumple)
                }}
                """

                response = self.model.generate_content(prompt)
                response_text = response.text.strip()

                json_text = self._extract_json_from_text(response_text)
                datos = json.loads(json_text)

                return datos.get("cumple", False)

            except Exception as e:
                print(f"Error en validación con IA: {e}, usando validación básica")

        # Validación básica como fallback
        if criterios:
            contenido_lower = contenido.lower()
            for criterio in criterios:
                if isinstance(criterio, str) and criterio.lower() not in contenido_lower:
                    return False

        return True

    def validar_similitud_semantica(self, texto1, texto2, umbral=0.5):
        """
        Validación de similitud semántica híbrida (IA + básica)

        Args:
            texto1: Primer texto a comparar
            texto2: Segundo texto a comparar
            umbral: Umbral de similitud (0.0 a 1.0)

        Returns:
            bool: True si la similitud supera el umbral
        """
        if not texto1 or not texto2:
            return False

        # Si hay IA disponible, usar análisis semántico inteligente
        if self.model:
            try:
                prompt = f"""
                Compara estos dos textos y determina su similitud semántica en una escala de 0.0 a 1.0,
                donde 0.0 significa completamente diferentes y 1.0 significa idénticos en significado:

                Texto 1: "{texto1}"
                Texto 2: "{texto2}"

                Responde SOLAMENTE con un objeto JSON con la siguiente estructura:
                {{
                    "similitud": valor numérico entre 0.0 y 1.0,
                    "explicacion": "breve explicación de por qué asignaste ese valor"
                }}
                """

                response = self.model.generate_content(prompt)
                response_text = response.text.strip()

                json_text = self._extract_json_from_text(response_text)
                datos = json.loads(json_text)

                similitud = datos.get("similitud", 0.0)
                return similitud >= umbral

            except Exception as e:
                print(f"Error en similitud con IA: {e}, usando validación básica")

        # Implementación básica usando intersección de palabras como fallback
        palabras1 = set(texto1.lower().split())
        palabras2 = set(texto2.lower().split())

        if not palabras1 or not palabras2:
            return False

        interseccion = len(palabras1.intersection(palabras2))
        union = len(palabras1.union(palabras2))

        similitud = interseccion / union if union > 0 else 0
        return similitud >= umbral

    def obtener_estado_biblioteca(self):
        """
        Retorna información sobre el estado de la librería híbrida
        VERSIÓN v1.2: Incluye información de configuración centralizada

        Returns:
            dict: Estado actual de la configuración
        """
        estado_config = self.validar_configuracion_centralizada()
        
        return {
            "gemini_disponible": GEMINI_AVAILABLE,
            "api_key_configurada": bool(self.api_key),
            "modelo_inicializado": bool(self.model),
            "modelo_nombre": self.model_name,
            "version": self.ROBOT_LIBRARY_VERSION,
            "modo": "IA" if self.model else "Fallback",
            "tipo": "Biblioteca Híbrida Gemini-Claude v1.2",
            
            # 🔧 CONFIGURACIÓN CENTRALIZADA v1.2 - Información adicional
            "config_centralizada": {
                "disponible": estado_config["config_manager_disponible"],
                "archivo_existe": estado_config["archivo_credenciales_existe"],
                "total_credenciales": estado_config["total_credenciales"],
                "entornos": estado_config["entornos_configurados"],
                "errores": estado_config["errores"]
            }
        }