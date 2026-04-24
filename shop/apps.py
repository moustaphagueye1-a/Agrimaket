from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        try:
            import shop.signals
            print("[SHOP] ✅ Signals MongoDB chargés")
        except Exception as e:
            print(f"[SHOP] ❌ Erreur chargement signals : {e}")