from db.mongo import get_produits, get_commandes

# ── 1. Produits en rupture de stock (stock < 5) ───────────────────────────
def produits_rupture_stock():
    return list(get_produits().find({"stock": {"$lt": 5}}))

# ── 2. Chiffre d'affaires total par catégorie ────────────────────────────
def ca_par_categorie():
    pipeline = [
        {"$unwind": "$articles"},
        {"$group": {
            "_id": "$articles.categorie",
            "total_ca": {
                "$sum": {
                    "$multiply": ["$articles.prix_unitaire", "$articles.quantite"]
                }
            },
            "nb_commandes": {"$sum": 1}
        }},
        {"$sort": {"total_ca": -1}}
    ]
    return list(get_commandes().aggregate(pipeline))

# ── 3. Historique des commandes d'un client (par email) ──────────────────
def historique_client(email):
    return list(get_commandes().find(
        {"client.email": email},
        sort=[("date", -1)]
    ))

# ── 4. Décrémenter le stock après une commande ───────────────────────────
def decrementer_stock(produit_id_int, quantite):
    get_produits().update_one(
        {"id": produit_id_int},
        {"$inc": {"stock": -quantite}}
    )