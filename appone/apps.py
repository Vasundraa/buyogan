from django.apps import AppConfig


class ApponeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appone'

    def ready(self):
        import appone.signals 