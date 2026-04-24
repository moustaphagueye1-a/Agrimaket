from django.urls import path
from .views import (index, detail, verifier, Confirmation,
                    inscription, connexion, deconnexion,
                    annuler_commande, mes_commandes)

urlpatterns = [
    path('',                              index,             name='home'),
    path('produit/<int:myid>/',           detail,            name='detail'),
    path('verifier/',                     verifier,          name='verifier'),
    path('confirmation/',                 Confirmation,      name='Confirmation'),
    path('inscription/',                  inscription,       name='inscription'),
    path('connexion/',                    connexion,         name='connexion'),
    path('deconnexion/',                  deconnexion,       name='deconnexion'),
    path('mes-commandes/',                mes_commandes,     name='mes_commandes'),
    path('annuler-commande/<str:commande_id>/', annuler_commande, name='annuler_commande'),
    
]