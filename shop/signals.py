# shop/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Produit
from db.mongo import get_produits


def _produit_to_mongo_doc(produit):
    """
    Convertit un objet Produit Django en document MongoDB.
    On utilise l'id Django comme clé de jointure (champ 'id' dans MongoDB).
    """
    return {
        'id':          produit.id,
        'nom':         produit.nom,
        'prix':        produit.prix,
        'description': produit.description,
        'categorie':   produit.categorie.name if produit.categorie else '',
        'stock':       100,   # stock par défaut à la création depuis l'admin
        'producteur':  '',    # à remplir manuellement si besoin
        'image':       '',    # l'image est gérée côté Django, pas stockée dans Mongo
        'attributs':   {},    # attributs vides par défaut, éditables via Mongo Express
    }


@receiver(post_save, sender=Produit)
def sync_produit_to_mongo(sender, instance, created, **kwargs):
    """
    Appelé automatiquement après chaque save() d'un Produit Django.
    - Création  → insert dans MongoDB
    - Mise à jour → update dans MongoDB
    """
    col = get_produits()
    doc = _produit_to_mongo_doc(instance)

    if created:
        # Nouveau produit → insérer dans MongoDB
        col.insert_one(doc)
        print(f"[SYNC] ✅ Produit '{instance.nom}' inséré dans MongoDB (id={instance.id})")
    else:
        # Mise à jour → mettre à jour dans MongoDB (sans écraser le stock actuel)
        col.update_one(
            {'id': instance.id},
            {'$set': {
                'nom':         doc['nom'],
                'prix':        doc['prix'],
                'description': doc['description'],
                'categorie':   doc['categorie'],
                'image':       doc['image'],
            }}
        )
        print(f"[SYNC] 🔄 Produit '{instance.nom}' mis à jour dans MongoDB (id={instance.id})")


@receiver(post_delete, sender=Produit)
def delete_produit_from_mongo(sender, instance, **kwargs):
    """
    Appelé automatiquement après chaque delete() d'un Produit Django.
    Supprime le document correspondant dans MongoDB.
    """
    get_produits().delete_one({'id': instance.id})
    print(f"[SYNC] 🗑️  Produit '{instance.nom}' supprimé de MongoDB (id={instance.id})")