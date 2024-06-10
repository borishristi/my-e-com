from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render

from .models import *

# Pour recevoir les données en json
from django.http import JsonResponse
# Pour charger les données en json
import json

from .utiles import panier_cookie, data_cookie

# Pour vérifier si l'utilisateur est connecté
from django.contrib.auth.decorators import login_required


# Create your views here.


def shop(request, *args, **kwargs):
    """Vue des produits"""
    # On récupère l'ensemble des produits
    produits = Produit.objects.all()

    # Vérification de la connectivité de l'utilisateur et récupérateur des informations sur le panier
    # if request.user.is_authenticated:
    #
    #     # On récupère les informations du client connecté
    #     client = request.user.client
    #
    #     # On vérifie si le client connecté a une commande en cours et qu'elle n'est pas complete
    #     # sinon on crée une commande.
    #
    #     commande, created = Commande.objects.get_or_create(client=client, complete=False)
    #
    #     # On récupère le nombre d'articles du panier
    #     nombre_article = commande.get_panier_articles
    #
    # else:
    #     # Si l'utilisateur n'est pas connecté, on réinitialise son panier à 0.
    #     cookie_panier = panier_cookie(request)
    #     articles = cookie_panier['articles']
    #     commande = cookie_panier['commande']
    #     nombre_article = cookie_panier['nombre_article']

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'produits': produits,
        'nombre_article': nombre_article,
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    # Vérification de la connectivité de l'utilisateur et récupérateur des informations sur le panier
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article,
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

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


def commandeAnonyme(request, data):
    name = data['form']['name']
    print('data', data)
    print('name', name)
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']

    cookie_panier = panier_cookie(request)

    articles = cookie_panier['articles']

    client, created = Client.objects.get_or_create(
        email=email
    )

    client.name = name
    client.save()

    commande = Commande.objects.create(
        client=client
    )

    for article in articles:
        produit = Produit.objects.get(id=article['produit']['pk'])

        CommandeArticle.objects.create(
            produit=produit,
            commande=commande,
            quantite=article['quantite']
        )

    return client, commande


def traitement_commande(request, *args, **kwargs):

    STATUS_TRANSACTION = ["ACCEPTED", 'COMPLETED', 'SUCCESS']

    data = json.loads(request.body)
    # transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:
        print('*' * 50)
        print(f"Le client est bien authentifié")
        client = request.user.client
        commande, created = Commande.objects.get_or_create(client=client, complete=False)
        print(f"le client est : {client}")

    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'].split(",")[0])
    commande.transaction_id = data['paymentInfo']['transaction_id']
    commande.total_trans = float(data['paymentInfo']['total'].split(",")[0])

    print(data)
    print(f"le total de notre transaction reçu au niveau du traitement de la commande est : {total}")

    if commande.get_panier_total == total:
        commande.complete = True
        commande.status = data['paymentInfo']['status']

    else:
        commande.status = 'REFUSED'
        commande.save()
        return JsonResponse("Attention Traitement refusé Fraude détecté", safe=False)

    print(f"On avons dépassé la vérification du prix et le statut est {commande.status}")
    commande.save()

    if commande.produit_physique:
        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse=data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )

    if not commande.status in STATUS_TRANSACTION:
        return JsonResponse("Désolé, le paiement a échoué, veuillez réessayer.")

    return JsonResponse('Commande effectué avec success. Vous serez livré dans un delai de 72h.', safe=False)
