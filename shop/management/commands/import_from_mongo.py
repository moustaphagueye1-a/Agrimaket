from django.core.management.base import BaseCommand
from shop.models import Produit, Categorie
from db.mongo import get_produits


class Command(BaseCommand):
    help = "Importe tous les produits MongoDB dans l'admin Django"

    def handle(self, *args, **kwargs):
        col = get_produits()
        produits_mongo = list(col.find({}))
        created = 0
        updated = 0

        for doc in produits_mongo:
            mongo_id   = doc.get('id')
            nom        = doc.get('nom', '')
            prix       = doc.get('prix', 0)
            description = doc.get('description', '')
            cat_name   = doc.get('categorie', 'Divers')

            if not nom or mongo_id is None:
                continue

            # Créer ou récupérer la catégorie
            categorie, _ = Categorie.objects.get_or_create(name=cat_name)

            # Vérifier si un produit Django avec ce nom existe déjà
            produit_qs = Produit.objects.filter(nom=nom)

            if produit_qs.exists():
                p = produit_qs.first()
                p.prix        = prix
                p.description = description
                p.categorie   = categorie
                p.save()
                updated += 1
                self.stdout.write(f"  Mis à jour : {nom}")
            else:
                p = Produit.objects.create(
                    nom         = nom,
                    prix        = prix,
                    description = description,
                    categorie   = categorie,
                )
                self.stdout.write(f"  Créé : {nom} (Django id={p.id})")
                created += 1

            # Mettre à jour MongoDB avec le vrai id Django
            col.update_one(
                {'id': mongo_id},
                {'$set': {'id': p.id}}
            )

        self.stdout.write(f"\n Import terminé : {created} créés, {updated} mis à jour")
        self.stdout.write(" Les ids MongoDB ont été mis à jour pour correspondre aux ids Django")