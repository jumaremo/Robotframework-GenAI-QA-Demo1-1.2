"""
AI CONFIG MANAGER v1.0
Gestor centralizado de proveedores de IA para Robot Framework v1.2+

Caracteristicas:
- Extiende ConfigManager v1.2 existente
- Mantiene compatibilidad total con GeminiLibrary
- Soporte para multiples proveedores (Gemini, Claude, AWS)
- Fallback automatico entre proveedores
- Configuracion centralizada en ai_providers.json
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()  # Cargar .env automáticamente
    print("OK Variables de entorno cargadas desde .env")
except ImportError:
    print("WARNING python-dotenv no instalado. Variables de entorno limitadas.")
except Exception as e:
    print(f"WARNING Error cargando .env: {e}")

# Importar ConfigManager v1.2 existente
try:
    from config.config import ConfigManager
    CONFIG_MANAGER_AVAILABLE = True
    print("OK ConfigManager v1.2 importado correctamente")
except ImportError as e:
    CONFIG_MANAGER_AVAILABLE = False
    print(f"WARNING No se pudo importar ConfigManager: {e}")


class AIConfigManager:
    """Gestor de configuracion para multiples proveedores de IA"""

    def __init__(self, config_file: str = None):
        """
        Inicializar gestor de configuracion AI

        Args:
            config_file: Ruta al archivo de configuracion (opcional)
        """
        self.base_path = Path(__file__).parent
        self.config_file = config_file or self.base_path / "ai_providers.json"

        # Integrar con ConfigManager v1.2 si esta disponible
        self.config_manager = None
        if CONFIG_MANAGER_AVAILABLE:
            try:
                self.config_manager = ConfigManager()
                print("OK ConfigManager v1.2 integrado con AIConfigManager")
            except Exception as e:
                print(f"WARNING Error inicializando ConfigManager: {e}")

        self._config = None
        self._load_config()

    def _load_config(self) -> None:
        """Cargar configuracion desde archivo JSON"""
        try:
            if not self.config_file.exists():
                raise FileNotFoundError(f"Archivo de configuracion no encontrado: {self.config_file}")

            # Intentar multiples encodings para mayor robustez
            encodings = ['utf-8-sig', 'utf-8', 'latin-1']
            config_loaded = False

            for encoding in encodings:
                try:
                    with open(self.config_file, 'r', encoding=encoding) as f:
                        self._config = json.load(f)
                    print(f"OK Configuracion AI cargada desde: {self.config_file} ({encoding})")
                    config_loaded = True
                    break
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    print(f"WARNING Error con encoding {encoding}: {e}")
                    continue

            if not config_loaded:
                raise Exception("No se pudo cargar con ningun encoding")

        except Exception as e:
            print(f"ERROR cargando configuracion AI: {e}")
            # Configuracion por defecto para fallback
            self._config = {
                "providers": {"gemini": {"enabled": True}},
                "settings": {"active_provider": "gemini"}
            }

    def get_active_provider(self) -> str:
        """Obtener proveedor activo"""
        return self._config.get("settings", {}).get("active_provider", "gemini")

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Obtener configuracion de un proveedor especifico

        Args:
            provider_name: Nombre del proveedor (gemini, claude, aws)

        Returns:
            Dict con configuracion del proveedor
        """
        providers = self._config.get("providers", {})
        if provider_name not in providers:
            raise ValueError(f"Proveedor no configurado: {provider_name}")

        return providers[provider_name]

    def is_provider_enabled(self, provider_name: str) -> bool:
        """Verificar si un proveedor esta habilitado"""
        try:
            config = self.get_provider_config(provider_name)
            return config.get("enabled", False)
        except ValueError:
            return False

    def get_api_key(self, provider_name: str) -> Optional[str]:
        """
        Obtener API key para un proveedor especifico

        Args:
            provider_name: Nombre del proveedor

        Returns:
            API key desde variables de entorno
        """
        try:
            config = self.get_provider_config(provider_name)
            api_key_var = config.get("api_key_var")

            if not api_key_var:
                return None

            return os.getenv(api_key_var)

        except ValueError:
            return None

    def verify_provider_availability(self, provider_name: str) -> Dict[str, Any]:
        """
        Verificar disponibilidad completa de un proveedor

        Args:
            provider_name: Nombre del proveedor

        Returns:
            Dict con estado de verificacion
        """
        result = {
            "provider": provider_name,
            "available": False,
            "enabled": False,
            "has_api_key": False,
            "config_exists": False,
            "issues": []
        }

        try:
            # Verificar configuracion
            config = self.get_provider_config(provider_name)
            result["config_exists"] = True

            # Verificar si esta habilitado
            result["enabled"] = config.get("enabled", False)
            if not result["enabled"]:
                result["issues"].append("Proveedor deshabilitado en configuracion")

            # Verificar API key
            api_key = self.get_api_key(provider_name)
            result["has_api_key"] = bool(api_key and api_key.strip())
            if not result["has_api_key"]:
                result["issues"].append(f"API key no encontrada: {config.get('api_key_var', 'N/A')}")

            # Estado general
            result["available"] = result["enabled"] and result["has_api_key"]

        except ValueError as e:
            result["issues"].append(str(e))

        return result

    def get_available_providers(self) -> List[str]:
        """Obtener lista de proveedores disponibles"""
        available = []
        for provider_name in self._config.get("providers", {}):
            if self.verify_provider_availability(provider_name)["available"]:
                available.append(provider_name)
        return available

    def set_active_provider(self, provider_name: str) -> bool:
        """
        Cambiar proveedor activo

        Args:
            provider_name: Nombre del nuevo proveedor activo

        Returns:
            True si el cambio fue exitoso
        """
        # Verificar que el proveedor este disponible
        verification = self.verify_provider_availability(provider_name)

        if not verification["available"]:
            print(f"ERROR No se puede activar {provider_name}:")
            for issue in verification["issues"]:
                print(f"   - {issue}")
            return False

        # Actualizar configuracion
        self._config["settings"]["active_provider"] = provider_name

        # Guardar configuracion actualizada
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)

            print(f"OK Proveedor activo cambiado a: {provider_name}")
            return True

        except Exception as e:
            print(f"ERROR guardando configuracion: {e}")
            return False

    def get_credentials_for_provider(self, provider_name: str, credential_type: str = "qa") -> Dict[str, str]:
        """
        Obtener credenciales usando ConfigManager v1.2 para un proveedor especifico

        Args:
            provider_name: Nombre del proveedor
            credential_type: Tipo de credencial (qa, admin, etc.)

        Returns:
            Dict con credenciales desde sistema centralizado v1.2
        """
        if self.config_manager:
            try:
                # Usar get_priority_credential que es el metodo correcto
                return self.config_manager.get_priority_credential(credential_type)
            except Exception as e:
                print(f"WARNING Error obteniendo credenciales v1.2: {e}")

        # Fallback a credenciales por defecto
        return {
            "usuario": "juan.reina",
            "clave": "1235",
            "tipo": credential_type,
            "source": "fallback"
        }

    def get_fallback_providers(self) -> List[str]:
        """Obtener lista de proveedores de fallback en orden de prioridad"""
        fallback_order = self._config.get("settings", {}).get("fallback_order", ["gemini"])
        available = self.get_available_providers()

        # Filtrar solo proveedores disponibles manteniendo el orden
        return [provider for provider in fallback_order if provider in available]

    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado completo del sistema multi-proveedor"""
        status = {
            "version": self._config.get("version", "1.0"),
            "active_provider": self.get_active_provider(),
            "total_providers": len(self._config.get("providers", {})),
            "available_providers": self.get_available_providers(),
            "v12_compatibility": self.config_manager is not None,
            "config_file": str(self.config_file),
            "providers_detail": {}
        }

        # Detalle por proveedor
        for provider_name in self._config.get("providers", {}):
            status["providers_detail"][provider_name] = self.verify_provider_availability(provider_name)

        return status

    def print_status(self) -> None:
        """Imprimir estado del sistema de forma legible"""
        status = self.get_system_status()

        print(f"\nSISTEMA MULTI-PROVEEDOR v{status['version']}")
        print(f"Archivo: {status['config_file']}")
        print(f"Proveedor activo: {status['active_provider']}")
        print(f"Disponibles: {len(status['available_providers'])}/{status['total_providers']}")
        print(f"Compatibilidad v1.2: {'OK' if status['v12_compatibility'] else 'ERROR'}")

        print(f"\nDETALLE POR PROVEEDOR:")
        for provider, detail in status["providers_detail"].items():
            icon = "OK" if detail["available"] else "ERROR"
            print(f"   {icon} {provider}: {'Disponible' if detail['available'] else 'No disponible'}")
            if detail["issues"]:
                for issue in detail["issues"]:
                    print(f"      - {issue}")


# Funcion de utilidad para uso rapido
def get_ai_config() -> AIConfigManager:
    """Obtener instancia de AIConfigManager"""
    return AIConfigManager()


# Test basico
if __name__ == "__main__":
    print("TESTING AI CONFIG MANAGER...")

    try:
        ai_config = AIConfigManager()
        ai_config.print_status()

        # Test compatibilidad v1.2
        print(f"\nTest compatibilidad v1.2:")
        creds = ai_config.get_credentials_for_provider("gemini", "qa")
        print(f"OK Credenciales v1.2: {creds['usuario']}/{creds['clave']}")

    except Exception as e:
        print(f"ERROR en test: {e}")