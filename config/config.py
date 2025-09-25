"""
ConfigManager v1.2 - Gestor de configuración centralizada
Maneja credenciales desde un archivo JSON maestro
"""
import json
import os
from pathlib import Path


class ConfigManager:
    """Gestor centralizado de configuración para el proyecto v1.2"""
    
    def __init__(self, credentials_file=None):
        """
        Inicializa el ConfigManager
        
        Args:
            credentials_file: Ruta al archivo de credenciales. Si no se especifica, usa la ruta por defecto.
        """
        if credentials_file:
            self.credentials_file = credentials_file
        else:
            # Ruta por defecto relativa al directorio del script
            current_dir = Path(__file__).parent
            self.credentials_file = current_dir / "credentials.json"
        
        self.config_data = None
        self._load_config()
    
    def _load_config(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(f"Archivo de credenciales no encontrado: {self.credentials_file}")
            
            # Leer con encoding utf-8-sig para manejar BOM
            with open(self.credentials_file, 'r', encoding='utf-8-sig') as f:
                self.config_data = json.load(f)
                
        except Exception as e:
            raise Exception(f"Error cargando configuración: {e}")
    
    def get_all_valid_credentials(self):
        """
        Obtiene todas las credenciales válidas de todos los entornos
        
        Returns:
            list: Lista de todas las credenciales válidas
        """
        if not self.config_data:
            return []
        
        all_credentials = []
        environments = self.config_data.get("environments", {})
        
        for env_name, env_data in environments.items():
            credentials = env_data.get("credentials", [])
            for cred in credentials:
                if cred.get("activo", True):
                    # Agregar información del entorno
                    cred_copy = cred.copy()
                    cred_copy["entorno"] = env_name
                    cred_copy["url"] = env_data.get("url", "")
                    all_credentials.append(cred_copy)
        
        # Ordenar por prioridad
        all_credentials.sort(key=lambda x: x.get("prioridad", 999))
        return all_credentials
    
    def get_credentials_by_environment(self, environment):
        """
        Obtiene credenciales para un entorno específico
        
        Args:
            environment: Nombre del entorno (qa, dev, prod)
            
        Returns:
            list: Lista de credenciales para el entorno especificado
        """
        if not self.config_data:
            return []
        
        env_data = self.config_data.get("environments", {}).get(environment, {})
        credentials = env_data.get("credentials", [])
        
        # Filtrar solo credenciales activas y agregar información del entorno
        active_credentials = []
        for cred in credentials:
            if cred.get("activo", True):
                cred_copy = cred.copy()
                cred_copy["entorno"] = environment
                cred_copy["url"] = env_data.get("url", "")
                active_credentials.append(cred_copy)
        
        # Ordenar por prioridad
        active_credentials.sort(key=lambda x: x.get("prioridad", 999))
        return active_credentials
    
    def get_priority_credential(self, environment="qa"):
        """
        Obtiene la credencial de mayor prioridad para un entorno
        
        Args:
            environment: Entorno para buscar la credencial prioritaria
            
        Returns:
            dict: Credencial de mayor prioridad o None si no hay credenciales
        """
        credentials = self.get_credentials_by_environment(environment)
        return credentials[0] if credentials else None
    
    def validate_config(self):
        """
        Valida que la configuración sea correcta
        
        Returns:
            dict: Resultado de la validación con detalles
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        try:
            if not self.config_data:
                result["valid"] = False
                result["errors"].append("No se pudo cargar la configuración")
                return result
            
            # Validar estructura básica
            if "environments" not in self.config_data:
                result["valid"] = False
                result["errors"].append("Falta la sección 'environments'")
            
            # Validar entornos
            environments = self.config_data.get("environments", {})
            if not environments:
                result["valid"] = False
                result["errors"].append("No hay entornos configurados")
            
            total_credentials = 0
            active_credentials = 0
            
            for env_name, env_data in environments.items():
                if "credentials" not in env_data:
                    result["warnings"].append(f"Entorno '{env_name}' no tiene credenciales")
                    continue
                
                credentials = env_data.get("credentials", [])
                total_credentials += len(credentials)
                
                for cred in credentials:
                    if cred.get("activo", True):
                        active_credentials += 1
            
            # Estadísticas
            result["stats"] = {
                "total_environments": len(environments),
                "total_credentials": total_credentials,
                "active_credentials": active_credentials
            }
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Error durante validación: {e}")
        
        return result


if __name__ == "__main__":
    # Test básico del ConfigManager
    try:
        cm = ConfigManager()
        print("ConfigManager inicializado correctamente")
        
        creds = cm.get_all_valid_credentials()
        print(f"Credenciales cargadas: {len(creds)}")
        
        for c in creds:
            print(f"Usuario: {c['usuario']} - Tipo: {c['tipo']}")
        
    except Exception as e:
        print(f"Error: {e}")