from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    # cia kad django zinotu tuos signalus
    def ready(self):
        from . signals import create_profile, save_profile