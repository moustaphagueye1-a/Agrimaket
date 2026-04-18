# shop/apps.py
from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        # Active les signals dès le démarrage de Django
        import shop.signals  # noqa