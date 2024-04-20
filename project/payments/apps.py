from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.payments'

    def ready(self):
        import project.payments.hooks  # noqa: F401