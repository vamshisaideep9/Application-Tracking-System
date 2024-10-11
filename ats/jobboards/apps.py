from django.apps import AppConfig


class JobboardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobboards'

    def ready(self):
        import jobboards.signals
