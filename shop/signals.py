from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Produit, Categorie
from db.mongo import get_produits, get_db


# ── Sync Produit ──────────────────────────────────────────────────────────────

@receiver(post_save, sender=Produit)
def sync_produit_to_mongo(sender, instance, created, **kwargs):
    try:
        col = get_produits()

        # Cherche le document existant par _id MongoDB ou par nom
        doc = col.find_one({'id': instance.id})
        if doc is None:
            doc = col.find_one({'nom': instance.nom})

        champs = {
            'id':          instance.id,
            'nom':         instance.nom,
            'prix':        float(instance.prix),
            'description': instance.description or '',
            'categorie':   instance.categorie.name if instance.categorie else '',
            'stock':       getattr(instance, 'stock', 100),
            'producteur':  getattr(instance, 'producteur', ''),
        }

        if doc is None:
            # ── Nouveau produit → INSERT ──────────────────────────
            champs['image']     = ''
            champs['attributs'] = {}
            result = col.insert_one(champs)
            print(f"[SIGNAL]  INSERT MongoDB — '{instance.nom}' (Django id={instance.id}, Mongo _id={result.inserted_id})")
        else:
            # ── Produit existant → UPDATE ─────────────────────────
            col.update_one(
                {'_id': doc['_id']},
                {'$set': champs}
            )
            print(f"[SIGNAL]  UPDATE MongoDB — '{instance.nom}' (id={instance.id})")

    except Exception as e:
        import traceback
        print(f"[SIGNAL]  ERREUR sync Produit : {e}")
        traceback.print_exc()


@receiver(post_delete, sender=Produit)
def delete_produit_from_mongo(sender, instance, **kwargs):
    try:
        col = get_produits()
        doc = col.find_one({'id': instance.id})
        if doc is None:
            doc = col.find_one({'nom': instance.nom})

        if doc:
            col.delete_one({'_id': doc['_id']})
            print(f"[SIGNAL]   DELETE MongoDB — '{instance.nom}' (id={instance.id})")
        else:
            print(f"[SIGNAL]   DELETE : '{instance.nom}' introuvable dans MongoDB")

    except Exception as e:
        print(f"[SIGNAL]  ERREUR delete Produit : {e}")


# ── Sync Categorie ────────────────────────────────────────────────────────────

@receiver(post_save, sender=Categorie)
def sync_categorie_to_mongo(sender, instance, created, **kwargs):
    """
    Quand une catégorie est renommée dans l'admin,
    met à jour tous les produits MongoDB qui avaient l'ancien nom.
    """
    try:
        col = get_produits()
        # On ne peut pas connaître l'ancien nom facilement,
        # donc on re-sync tous les produits de cette catégorie
        from shop.models import Produit as ProduitModel
        produits = ProduitModel.objects.filter(categorie=instance)
        for p in produits:
            col.update_one(
                {'id': p.id},
                {'$set': {'categorie': instance.name}}
            )
        if created:
            print(f"[SIGNAL]  Catégorie créée : '{instance.name}'")
        else:
            print(f"[SIGNAL]  Catégorie mise à jour : '{instance.name}' — {produits.count()} produit(s) mis à jour")

    except Exception as e:
        print(f"[SIGNAL]  ERREUR sync Catégorie : {e}")


@receiver(post_delete, sender=Categorie)
def delete_categorie_from_mongo(sender, instance, **kwargs):
    """
    Quand une catégorie est supprimée, met 'Sans catégorie'
    pour les produits MongoDB orphelins.
    """
    try:
        col = get_produits()
        result = col.update_many(
            {'categorie': instance.name},
            {'$set': {'categorie': 'Sans catégorie'}}
        )
        print(f"[SIGNAL]   Catégorie supprimée : '{instance.name}' — {result.modified_count} produit(s) mis à jour")

    except Exception as e:
        print(f"[SIGNAL]  ERREUR delete Catégorie : {e}")