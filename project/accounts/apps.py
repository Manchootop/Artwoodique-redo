from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.accounts'

    def ready(self):
        import project.accounts.signals  # noqa: F401