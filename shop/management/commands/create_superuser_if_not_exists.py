from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Produit, Categorie
from db.mongo import get_produits


class Command(BaseCommand):
    help = "Setup complet : superuser + sync MongoDB → Django"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        # ─────────────────────────────
        # 1. SUPERUSER FIXE
        # ─────────────────────────────
        username = "amdy"
        email = "moustaphag2003@gmail.com"
        password = "Tapha2003"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser créé avec succès"))
        else:
            self.stdout.write(self.style.WARNING("Superuser existe déjà"))

        # ─────────────────────────────
        # 2. SYNC MONGODB → DJANGO
        # ─────────────────────────────
        col = get_produits()
        produits_mongo = list(col.find({}))
        created = 0

        for doc in produits_mongo:
            nom = doc.get('nom', '')
            if not nom:
                continue

            cat_name = doc.get('categorie', 'Divers')
            cat, _ = Categorie.objects.get_or_create(name=cat_name)

            p, was_created = Produit.objects.get_or_create(
                nom=nom,
                defaults={
                    'prix': doc.get('prix', 0),
                    'description': doc.get('description', ''),
                    'categorie': cat,
                    'image': doc.get('image', '')  # important pour tes images
                }
            )

            if was_created:
                created += 1

                col.update_one(
                    {'_id': doc['_id']},
                    {'$set': {'id': p.id}}
                )

        self.stdout.write(self.style.SUCCESS(
            f"{created} produits importés depuis MongoDB"
        ))