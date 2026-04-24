from db.mongo import get_produits

PRODUITS = [
    {
        "id": 1,
        "nom": "Mangues de Casamance",
        "categorie": "Fruits",
        "prix": 1500,
        "stock": 80,
        "producteur": "Coopérative Agricole de Ziguinchor",
        "description": "Mangues Kent fraîches cultivées en Casamance, sucrées et juteuses.",
        "image": "c:\Users\Admin\OneDrive\Images\imagemangue.jpeg",
        "attributs": {"bio": True, "variete": "Kent", "poids_kg": 1}
    },
    {
        "id": 2,
        "nom": "Bissap séché",
        "categorie": "Épices & Condiments",
        "prix": 800,
        "stock": 60,
        "producteur": "Groupement Féminin de Kaolack",
        "description": "Fleurs d'hibiscus séchées pour jus et infusions, récolte locale.",
        "image": "",
        "attributs": {"bio": True, "conditionnement": "sachet 200g"}
    },
    {
        "id": 3,
        "nom": "Arachides grillées",
        "categorie": "Légumineuses",
        "prix": 500,
        "stock": 120,
        "producteur": "Ferme Diallo – Thiès",
        "description": "Arachides grillées artisanalement, sans additifs, du bassin arachidier.",
        "image": "",
        "attributs": {"bio": False, "poids_g": 500, "sale": False}
    },
    {
        "id": 4,
        "nom": "Huile d'arachide artisanale",
        "categorie": "Huiles",
        "prix": 2500,
        "stock": 45,
        "producteur": "Coopérative de Diourbel",
        "description": "Huile pressée à froid, 100% naturelle, idéale pour le thiéboudienne.",
        "image": "",
        "attributs": {"volume_ml": 1000, "pression": "froide", "bio": False}
    },
    {
        "id": 5,
        "nom": "Miel de Kédougou",
        "categorie": "Miel",
        "prix": 5000,
        "stock": 25,
        "producteur": "Apiculteurs de Kédougou",
        "description": "Miel sauvage récolté dans les forêts de Kédougou, pur et non traité.",
        "image": "",
        "attributs": {"poids_g": 500, "type": "sauvage", "cristallise": False}
    },
    {
        "id": 6,
        "nom": "Fromage Peul – Wagasi",
        "categorie": "Fromages",
        "prix": 2000,
        "stock": 15,
        "producteur": "Éleveurs Peuls – Kolda",
        "description": "Fromage frais traditionnel à base de lait de vache, spécialité peule.",
        "image": "",
        "attributs": {"lait": "vache", "affinage": "frais", "bio": True}
    },
    {
        "id": 7,
        "nom": "Mil Souna local",
        "categorie": "Céréales",
        "prix": 600,
        "stock": 200,
        "producteur": "Coopérative de Louga",
        "description": "Mil souna cultivé localement, base du couscous et du thiakry.",
        "image": "",
        "attributs": {"bio": False, "poids_kg": 1, "moulu": False}
    },
    {
        "id": 8,
        "nom": "Tamarin sucré",
        "categorie": "Fruits",
        "prix": 700,
        "stock": 50,
        "producteur": "Verger Sène – Fatick",
        "description": "Tamarin mûr et sucré, parfait pour le bouye ou en collation.",
        "image": "",
        "attributs": {"bio": True, "poids_g": 300}
    },
    {
        "id": 9,
        "nom": "Poudre de Moringa",
        "categorie": "Épices & Condiments",
        "prix": 3000,
        "stock": 35,
        "producteur": "Groupement Féminin de Saint-Louis",
        "description": "Feuilles de moringa séchées et moulues, riche en nutriments.",
        "image": "",
        "attributs": {"bio": True, "poids_g": 200, "usage": "alimentaire"}
    },
    {
        "id": 10,
        "nom": "Gombo séché",
        "categorie": "Légumes",
        "prix": 900,
        "stock": 4,  # rupture de stock
        "producteur": "Maraîchers de Dagana",
        "description": "Gombo séché au soleil, pour soupe kandia et sauces locales.",
        "image": "",
        "attributs": {"bio": False, "poids_g": 250}
    },
    {
        "id": 11,
        "nom": "Pain de Singe – Baobab",
        "categorie": "Fruits",
        "prix": 1200,
        "stock": 40,
        "producteur": "Coopérative de Thiès",
        "description": "Pulpe séchée de fruit de baobab, riche en vitamine C.",
        "image": "",
        "attributs": {"bio": True, "poids_g": 300, "forme": "pulpe séchée"}
    },
    {
        "id": 12,
        "nom": "Ditax (Detarium senegalense)",
        "categorie": "Fruits",
        "prix": 800,
        "stock": 30,
        "producteur": "Verger Badji – Ziguinchor",
        "description": "Fruit traditionnel du Sénégal, saveur acidulée, riche en fer.",
        "image": "",
        "attributs": {"bio": True, "saisonnier": True}
    },
    {
        "id": 13,
        "nom": "Poisson séché – Kétiakh",
        "categorie": "Poissons séchés",
        "prix": 4000,
        "stock": 20,
        "producteur": "Pêcheurs de Mbour",
        "description": "Poisson fermenté et séché, indispensable pour le thiéboudienne.",
        "image": "",
        "attributs": {"type_poisson": "sardinelle", "conservation": "sec", "poids_g": 500}
    },
    {
        "id": 14,
        "nom": "Thiof fumé",
        "categorie": "Poissons séchés",
        "prix": 6000,
        "stock": 3,  # rupture de stock
        "producteur": "Pêcheurs de Saint-Louis",
        "description": "Mérou fumé artisanalement, le roi des poissons sénégalais.",
        "image": "",
        "attributs": {"type_poisson": "mérou", "fumage": "artisanal", "poids_g": 400}
    },
    {
        "id": 15,
        "nom": "Piment local séché",
        "categorie": "Épices & Condiments",
        "prix": 600,
        "stock": 70,
        "producteur": "Maraîchers de Casamance",
        "description": "Piment rouge séché fort, indispensable dans la cuisine sénégalaise.",
        "image": "",
        "attributs": {"bio": False, "force": "fort", "poids_g": 100}
    },
]

def seed():
    col = get_produits()
    if col.count_documents({}) == 0:
        col.insert_many(PRODUITS)
        print(f" {len(PRODUITS)} produits sénégalais insérés dans MongoDB")
    else:
        print(f"ℹ  Collection produits déjà peuplée ({col.count_documents({})} produits)")

if __name__ == "__main__":
    seed()