from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
<<<<<<< Updated upstream:chatgpteros/core/apps.py
    name = 'core'
<<<<<<< HEAD
=======
    name = 'applications.core'

    def ready(self):
        import applications.core.customs_filters
>>>>>>> Stashed changes:chatgpteros/applications/core/apps.py
=======

    def ready(self):
        import core.customs_filters  # Importa tu archivo de filtros personalizados aquí
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6
