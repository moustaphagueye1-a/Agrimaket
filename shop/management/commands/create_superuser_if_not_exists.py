from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Créer un superuser automatiquement si n'existe pas"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "amdy"
        email = "moustaphag2003@gmail.com"
        password = "Tapha2003"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser existe déjà"))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Superuser créé avec succès"))