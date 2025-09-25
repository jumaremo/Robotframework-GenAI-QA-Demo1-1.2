# listeners/robot_ai_listener_gemini.py
import os
import json
import traceback
from datetime import datetime
from pathlib import Path

# ImportaciÃ³n condicional de Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class RobotAIListenerGemini:
    """
    Listener para Robot Framework que analiza errores y proporciona sugerencias
    utilizando la IA de Google Gemini.
    
    Este listener captura errores durante la ejecuciÃ³n de pruebas y utiliza
    Gemini para analizar la causa del error y proporcionar recomendaciones.
    """
    
    ROBOT_LISTENER_API_VERSION = 2
    
    def __init__(self, model="gemini-1.5-flash"):
        """
        Inicializa el listener con la configuraciÃ³n bÃ¡sica.
        
        Args:
            model (str): Modelo de Gemini a utilizar. Por defecto es gemini-pro.
        """
        self.model_name = model
        self.model = None
        self.current_test = None
        self.errors = {}
        self.api_key = None
        
        self._initialize_gemini()
        print(f"\nðŸ¤– Gemini AI Listener inicializado - Analizando errores con {model}")
    
    def _initialize_gemini(self):
        """Inicializa y configura Gemini AI"""
        self.api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not GEMINI_AVAILABLE:
            print("âš ï¸ ADVERTENCIA: Gemini AI no disponible. Instalar: pip install google-generativeai")
            self.active = False
            return
        
        if not self.api_key:
            print("âš ï¸ ADVERTENCIA: No se encontrÃ³ GEMINI_API_KEY. El anÃ¡lisis de errores no estarÃ¡ disponible.")
            print("ðŸ’¡ Configura GEMINI_API_KEY en tu archivo .env o como variable de entorno")
            self.active = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.active = True
            print(f"âœ… Gemini AI configurado correctamente con modelo: {self.model_name}")
        except Exception as e:
            print(f"âŒ Error configurando Gemini: {e}")
            self.active = False
    
    def start_test(self, name, attrs):
        """Captura el inicio de un caso de prueba"""
        self.current_test = name
        print(f"\nâ–¶ï¸ Iniciando caso de prueba: {name}")
    
    def end_test(self, name, attrs):
        """
        Maneja el final de un caso de prueba, generando anÃ¡lisis para casos fallidos.
        """
        if attrs['status'] != 'PASS' and self.active:
            error_message = attrs.get('message', '')
            
            print(f"\nâŒ Caso de prueba fallido: {name}")
            print(f"ðŸ” Generando anÃ¡lisis del error con Gemini AI...")
            
            try:
                analysis = self._analyze_error_with_gemini(name, error_message, attrs)
                
                print("\nðŸ¤– ANÃLISIS DE ERROR GEMINI AI:")
                print("=" * 80)
                print(f"ðŸŽ¯ CAUSA PROBABLE: {analysis['causa_probable']}")
                print(f"\nðŸ“Š NIVEL DE CONFIANZA: {analysis.get('confianza', 'N/A')}")
                print("\nðŸ› ï¸ SOLUCIONES RECOMENDADAS:")
                for idx, solution in enumerate(analysis['soluciones'], 1):
                    print(f"  {idx}. {solution}")
                
                if 'contexto_adicional' in analysis:
                    print(f"\nðŸ’¡ CONTEXTO ADICIONAL: {analysis['contexto_adicional']}")
                
                print("=" * 80)
                
                # Guardar anÃ¡lisis en archivo para referencia
                self._save_analysis_to_file(name, analysis)
                
            except Exception as e:
                print(f"âš ï¸ No se pudo generar anÃ¡lisis con Gemini AI: {e}")
                traceback.print_exc()
                
                # Proporcionar anÃ¡lisis bÃ¡sico de fallback
                fallback_analysis = self._get_fallback_analysis(error_message)
                print("\nðŸ“‹ ANÃLISIS BÃSICO (FALLBACK):")
                print("=" * 80)
                print(f"ðŸ” POSIBLE CAUSA: {fallback_analysis['causa_probable']}")
                print("\nðŸ”§ SUGERENCIAS BÃSICAS:")
                for idx, solution in enumerate(fallback_analysis['soluciones'], 1):
                    print(f"  {idx}. {solution}")
                print("=" * 80)
        
        self.current_test = None
    
    def _analyze_error_with_gemini(self, test_name, error_message, attrs):
        """
        Analiza un error utilizando Gemini AI.
        
        Args:
            test_name: Nombre del caso de prueba
            error_message: Mensaje de error
            attrs: Atributos del caso de prueba
            
        Returns:
            dict: AnÃ¡lisis del error con causa probable y soluciones recomendadas
        """
        if not self.active:
            return self._get_fallback_analysis(error_message)
        
        # Preparar contexto detallado del error
        error_context = {
            "test_name": test_name,
            "error_message": error_message,
            "status": attrs.get('status', 'UNKNOWN'),
            "tags": attrs.get('tags', []),
            "documentation": attrs.get('doc', ''),
            "start_time": attrs.get('starttime', ''),
            "end_time": attrs.get('endtime', ''),
            "framework": "Robot Framework",
            "timestamp": datetime.now().isoformat()
        }
        
        prompt = f"""
        Eres un experto en automatizaciÃ³n de pruebas con Robot Framework y Selenium WebDriver.
        Analiza el siguiente error de una prueba automatizada y proporciona un diagnÃ³stico detallado.
        
        CONTEXTO DEL ERROR:
        {json.dumps(error_context, indent=2, ensure_ascii=False)}
        
        INSTRUCCIONES:
        1. Analiza el error considerando patrones comunes en pruebas de aplicaciones web
        2. Identifica la causa mÃ¡s probable basÃ¡ndote en el mensaje de error
        3. Proporciona soluciones ordenadas por probabilidad de Ã©xito
        4. Incluye un nivel de confianza en tu anÃ¡lisis
        5. Si es relevante, agrega contexto adicional Ãºtil
        
        FORMATO DE RESPUESTA - Responde ÃšNICAMENTE con JSON vÃ¡lido:
        {{
            "causa_probable": "descripciÃ³n detallada de la causa mÃ¡s probable del error",
            "confianza": "Alta/Media/Baja - segÃºn tu nivel de certeza",
            "soluciones": [
                "soluciÃ³n 1 - la mÃ¡s probable de funcionar",
                "soluciÃ³n 2 - alternativa viable", 
                "soluciÃ³n 3 - opciÃ³n adicional",
                "soluciÃ³n 4 - Ãºltimo recurso"
            ],
            "contexto_adicional": "informaciÃ³n adicional Ãºtil para el desarrollador",
            "tipo_error": "categorÃ­a del error (timeout/locator/credential/network/etc)"
        }}
        
        IMPORTANTE: Responde SOLO con el JSON, sin texto adicional ni markdown.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Limpiar respuesta si viene con markdown
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                # Encontrar la primera lÃ­nea que empiece con {
                start_idx = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('{'):
                        start_idx = i
                        break
                # Encontrar la Ãºltima lÃ­nea que termine con }
                end_idx = len(lines) - 1
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].strip().endswith('}'):
                        end_idx = i
                        break
                response_text = '\n'.join(lines[start_idx:end_idx + 1])
            
            try:
                analysis = json.loads(response_text)
                
                # Validar que tenga los campos requeridos
                required_fields = ['causa_probable', 'soluciones']
                for field in required_fields:
                    if field not in analysis:
                        raise ValueError(f"Campo requerido '{field}' no encontrado en la respuesta")
                
                # Asegurar que soluciones es una lista
                if not isinstance(analysis['soluciones'], list):
                    analysis['soluciones'] = [str(analysis['soluciones'])]
                
                return analysis
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parseando respuesta de Gemini: {e}")
                print(f"Respuesta recibida: {response_text[:200]}...")
                return self._get_fallback_analysis(error_message)
                
        except Exception as e:
            print(f"Error comunicÃ¡ndose con Gemini API: {e}")
            return self._get_fallback_analysis(error_message)
    
    def _get_fallback_analysis(self, error_message):
        """AnÃ¡lisis bÃ¡sico cuando Gemini no estÃ¡ disponible"""
        # AnÃ¡lisis bÃ¡sico basado en patrones comunes
        causa_probable = "Error no identificado automÃ¡ticamente"
        soluciones = [
            "Revisar el log completo para mÃ¡s detalles",
            "Verificar que la aplicaciÃ³n estÃ© accesible",
            "Comprobar selectores y tiempos de espera",
            "Ejecutar la prueba manualmente para reproducir el error"
        ]
        
        error_lower = error_message.lower() if error_message else ""
        
        if "element" in error_lower and ("not found" in error_lower or "not visible" in error_lower):
            causa_probable = "Elemento no encontrado o no visible en la pÃ¡gina"
            soluciones = [
                "Verificar que el localizador del elemento sea correcto",
                "Aumentar el tiempo de espera para que el elemento aparezca",
                "Comprobar si el elemento estÃ¡ en un iframe",
                "Verificar que la pÃ¡gina se haya cargado completamente"
            ]
        elif "timeout" in error_lower:
            causa_probable = "Timeout - La operaciÃ³n tardÃ³ mÃ¡s tiempo del esperado"
            soluciones = [
                "Aumentar el valor de timeout en la configuraciÃ³n",
                "Verificar la velocidad de la conexiÃ³n de red",
                "Comprobar si hay procesos que ralenticen el sistema",
                "Revisar si la aplicaciÃ³n responde correctamente"
            ]
        elif "diligencie" in error_lower or "campos requeridos" in error_lower:
            causa_probable = "Campos obligatorios no completados correctamente"
            soluciones = [
                "Verificar que todos los campos requeridos estÃ©n siendo llenados",
                "Comprobar que los datos de entrada sean vÃ¡lidos",
                "Revisar si hay validaciones del lado del cliente",
                "Verificar el formato de los datos introducidos"
            ]
        elif "credential" in error_lower or "login" in error_lower:
            causa_probable = "Problema con las credenciales de acceso"
            soluciones = [
                "Verificar que las credenciales sean correctas",
                "Comprobar si la cuenta estÃ¡ activa",
                "Revisar si hay cambios en las polÃ­ticas de contraseÃ±as",
                "Verificar la configuraciÃ³n del entorno de pruebas"
            ]
        
        return {
            "causa_probable": causa_probable,
            "confianza": "Baja",
            "soluciones": soluciones,
            "contexto_adicional": "AnÃ¡lisis bÃ¡sico sin IA - considera configurar Gemini API para anÃ¡lisis mÃ¡s detallados",
            "tipo_error": "anÃ¡lisis_bÃ¡sico"
        }
    
    def _save_analysis_to_file(self, test_name, analysis):
        """Guarda el anÃ¡lisis en un archivo para referencia posterior"""
        try:
            # Crear directorio de anÃ¡lisis si no existe
            analysis_dir = Path("results/ai_analysis")
            analysis_dir.mkdir(parents=True, exist_ok=True)
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_test_name = "".join(c for c in test_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_test_name}_{timestamp}_analysis.json"
            filepath = analysis_dir / filename
            
            # Agregar metadata al anÃ¡lisis
            analysis_with_metadata = {
                "test_name": test_name,
                "timestamp": datetime.now().isoformat(),
                "listener_version": "gemini-v2.0",
                "analysis": analysis
            }
            
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_with_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"ðŸ’¾ AnÃ¡lisis guardado en: {filepath}")
            
        except Exception as e:
            print(f"âš ï¸ No se pudo guardar el anÃ¡lisis: {e}")
    
    def log_message(self, message):
        """Captura mensajes de log para anÃ¡lisis adicional"""
        # Solo registramos mensajes de error para anÃ¡lisis
        if message.get('level') in ['ERROR', 'FAIL', 'WARN']:
            if self.current_test:
                if self.current_test not in self.errors:
                    self.errors[self.current_test] = []
                self.errors[self.current_test].append({
                    'level': message.get('level'),
                    'message': message.get('message', ''),
                    'timestamp': message.get('timestamp', datetime.now().isoformat())
                })

# FunciÃ³n de ayuda para usar desde lÃ­nea de comandos
def main():
    print("""
    ðŸ¤– Robot Framework Gemini AI Listener
    
    Este script funciona como un listener para Robot Framework y analiza
    los errores utilizando Google Gemini AI.
    
    Para usarlo, agrega esta biblioteca como un listener en tu archivo .robot:
    
    *** Settings ***
    Library    ../listeners/robot_ai_listener_gemini.py
    
    O ejecÃºtalo desde la lÃ­nea de comandos:
    
    robot --listener ../listeners/robot_ai_listener_gemini.py test_file.robot
    
    CONFIGURACIÃ“N REQUERIDA:
    - Instalar: pip install google-generativeai
    - Configurar GEMINI_API_KEY en archivo .env o variable de entorno
    """)

if __name__ == "__main__":
    main()

