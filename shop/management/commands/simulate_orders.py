from django.core.management.base import BaseCommand
from db.commande_auto import lancer_simulation

class Command(BaseCommand):
    help = "Simule une commande aléatoire toutes les 60 secondes"

    def handle(self, *args, **kwargs):
        lancer_simulation()