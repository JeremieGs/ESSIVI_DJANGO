from django.shortcuts import render
from django.shortcuts import redirect
import requests
from essivi_sarl.models import Commande
from requests.structures import CaseInsensitiveDict
from django.views.decorators.csrf import csrf_exempt
def index(request):
    return render(request,'login.html')
def pagecommande(request):
    return render(request,'commande.html')
def pageproduit(request):
    return render(request,'produit.html')
def pageclient(request):
    return render(request,'client.html')
def pagelivreur(request):
    return render(request,'livreur.html')
def pagestock(request):
    return render(request,'stock.html')
def pagelivraison(request):
    return render(request,'livraison.html')
def pagestatistique(request):
    return render(request,'statistique.html')
def pagehome(request):
    return render(request,'home.html')
def detailscommandes(request):
    id =request.GET.get('id')
    context = {'id': id}
    return render(request,'detailscommande.html',context=context)
def detailsentrees(request):
    id =request.GET.get('id')
    context = {'id': id}
    return render(request,'detailsentree.html',context=context)
def detailsproduit(request):
    id =request.GET.get('id')
    context = {'id': id}
    return render(request,'detailproduit.html',context=context)
def facture(request):
    id =request.GET.get('id')
    context = {'id': id}
    return render(request,'index.html',context=context)