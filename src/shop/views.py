from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.


def shop(request):
    """Vue des produits"""
    context = {}
    # return HttpRequest('I\'m testing')
    return render(request, 'shop/index.html', context)
