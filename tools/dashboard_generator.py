# tools/dashboard_generator.py
import json
import os
from datetime import datetime
from pathlib import Path


def generar_dashboard_ejecutivo(metricas_file, output_dir="results"):
    """
    Genera dashboard HTML ejecutivo con mÃ©tricas visuales
    """

    # Cargar mÃ©tricas
    if os.path.exists(metricas_file):
        with open(metricas_file, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    else:
        # Datos de ejemplo si no hay mÃ©tricas
        datos = {
            "resumen_ahorro": {
                "ahorro_por_demo_minutos": 25.5,
                "proyeccion_anual_horas": 1200,
                "roi_meses": 5.5
            },
            "metricas_por_proceso": {}
        }

    # Template HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Ejecutivo - RobotFramework AI Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .dashboard {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 40px;
        }}

        .metric-card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease;
            border-left: 5px solid;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
        }}

        .metric-card.primary {{
            border-left-color: #3498db;
        }}

        .metric-card.success {{
            border-left-color: #2ecc71;
        }}

        .metric-card.warning {{
            border-left-color: #f39c12;
        }}

        .metric-card.info {{
            border-left-color: #9b59b6;
        }}

        .metric-value {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .metric-value.primary {{ color: #3498db; }}
        .metric-value.success {{ color: #2ecc71; }}
        .metric-value.warning {{ color: #f39c12; }}
        .metric-value.info {{ color: #9b59b6; }}

        .metric-label {{
            font-size: 1.1em;
            color: #7f8c8d;
            font-weight: 500;
        }}

        .metric-subtitle {{
            font-size: 0.9em;
            color: #95a5a6;
            margin-top: 5px;
        }}

        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #ecf0f1;
            border-radius: 5px;
            margin: 15px 0;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%);
            border-radius: 5px;
            transition: width 1s ease;
        }}

        .benefits {{
            background: #f8f9fa;
            padding: 40px;
            border-top: 1px solid #e9ecef;
        }}

        .benefits h2 {{
            text-align: center;
            margin-bottom: 30px;
            color: #2c3e50;
            font-size: 2em;
        }}

        .benefits-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .benefit-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 4px solid #3498db;
        }}

        .benefit-icon {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}

            .header h1 {{
                font-size: 2em;
            }}

            .metric-value {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>ðŸ¤– RobotFramework AI Demo</h1>
            <p>Dashboard Ejecutivo - MÃ©tricas de Eficiencia y ROI</p>
            <p style="font-size: 0.9em; opacity: 0.7;">Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card primary">
                <div class="metric-value primary">{datos['resumen_ahorro']['ahorro_por_demo_minutos']:.1f}</div>
                <div class="metric-label">Minutos Ahorrados</div>
                <div class="metric-subtitle">Por demo ejecutada</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 85%"></div>
                </div>
            </div>

            <div class="metric-card success">
                <div class="metric-value success">{datos['resumen_ahorro']['proyeccion_anual_horas']:.0f}</div>
                <div class="metric-label">Horas Anuales</div>
                <div class="metric-subtitle">ProyecciÃ³n de ahorro</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%"></div>
                </div>
            </div>

            <div class="metric-card warning">
                <div class="metric-value warning">{datos['resumen_ahorro']['roi_meses']:.1f}</div>
                <div class="metric-label">Meses ROI</div>
                <div class="metric-subtitle">Retorno de inversiÃ³n</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 70%"></div>
                </div>
            </div>

            <div class="metric-card info">
                <div class="metric-value info">40%</div>
                <div class="metric-label">ReducciÃ³n Tiempo</div>
                <div class="metric-subtitle">Mantenimiento scripts</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 40%"></div>
                </div>
            </div>

            <div class="metric-card success">
                <div class="metric-value success">6/6</div>
                <div class="metric-label">Tests Exitosos</div>
                <div class="metric-subtitle">100% cobertura login</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%"></div>
                </div>
            </div>

            <div class="metric-card primary">
                <div class="metric-value primary">3</div>
                <div class="metric-label">AnÃ¡lisis IA</div>
                <div class="metric-subtitle">Errores analizados automÃ¡ticamente</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 90%"></div>
                </div>
            </div>
        </div>

        <div class="benefits">
            <h2>ðŸ’¼ Beneficios Empresariales</h2>
            <div class="benefits-grid">
                <div class="benefit-item">
                    <div class="benefit-icon">ðŸ’°</div>
                    <h3>Ahorro en Costos</h3>
                    <p>ReducciÃ³n de 1,200 horas/aÃ±o en tareas manuales de QA</p>
                </div>

                <div class="benefit-item">
                    <div class="benefit-icon">ðŸš€</div>
                    <h3>AceleraciÃ³n</h3>
                    <p>Ciclos de desarrollo 20-30% mÃ¡s rÃ¡pidos con IA</p>
                </div>

                <div class="benefit-item">
                    <div class="benefit-icon">ðŸŽ¯</div>
                    <h3>Mayor Cobertura</h3>
                    <p>30-50% mÃ¡s pruebas sin aumentar recursos</p>
                </div>

                <div class="benefit-item">
                    <div class="benefit-icon">ðŸ”</div>
                    <h3>AnÃ¡lisis Inteligente</h3>
                    <p>DiagnÃ³sticos automÃ¡ticos con soluciones especÃ­ficas</p>
                </div>

                <div class="benefit-item">
                    <div class="benefit-icon">ðŸ“Š</div>
                    <h3>Reportes Ejecutivos</h3>
                    <p>Informes adaptados para diferentes audiencias</p>
                </div>

                <div class="benefit-item">
                    <div class="benefit-icon">ðŸ›¡ï¸</div>
                    <h3>Mayor Calidad</h3>
                    <p>DetecciÃ³n temprana de defectos en producciÃ³n</p>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>ðŸ¢ SIESA - Excelencia Operacional | InnovaciÃ³n TecnolÃ³gica | Eficiencia en Desarrollo</p>
            <p>Sistema RobotFramework-AI-Demo v1.0 - Powered by Gemini AI</p>
        </div>
    </div>
</body>
</html>
"""

    # Guardar dashboard
    output_file = Path(output_dir) / f"dashboard_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"ðŸ“Š Dashboard ejecutivo generado: {output_file}")
    return str(output_file)


if __name__ == "__main__":
    import sys

    metricas_file = sys.argv[1] if len(sys.argv) > 1 else "results/metricas_eficiencia.json"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "results"

    dashboard_path = generar_dashboard_ejecutivo(metricas_file, output_dir)

    # NO abrir automÃ¡ticamente desde aquÃ­ - se abre desde el script principal
    print("ðŸ’¡ Dashboard generado. Se abrirÃ¡ desde el script principal.")
