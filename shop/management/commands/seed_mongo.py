from django.core.management.base import BaseCommand
from db.seed import seed

class Command(BaseCommand):
    help = "Insère les 15 produits sénégalais dans MongoDB"

    def handle(self, *args, **kwargs):
        seed()