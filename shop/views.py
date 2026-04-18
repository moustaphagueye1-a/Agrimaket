import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404

from db.mongo import get_produits, get_commandes
from db.queries import decrementer_stock
from .models import Commande, Produit  # ← import des modèles Django


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de mapping Django → MongoDB
# ─────────────────────────────────────────────────────────────────────────────

class CategorieMongo:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name


class ImageMock:
    """
    Priorité 1 : image venant du modèle Django (uploadée via l'admin).
    Priorité 2 : chemin stocké dans MongoDB.
    Priorité 3 : vide → le template affichera le placeholder SVG.
    """
    def __init__(self, django_image_field=None, mongo_path=''):
        # Si le champ Django existe et a une image uploadée
        if django_image_field and bool(django_image_field):
            self._url  = django_image_field.url
            self._bool = True
        # Sinon, chemin MongoDB
        elif mongo_path:
            self._url  = f'/media/{mongo_path}'
            self._bool = True
        else:
            self._url  = ''
            self._bool = False

    def __bool__(self):
        return self._bool

    @property
    def url(self):
        return self._url

    def __str__(self):
        return self._url


# Dans shop/views.py — remplacer uniquement la classe ProduitMongo

class ProduitMongo:
    """
    Fusionne un document MongoDB avec le modèle Django via l'id.
    L'id Django == le champ 'id' dans MongoDB (clé de jointure fiable).
    """
    _django_cache = {}

    @classmethod
    def _get_django_produit(cls, produit_id):
        if produit_id not in cls._django_cache:
            try:
                cls._django_cache[produit_id] = Produit.objects.get(id=produit_id)
            except Produit.DoesNotExist:
                cls._django_cache[produit_id] = None
        return cls._django_cache[produit_id]

    def __init__(self, doc):
        self.id          = doc.get('id', 0)
        self._mongo_id   = str(doc['_id'])
        self.nom         = doc.get('nom', '')
        self.prix        = doc.get('prix', 0)
        self.description = doc.get('description', '')
        self.stock       = doc.get('stock', 0)
        self.producteur  = doc.get('producteur', '')
        self.attributs   = doc.get('attributs', {})
        self.categorie   = CategorieMongo(doc.get('categorie', ''))

        # ── Jointure par ID (fiable) ──────────────────────────────────────
        django_produit = self._get_django_produit(self.id)  # ← par id, pas par nom
        django_image   = django_produit.image if django_produit else None
        self.image     = ImageMock(
            django_image_field=django_image,
            mongo_path=doc.get('image', '')
        )

    def __str__(self):
        return self.nom


# ─────────────────────────────────────────────────────────────────────────────
# Vues
# ─────────────────────────────────────────────────────────────────────────────

def index(request):
    # Vider le cache à chaque chargement pour prendre en compte les
    # nouvelles images ajoutées dans l'admin
    ProduitMongo._django_cache.clear()

    query     = {}
    item_name = request.GET.get('item-name', '')
    if item_name:
        query['nom'] = {'$regex': item_name, '$options': 'i'}

    produits_docs = list(get_produits().find(query).sort('id', 1))
    produits_list = [ProduitMongo(p) for p in produits_docs]

    paginator = Paginator(produits_list, 4)
    produits  = paginator.get_page(request.GET.get('page'))

    return render(request, 'shop/index.html', {
        'produits':  produits,
        'item_name': item_name,
    })


def detail(request, myid):
    ProduitMongo._django_cache.clear()

    doc = get_produits().find_one({'id': myid})
    if doc is None:
        raise Http404("Produit introuvable")

    return render(request, 'shop/detail.html', {
        'produit': ProduitMongo(doc)
    })


def verifier(request):
    if request.method == "POST":
        items_raw = request.POST.get('items', '[]')
        total_str = request.POST.get('total', '0')
        nom       = request.POST.get('nom', '')
        email     = request.POST.get('email', '')
        telephone = request.POST.get('telephone', '')
        region    = request.POST.get('region', '')
        commune   = request.POST.get('commune', '')
        adresse   = request.POST.get('adresse', '')

        # ── Parser le panier JSON ─────────────────────────────────────────
        try:
            items = json.loads(items_raw)
        except (json.JSONDecodeError, TypeError):
            items = []

        # ── Construire les articles + décrémenter le stock ────────────────
        articles      = []
        total_calcule = 0

        for item in items:
            produit_id  = int(item.get('id', 0))
            quantite    = int(item.get('quantite', 1))
            prix        = float(item.get('prix', 0))
            doc_produit = get_produits().find_one({'id': produit_id})
            categorie   = doc_produit['categorie'] if doc_produit else ''

            articles.append({
                'produit_id':    produit_id,
                'nom':           item.get('nom', ''),
                'categorie':     categorie,
                'quantite':      quantite,
                'prix_unitaire': prix,
            })
            total_calcule += prix * quantite
            decrementer_stock(produit_id, quantite)

        total_final = total_calcule or float(
            total_str.replace(' FCFA', '').replace(',', '') or 0
        )

        # ── 1. Enregistrement dans MongoDB ───────────────────────────────
        commande_mongo = {
            'client': {
                'nom':       nom,
                'email':     email,
                'telephone': telephone,
                'region':    region,
                'commune':   commune,
                'adresse':   adresse,
            },
            'date':      datetime.utcnow(),
            'articles':  articles,
            'statut':    'confirmée',
            'total':     total_final,
            'items_raw': items_raw,
            'total_raw': total_str,
        }
        get_commandes().insert_one(commande_mongo)

        # ── 2. Enregistrement dans Django admin (SQLite) ──────────────────
        #    On reconstruit le résumé lisible des articles pour le champ
        #    items (TextField) du modèle Django Commande
        resume_items = json.dumps([
            {
                'produit': a['nom'],
                'quantite': a['quantite'],
                'prix_unitaire': a['prix_unitaire'],
                'sous_total': a['quantite'] * a['prix_unitaire'],
            }
            for a in articles
        ], ensure_ascii=False)

        Commande.objects.create(
            items     = resume_items,
            total     = f"{total_final:.0f} FCFA",
            nom       = nom,
            email     = email,
            telephone = telephone,
            region    = region,
            commune   = commune,
            adresse   = adresse,
        )

        # ── Session pour la page de confirmation ──────────────────────────
        request.session['client_nom'] = nom
        return redirect('Confirmation')

    return render(request, 'shop/verifier.html')


def Confirmation(request):
    nom = request.session.get('client_nom', 'Client')
    return render(request, 'shop/confirmation.html', {'nom': nom})