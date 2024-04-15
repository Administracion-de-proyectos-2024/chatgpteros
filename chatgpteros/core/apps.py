from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
<<<<<<< Updated upstream:chatgpteros/core/apps.py
    name = 'core'
=======
    name = 'applications.core'

    def ready(self):
        import applications.core.customs_filters
>>>>>>> Stashed changes:chatgpteros/applications/core/apps.py
