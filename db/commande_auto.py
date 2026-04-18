import time
import random
from datetime import datetime
from db.mongo import get_produits, get_commandes
from db.queries import decrementer_stock

CLIENTS_TEST = [
    {"nom": "Moussa Diallo",  "email": "moussa@email.sn",  "telephone": "771234567", "region": "Dakar",    "commune": "Plateau",    "adresse": "Rue 10 angle 15"},
    {"nom": "Fatou Ndiaye",   "email": "fatou@email.sn",   "telephone": "782345678", "region": "Thiès",    "commune": "Thiès Nord", "adresse": "Cité Millionnaire"},
    {"nom": "Aminata Sow",    "email": "aminata@email.sn", "telephone": "763456789", "region": "Saint-Louis","commune": "Sor",      "adresse": "Quartier Léona"},
    {"nom": "Ibrahima Fall",  "email": "ibrahima@email.sn","telephone": "774567890", "region": "Ziguinchor","commune": "Ziguinchor","adresse": "Boucotte"},
    {"nom": "Rokhaya Diop",   "email": "rokhaya@email.sn", "telephone": "785678901", "region": "Kaolack",  "commune": "Kaolack",   "adresse": "Médina Baye"},
]

def creer_commande_aleatoire():
    produits = list(get_produits().find({"stock": {"$gt": 0}}))
    if not produits:
        print("⚠️  Aucun produit disponible en stock")
        return

    produit  = random.choice(produits)
    quantite = random.randint(1, 3)
    client   = random.choice(CLIENTS_TEST)
    total    = produit["prix"] * quantite

    commande = {
        "client": client,
        "date": datetime.utcnow(),
        "articles": [{
            "produit_id":   produit["id"],
            "nom":          produit["nom"],
            "categorie":    produit["categorie"],
            "quantite":     quantite,
            "prix_unitaire": produit["prix"],
        }],
        "statut": "confirmée",
        "total": total
    }

    get_commandes().insert_one(commande)
    decrementer_stock(produit["id"], quantite)

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] 🛒  "
        f"{quantite}x {produit['nom']} — {client['nom']} — "
        f"{total:,} FCFA"
    )

def lancer_simulation():
    print("🚀 Simulation démarrée : 1 commande automatique par minute")
    while True:
        creer_commande_aleatoire()
        time.sleep(60)