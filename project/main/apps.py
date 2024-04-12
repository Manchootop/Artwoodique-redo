from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.main'

    def ready(self):
        import project.orders.signals  # noqa: F401