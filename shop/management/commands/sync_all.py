from django.core.management.base import BaseCommand
from shop.models import Produit
from db.mongo import get_produits


class Command(BaseCommand):
    help = "Force la synchronisation complète Django Admin → MongoDB"

    def handle(self, *args, **kwargs):
        col = get_produits()
        produits_django = Produit.objects.all()

        for p in produits_django:
            # Cherche par id ou par nom
            doc = col.find_one({'id': p.id}) or col.find_one({'nom': p.nom})

            data = {
                'id':          p.id,
                'nom':         p.nom,
                'prix':        float(p.prix),
                'description': p.description or '',
                'categorie':   p.categorie.name if p.categorie else '',
            }

            if doc:
                col.update_one({'_id': doc['_id']}, {'$set': data})
                self.stdout.write(f"🔄 Mis à jour : {p.nom}")
            else:
                col.insert_one(data)
                self.stdout.write(f"✅ Créé dans MongoDB : {p.nom}")

        # Supprimer de MongoDB les produits qui n'existent plus dans Django
        django_noms = set(Produit.objects.values_list('nom', flat=True))
        for doc in col.find({}):
            if doc.get('nom') not in django_noms:
                col.delete_one({'_id': doc['_id']})
                self.stdout.write(f"🗑️  Supprimé de MongoDB : {doc.get('nom')}")

        self.stdout.write("\n✅ Synchronisation complète terminée")