#!/usr/bin/env python3
"""
SWITCH AI PROVIDER v1.0
Script para cambiar entre proveedores de IA dinamicamente

Uso:
    python tools/switch_ai_provider.py gemini
    python tools/switch_ai_provider.py claude
    python tools/switch_ai_provider.py aws
    python tools/switch_ai_provider.py --status
    python tools/switch_ai_provider.py --list
"""

import sys
import os
import argparse
from pathlib import Path

# Cargar variables de entorno
try:
    from dotenv import load_dotenv, set_key

    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv no disponible. Algunas funciones limitadas.")
    set_key = None

# Añadir directorio padre para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config.ai_config import AIConfigManager
except ImportError as e:
    print(f"ERROR: No se pudo importar AIConfigManager: {e}")
    sys.exit(1)


class ProviderSwitcher:
    """Cambiador de proveedores de IA"""

    def __init__(self):
        """Inicializar switcher"""
        try:
            self.ai_config = AIConfigManager()
            self.env_file = Path(__file__).parent.parent / ".env"
            print("OK ProviderSwitcher inicializado")
        except Exception as e:
            print(f"ERROR inicializando ProviderSwitcher: {e}")
            raise

    def switch_to_provider(self, provider_name: str) -> bool:
        """
        Cambiar a un proveedor especifico

        Args:
            provider_name: Nombre del proveedor (gemini, claude, aws)

        Returns:
            True si el cambio fue exitoso
        """
        print(f"\nCAMBIANDO A PROVEEDOR: {provider_name.upper()}")
        print("=" * 50)

        # 1. Verificar disponibilidad del proveedor
        verification = self.ai_config.verify_provider_availability(provider_name)

        print(f"Verificando {provider_name}...")
        if not verification["available"]:
            print(f"ERROR {provider_name} no esta disponible:")
            for issue in verification["issues"]:
                print(f"   - {issue}")

            # Sugerir soluciones
            self._suggest_fixes(provider_name, verification)
            return False

        print(f"OK {provider_name} esta disponible")

        # 2. Actualizar variable de entorno
        if self._update_env_provider(provider_name):
            print(f"OK Variable AI_PROVIDER actualizada en .env")
        else:
            print(f"WARNING No se pudo actualizar .env (continua con config)")

        # 3. Actualizar configuracion JSON
        if self.ai_config.set_active_provider(provider_name):
            print(f"OK Proveedor activo cambiado en configuracion")
        else:
            print(f"ERROR actualizando configuracion")
            return False

        # 4. Verificar el cambio
        current_provider = self.ai_config.get_active_provider()
        if current_provider == provider_name:
            print(f"\nCAMBIO EXITOSO!")
            print(f"   Proveedor activo: {current_provider}")
            print(f"   Estado: Operativo")

            # Mostrar siguiente paso
            self._show_next_steps(provider_name)
            return True
        else:
            print(f"ERROR: proveedor activo sigue siendo {current_provider}")
            return False

    def _update_env_provider(self, provider_name: str) -> bool:
        """Actualizar variable AI_PROVIDER en .env"""
        if not set_key:
            print("WARNING: No se puede actualizar .env (python-dotenv limitado)")
            return False

        try:
            if self.env_file.exists():
                set_key(str(self.env_file), "AI_PROVIDER", provider_name)
                return True
            else:
                # Crear .env si no existe
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(f"AI_PROVIDER={provider_name}\n")
                return True
        except Exception as e:
            print(f"ERROR actualizando .env: {e}")
            return False

    def _suggest_fixes(self, provider_name: str, verification: dict) -> None:
        """Sugerir soluciones para problemas del proveedor"""
        print(f"\nSOLUCIONES SUGERIDAS PARA {provider_name.upper()}:")

        if not verification["config_exists"]:
            print(f"   1. Verificar que existe config/ai_providers.json")
            print(f"   2. Verificar que {provider_name} esta en la configuracion")

        if not verification["enabled"]:
            print(f"   1. Editar config/ai_providers.json")
            print(f"   2. Cambiar 'enabled': true para {provider_name}")

        if not verification["has_api_key"]:
            config = self.ai_config.get_provider_config(provider_name)
            api_key_var = config.get("api_key_var", "API_KEY")
            print(f"   1. Configurar variable de entorno: {api_key_var}")
            print(f"   2. Agregar a .env: {api_key_var}=tu_api_key_aqui")

            if provider_name == "claude":
                print(f"   3. Obtener API key en: https://console.anthropic.com/")
            elif provider_name == "aws":
                print(f"   3. Configurar AWS credentials con aws configure")
                print(f"   4. O agregar AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY a .env")

    def _show_next_steps(self, provider_name: str) -> None:
        """Mostrar proximos pasos despues del cambio"""
        print(f"\nPROXIMOS PASOS:")
        print(f"   1. Instalar dependencias si es necesario:")

        if provider_name == "claude":
            print(f"      pip install anthropic>=0.25.0")
        elif provider_name == "aws":
            print(f"      pip install boto3>=1.34.0")

        print(f"   2. Verificar funcionamiento:")
        print(f"      python -c \"from config.ai_config import AIConfigManager; AIConfigManager().print_status()\"")

        print(f"   3. Ejecutar tests:")
        print(f"      robot tests/login/siesa_login_tests.robot")

    def show_status(self) -> None:
        """Mostrar estado actual del sistema"""
        self.ai_config.print_status()

    def list_providers(self) -> None:
        """Listar todos los proveedores disponibles"""
        print(f"\nPROVEEDORES CONFIGURADOS:")

        all_providers = self.ai_config._config.get("providers", {})
        available = self.ai_config.get_available_providers()
        active = self.ai_config.get_active_provider()

        for provider_name, config in all_providers.items():
            # Iconos de estado
            active_icon = "ACTIVO" if provider_name == active else "      "
            available_icon = "OK" if provider_name in available else "ERROR"
            enabled_icon = "ON" if config.get("enabled", False) else "OFF"

            print(f"   {active_icon} {available_icon} {enabled_icon} {provider_name}")
            print(f"      Nombre: {config.get('name', 'N/A')}")
            print(f"      API Key: {config.get('api_key_var', 'N/A')}")

            if provider_name not in available:
                verification = self.ai_config.verify_provider_availability(provider_name)
                for issue in verification["issues"]:
                    print(f"      WARNING: {issue}")
            print()

        print(f"Leyenda:")
        print(f"   ACTIVO = Proveedor en uso   OK = Disponible   ERROR = No disponible")
        print(f"   ON = Habilitado   OFF = Deshabilitado")


def main():
    """Funcion principal"""
    parser = argparse.ArgumentParser(
        description="Cambiador de proveedores de IA para Robot Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python tools/switch_ai_provider.py gemini     # Cambiar a Gemini
  python tools/switch_ai_provider.py claude     # Cambiar a Claude  
  python tools/switch_ai_provider.py aws        # Cambiar a AWS
  python tools/switch_ai_provider.py --status   # Mostrar estado
  python tools/switch_ai_provider.py --list     # Listar proveedores
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("provider", nargs="?", help="Proveedor a activar (gemini, claude, aws)")
    group.add_argument("--status", "-s", action="store_true", help="Mostrar estado actual")
    group.add_argument("--list", "-l", action="store_true", help="Listar todos los proveedores")

    args = parser.parse_args()

    try:
        switcher = ProviderSwitcher()

        if args.status:
            switcher.show_status()
        elif args.list:
            switcher.list_providers()
        elif args.provider:
            provider = args.provider.lower()
            if provider not in ["gemini", "claude", "aws"]:
                print(f"ERROR: Proveedor no valido: {provider}")
                print(f"   Proveedores validos: gemini, claude, aws")
                sys.exit(1)

            success = switcher.switch_to_provider(provider)
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\nOperacion cancelada por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()