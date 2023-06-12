from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .templateview import *
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns =[
    # enregistrement livreur
    path('livreurregister',registerview.as_view()),
    #enregistrement admin
    #enregistrement client
    path('clientregister',Clientregisterview.as_view()),
    #enregistrement marque
    path('marqueregister',enrmarqueview.as_view()),
    #login livreur
    path('login',loginview.as_view()),
    #
    path('adminlogin',adminloginview.as_view()),
    #
    path('adminlogout',adminlogoutview.as_view()),
    path('userview',Utilisateur_livr_view.as_view()),
    path('adminview',admin_view.as_view()),
    #
    path('enrproduit',enrproduitview.as_view()),
    #
    path('entreestock',entreeview.as_view()),
    #
    path('commande',commandeview.as_view()),
    #
    path('livraison',livraisonview.as_view()),
    #
    path('listcommande',listecommandeview.as_view()),
    #
    path('listlivraison',listelivraisonview.as_view()),
    #
    path('listlivreur',listelivreurview.as_view()),
    #
    path('listfournisseur',listefournisseurview.as_view()),
    #
    path('listmarque',listemarqueview.as_view()),
    #
    path('detailscommande',detailscommandeview.as_view()),
    #
    path('detailsentree',detailsentreeview.as_view()),
    #
    path('listentree',listeentreeview.as_view()),
    #
    path('listproduit',listproduitview.as_view()),
    #
    path('listfacture',listfacture.as_view()),
    #
    path('facture',facturedetails.as_view()),
    #
    path('enrfournisseur',enrfournisseurview.as_view()),
    #
    path('logout',Logoutview.as_view()),
    #annuler commande
    path('annuler',annulecommande.as_view()),
    path('modifierproduit',modifierproduit.as_view()),
    path('detailsproduits',detailsduproduit.as_view()),
    path('detailproduit',detailsproduit),
    #
    path('nom_livreur',nomlivreurlivraison.as_view()),
    #
    path('tartview',tartview.as_view()),
    path('venteproduit',venteproduit.as_view()),
    path('lastcommande',lastcommande.as_view()),
    path('home',home.as_view()),
    #
    path('livraisonterminer',livraisonterminer.as_view()),
    path('lastlivraison',lastlivraison.as_view()),
    path('livreuracte',livreuracte.as_view()),
    path('chiffreaffairesemaine',chiffreaffairesemaine.as_view()),
    path('conteneur',conteneur.as_view()),
    path('client',client.as_view()),
    #
    path('facturepaye', facturepaye.as_view()),
    path('listeclient', listeclientview.as_view()),
    path('livraisonenattente', listelivraisonenattenteview.as_view()),
    path('listhistorique', listehistoriqueview.as_view()),
    path('modifierlivreur', modifierlivreurview.as_view()),
    #
    path('check', checkview.as_view()),
    path('', index,name='login'),
    path('pagecommande', pagecommande,name='commandepage',),
    #
    path('pageproduit', pageproduit,name='produitpage',),
    path(r'^images/(?P<path>.*)$', ImageServeView.as_view(), name='image-serve'),
    path('pageclient', pageclient,name='clientpage',),
    path('pagelivreur', pagelivreur,name='livreurpage',),
    path('pagestock', pagestock,name='stockpage',),
    path('pagelivraison', pagelivraison,name='livraisonpage',),
    path('detailscommandes', detailscommandes,name='detailscommandes',),
    path('pagedetailsentree', detailsentrees,name='detailsentree',),
    path('pagestatistique', pagestatistique,name='detailscommandes',),
    path('pagehome', pagehome,name='homepage',),
    path('pagefacture', facture,name='facture',),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]