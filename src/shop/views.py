from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render

from .models import *

# Pour recevoir les données en json
from django.http import JsonResponse
# Pour charger les données en json
import json
# Pour vérifier si l'utilisateur est connecté
from django.contrib.auth.decorators import login_required


# Create your views here.


def shop(request, *args, **kwargs):
    """Vue des produits"""
    # On récupère l'ensemble des produits
    produits = Produit.objects.all()

    # Vérification de la connectivité de l'utilisateur et récupérateur des informations sur le panier
    if request.user.is_authenticated:

        # On récupère les informations du client connecté
        client = request.user.client

        # On vérifie si le client connecté a une commande en cours et qu'elle n'est pas complete
        # sinon on crée une commande.

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        # On récupère le nombre d'articles du panier
        nombre_article = commande.get_panier_articles

    else:
        # Si l'utilisateur n'est pas connecté, on réinitialise son panier à 0.
        articles = []
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0,
        }
        nombre_article = commande['get_panier_article']

    context = {
        'produits': produits,
        'nombre_article': nombre_article,
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    # Vérification de la connectivité de l'utilisateur et récupérateur des informations sur le panier
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        # On récupère tous les articles commandés par le client
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_articles
    else:
        articles = []
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0,
        }
        nombre_article = commande['get_panier_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article,
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_articles

    else:
        articles = []
        commande = {
            'get_panier_total': 0,
            'get_panier_article': 0,
        }
        nombre_article = commande['get_panier_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article,
    }

    return render(request, 'shop/commande.html', context)


# On spécifie qu'il faut être connecté pour avoir accès à cette vue @login_required()
@login_required()
def update_article(request, *args, **kwargs):
    # On récupère les données transmises avec le JavaScript
    data = json.loads(request.body)

    # On récupère l'id du produit
    produit_id = data['produit_id']

    # On récupère l'action enclenchée par le bouton
    action = data['action']

    # On récupère le client connecté
    client = request.user.client

    # On récupère le produit correspondant à l'id récupéré
    produit = Produit.objects.get(id=produit_id)

    # On récupère la commande si elle existe déjà ou on la crée si elle n'existe pas
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    # On effectue des opérations en fonction de l'action
    if action == "add":
        commande_article.quantite += 1

    if action == "remove":
        commande_article.quantite -= 1

    commande_article.save()

    if commande_article.quantite <= 0:
        commande_article.delete()

    return JsonResponse({'panier modifier': 'yes'}, safe=False)


def traitement_commande(request, *args, **kwargs):
    data = json.loads(request.body)
    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)

        print(f"Le total est : {data['form']['total']}")
        print(type(data['form']['total']))
        my_str = '24.77,00'
        my_float = float(my_str.split(',')[0])
        print(my_float)
        total = float(data['form']['total'].split(",")[0])
        commande.transaction_id = transaction_id
        if commande.get_panier_total == total:
            commande.complete = True
            commande.save()

        if commande.produit_physique:
            AddressChipping.objects.create(
                client=client,
                commande=commande,
                addresse=data['shipping']['address'],
                ville=data['shipping']['city'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        print('utilisateur non connecté')

    return JsonResponse('Traitement complet', safe=False)
