# tools/robot_md_reporter_gemini.py
# VERSIÓN v1.2: Sistema de configuración centralizada integrado
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import json

# Configuración UTF-8 robusta
import locale
import codecs

# Forzar codificación UTF-8
if sys.platform.startswith('win'):
    # Para Windows
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configurar locale
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

# Importación condicional de Gemini AI para análisis avanzado
try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def create_directory_if_not_exists(directory):
    """Crea el directorio si no existe"""
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"✅ Directorio verificado: {directory}")


def parse_robot_output(xml_path):
    """Parsea el archivo XML de salida de Robot Framework"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"❌ Error al leer el archivo XML: {e}")
        return None


def format_time(timestamp):
    """Formatea el timestamp de Robot Framework"""
    try:
        # Robot Framework usa el formato 'YYYYMMDD HH:MM:SS.mmm'
        if ' ' in timestamp:
            date_str = timestamp.split(' ')[0]
            time_str = timestamp.split(' ')[1]
        else:
            date_str = timestamp[:8] if len(timestamp) >= 8 else timestamp
            time_str = timestamp[9:] if len(timestamp) > 9 else ''

        if len(date_str) >= 8:
            year = date_str[0:4]
            month = date_str[4:6]
            day = date_str[6:8]
            formatted_date = f"{year}-{month}-{day}"
            return f"{formatted_date} {time_str}" if time_str else formatted_date
        else:
            return timestamp
    except:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def extract_test_execution_time(status_element):
    """Extrae y formatea el tiempo de ejecución de un test"""
    if status_element is None:
        return "N/A"

    start_time = status_element.get('starttime', '')
    end_time = status_element.get('endtime', '')

    if not start_time or not end_time:
        return "N/A"

    try:
        # Convertir a objetos datetime para cálculo
        start_dt = datetime.strptime(start_time, '%Y%m%d %H:%M:%S.%f')
        end_dt = datetime.strptime(end_time, '%Y%m%d %H:%M:%S.%f')

        # Calcular duración
        duration = end_dt - start_dt

        # Formatear duración en segundos
        seconds = duration.total_seconds()
        if seconds < 60:
            return f"{seconds:.2f} segundos"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes} minutos, {remaining_seconds:.2f} segundos"
    except Exception as e:
        return "Error calculando tiempo"


def collect_test_details(test_element):
    """Recoge todos los detalles importantes de un test"""
    status = test_element.find('status')
    test_status = status.get('status', 'UNKNOWN') if status is not None else 'UNKNOWN'
    test_message = status.text if status is not None and status.text else ''

    # Extraer tags
    tags = []
    tags_element = test_element.find('tags')
    if tags_element is not None:
        for tag in tags_element.findall('tag'):
            tags.append(tag.text)

    # Extraer keywords ejecutados
    keywords = []
    for kw in test_element.findall('.//kw'):
        kw_name = kw.get('name', '')
        if kw_name and kw_name not in keywords:
            keywords.append(kw_name)

    execution_time = extract_test_execution_time(status)

    return {
        'name': test_element.get('name', 'Sin nombre'),
        'status': test_status,
        'message': test_message,
        'documentation': test_element.get('doc', ''),
        'tags': tags,
        'keywords': keywords[:5],  # Limitar a los primeros 5 para no sobrecargar el informe
        'execution_time': execution_time
    }


def analyze_error_with_gemini(test_name, error_message, model="gemini-1.5-flash"):
    """
    Analiza un error usando Gemini AI para generar recomendaciones más precisas
    """
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

    if not GEMINI_AVAILABLE or not api_key:
        return get_basic_recommendations(error_message)

    try:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)

        prompt = f"""
        Analiza el siguiente error de una prueba automatizada con Robot Framework y Selenium:

        Test: {test_name}
        Error: {error_message}

        Proporciona recomendaciones específicas y prácticas para solucionarlo.
        Responde en formato JSON:
        {{
            "causa_probable": "causa más probable del error",
            "recomendaciones": [
                "recomendación 1 específica y accionable",
                "recomendación 2 específica y accionable",
                "recomendación 3 específica y accionable"
            ],
            "categoria": "tipo de error (timeout/locator/credential/network/etc)"
        }}
        """

        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()

        # Limpiar respuesta si viene con markdown
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('{')), 0)
            end_idx = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip().endswith('}')), len(lines) - 1)
            response_text = '\n'.join(lines[start_idx:end_idx + 1])

        try:
            analysis = json.loads(response_text)
            return analysis
        except json.JSONDecodeError:
            return get_basic_recommendations(error_message)

    except Exception as e:
        print(f"⚠️ Error analizando con Gemini: {e}")
        return get_basic_recommendations(error_message)


def get_basic_recommendations(error_message):
    """Recomendaciones básicas basadas en patrones comunes"""
    error_lower = error_message.lower() if error_message else ""

    if "element" in error_lower and ("not found" in error_lower or "not visible" in error_lower):
        return {
            "causa_probable": "Elemento no encontrado o no visible en la página",
            "recomendaciones": [
                "Verificar que el localizador del elemento sea correcto",
                "Aumentar el tiempo de espera para que el elemento aparezca",
                "Comprobar si el elemento está en un iframe",
                "Verificar que la página se haya cargado completamente"
            ],
            "categoria": "locator"
        }
    elif "timeout" in error_lower:
        return {
            "causa_probable": "Timeout - La operación tardó más tiempo del esperado",
            "recomendaciones": [
                "Aumentar el valor de timeout en la configuración",
                "Verificar la velocidad de la conexión de red",
                "Comprobar si hay procesos que ralenticen el sistema",
                "Revisar si la aplicación responde correctamente"
            ],
            "categoria": "timeout"
        }
    elif "diligencie" in error_lower or "campos requeridos" in error_lower:
        return {
            "causa_probable": "Campos obligatorios no completados correctamente",
            "recomendaciones": [
                "Verificar que todos los campos requeridos estén siendo llenados",
                "Comprobar que los datos de entrada sean válidos",
                "Revisar si hay validaciones del lado del cliente",
                "Verificar el formato de los datos introducidos"
            ],
            "categoria": "validation"
        }
    else:
        return {
            "causa_probable": "Error no categorizado automáticamente",
            "recomendaciones": [
                "Revisar el log completo para más detalles",
                "Ejecutar el test con mayor nivel de detalle (--loglevel DEBUG)",
                "Verificar si ha habido cambios recientes en la aplicación",
                "Comprobar la configuración del entorno de pruebas"
            ],
            "categoria": "general"
        }


def create_markdown_report(xml_root, output_path):
    """Crea un informe en formato Markdown mejorado a partir del XML de salida"""
    if xml_root is None:
        return

    # Obtener información básica
    suite = xml_root.find('suite')
    suite_name = suite.get('name', 'Sin nombre') if suite else 'Sin nombre'

    # Calcular estadísticas
    all_tests = xml_root.findall('.//test')
    passed_tests = xml_root.findall('.//test/status[@status="PASS"]')
    failed_tests = xml_root.findall('.//test/status[@status="FAIL"]')

    total = len(all_tests)
    pass_count = len(passed_tests)
    fail_count = len(failed_tests)

    pass_percentage = (pass_count / total) * 100 if total > 0 else 0

    # Extraer tiempo total de ejecución
    status_element = xml_root.find('suite/status')
    total_execution_time = extract_test_execution_time(status_element)

    # Fecha actual formateada
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Crear el contenido del informe
    report_content = []

    # Encabezado con estilo mejorado
    report_content.append(f"# 📊 Informe Ejecutivo de Pruebas Automatizadas")
    report_content.append(f"## {suite_name}")
    report_content.append(f"\n**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append(f"**Motor de IA:** {'Gemini AI' if GEMINI_AVAILABLE else 'Análisis básico'}")

    # Resumen visual con emojis
    report_content.append("\n## 📈 Resumen de Resultados")

    report_content.append("\n| Métrica | Resultado |")
    report_content.append("| ------- | --------- |")
    report_content.append(f"| Total de pruebas | **{total}** |")
    report_content.append(f"| ✅ Pruebas exitosas | **{pass_count}** ({pass_percentage:.1f}%) |")
    report_content.append(f"| ❌ Pruebas fallidas | **{fail_count}** |")
    report_content.append(f"| ⏱️ Tiempo total de ejecución | **{total_execution_time}** |")
    report_content.append(f"| 📅 Fecha de ejecución | **{current_date}** |")

    # Gráfico visual ASCII/Unicode de barras para resultados
    if total > 0:
        bar_graph_pass = "🟩" * max(1, int(pass_percentage / 10))
        bar_graph_fail = "🟥" * max(0, int((100 - pass_percentage) / 10))
        report_content.append(
            f"\n**Distribución de resultados:** {bar_graph_pass}{bar_graph_fail} {pass_percentage:.1f}%")

    # Detalle de los casos de prueba con información expandida
    report_content.append("\n## 🧪 Detalle de Casos de Prueba")

    # Primero listar tests fallidos para darles mayor visibilidad
    if fail_count > 0:
        report_content.append("\n### ❌ Tests Fallidos")

        for test in all_tests:
            status = test.find('status')
            if status is not None and status.get('status') == 'FAIL':
                test_details = collect_test_details(test)

                report_content.append(f"\n#### 🔴 {test_details['name']}")

                if test_details['documentation']:
                    report_content.append(f"\n**Descripción:** {test_details['documentation']}")

                # Tags como badges
                if test_details['tags']:
                    tags_str = ' '.join([f"`{tag}`" for tag in test_details['tags']])
                    report_content.append(f"\n**Tags:** {tags_str}")

                report_content.append(f"\n**Tiempo de ejecución:** {test_details['execution_time']}")

                # Mensaje de error con formato para destacarlo
                if test_details['message']:
                    report_content.append(f"\n**Error:** ```\n{test_details['message']}\n```")

                # Acciones ejecutadas (opcional, para dar contexto)
                if test_details['keywords']:
                    keywords_list = ", ".join(test_details['keywords'])
                    report_content.append(f"\n**Acciones principales:** {keywords_list}...")

    # Luego listar tests exitosos
    if pass_count > 0:
        report_content.append("\n### ✅ Tests Exitosos")

        for test in all_tests:
            status = test.find('status')
            if status is not None and status.get('status') == 'PASS':
                test_details = collect_test_details(test)

                report_content.append(f"\n#### 🟢 {test_details['name']}")

                if test_details['documentation']:
                    report_content.append(f"\n**Descripción:** {test_details['documentation']}")

                # Tags como badges
                if test_details['tags']:
                    tags_str = ' '.join([f"`{tag}`" for tag in test_details['tags']])
                    report_content.append(f"\n**Tags:** {tags_str}")

                report_content.append(f"\n**Tiempo de ejecución:** {test_details['execution_time']}")

    # Añadir sección con sugerencias para tests fallidos usando IA
    if fail_count > 0:
        report_content.append("\n## 🤖 Recomendaciones de IA para Tests Fallidos")
        report_content.append(
            "\nA continuación se presentan sugerencias generadas con IA para solucionar los problemas encontrados:")

        for test in all_tests:
            status = test.find('status')
            if status is not None and status.get('status') == 'FAIL':
                test_name = test.get('name', 'Sin nombre')
                test_message = status.text if status.text else 'Error no especificado'

                # Generar recomendaciones usando Gemini AI
                analysis = analyze_error_with_gemini(test_name, test_message)

                # Añadir análisis al informe
                report_content.append(f"\n### 🔍 Test: {test_name}")
                report_content.append(f"\n**🎯 Causa probable:** {analysis['causa_probable']}")
                report_content.append(f"\n**📋 Categoría:** `{analysis.get('categoria', 'general')}`")

                if len(test_message) > 100:
                    report_content.append(f"\n**❌ Error detectado:** `{test_message[:100]}...`")
                else:
                    report_content.append(f"\n**❌ Error detectado:** `{test_message}`")

                report_content.append("\n**🛠️ Recomendaciones:**")

                for i, recommendation in enumerate(analysis['recomendaciones'], 1):
                    report_content.append(f"{i}. {recommendation}")

    # Añadir enlaces a recursos útiles
    report_content.append("\n## 📚 Recursos Adicionales")
    report_content.append("\n- [Informe HTML Detallado](./log.html)")
    report_content.append("- [Reporte General de Robot Framework](./report.html)")
    report_content.append("- [Capturas de Pantalla](./screenshots)")

    if GEMINI_AVAILABLE:
        report_content.append("- [Análisis de IA con Gemini](./ai_analysis)")

    # Pie del informe
    report_content.append("\n---")
    ai_info = "con Gemini AI" if GEMINI_AVAILABLE else "con análisis básico"
    report_content.append(
        f"\n*Informe generado automáticamente por RobotFramework-Gemini-Demo {ai_info} - {current_date}*")

    # Escribir el archivo markdown con codificación UTF-8 explícita
    output_file = Path(output_path)
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(report_content))
        print(f"✅ Informe Markdown mejorado generado: {output_path}")
    except Exception as e:
        print(f"❌ Error escribiendo archivo: {e}")
        # Fallback: intentar con codificación cp1252 en Windows
        try:
            with open(output_file, 'w', encoding='cp1252', errors='replace') as f:
                f.write('\n'.join(report_content))
            print(f"⚠️ Informe generado con codificación alternativa: {output_path}")
        except Exception as e2:
            print(f"❌ Error crítico escribiendo archivo: {e2}")


def main():
    # Configurar codificación al inicio
    print("🔧 Configurando codificación UTF-8...")

    # Configurar rutas
    input_xml = "output.xml"
    output_dir = "results"
    output_file = f"{output_dir}/informe_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    # Verificar argumentos
    if len(sys.argv) > 1:
        input_xml = sys.argv[1]

    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
        output_file = f"{output_dir}/informe_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    # Crear directorio si no existe
    create_directory_if_not_exists(output_dir)

    # Verificar si existe el archivo XML
    if not os.path.exists(input_xml):
        print(f"❌ El archivo {input_xml} no existe")
        return

    # Procesar el archivo XML
    print(f"🔄 Procesando el archivo {input_xml}...")
    xml_root = parse_robot_output(input_xml)

    # Crear el informe en formato Markdown
    create_markdown_report(xml_root, output_file)


if __name__ == "__main__":
    main()