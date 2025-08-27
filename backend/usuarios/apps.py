"""
Configuración de la app usuarios
"""
from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    verbose_name = 'Gestión de Usuarios'
    
    def ready(self):
        """Importar signals cuando la app esté lista"""
        import usuarios.models  # Esto asegura que los signals se registren