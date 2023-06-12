from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import AuthenticationFailed
from django.core import serializers
from .serializers import UtilisateurSerializer,ClientSerializer ,marqueSerializer ,produitSerializer,fournisseurSerializer,entreeSerializer,ligneentreeSerializer,commandeSerializer,lignecommandeSerializer,livraisonSerializer,factureSerializer
from .models import Utilisateur  ,Produit,Fournisseur,Entree,Commande,LigneCommande,Livraison,Marque_eau,LigneEntree,Facture,Client
import jwt ,datetime
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
import os
import json
from django.db.models import Sum
class ImageServeView(View):
    def get(self, request, *args, **kwargs):
        path = kwargs.get('path')
        fullpath = os.path.join(settings.MEDIA_ROOT, path)
        with open(fullpath, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
        return response
# Create your views here.
# enregistrement  livreur
class registerview(APIView):
    def post(self,request):
        serializer = UtilisateurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("enregistrement reussi")

# enregistrement  Client
class Clientregisterview(APIView):
    def post(self,request):       
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("succes : client enregistré")
#enregistrement marque
class enrmarqueview(APIView):
    def post(self , request):
        serializer = marqueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("marque "+str(request.data['name'])+" enregister avec succes")
#enregistrement produit
class enrproduitview(APIView):
    def post(self , request):
        serializer = produitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("produit "+str(request.data['name'])+" enregister avec succes")
#enregistrement fournisseur
class enrfournisseurview(APIView):
    def post(self , request):
        serializer = fournisseurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
#entree stock 
class entreeview(APIView):
    def post(self , request):
        serializer = entreeSerializer(data=request.data['entree'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        LastInsertId = (Entree.objects.last()).id
        serializer0=request.data['ligneentree']
        for serializerent in serializer0:
            data1={
                "produit":serializerent["produit"],
                "quantite":serializerent["quantite"],
                "entree":LastInsertId
            }
            serializer1 = ligneentreeSerializer(data=data1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
        return Response("succes enregistrement effectué")

#commande 
class commandeview(APIView):
    def post(self , request):
        serializer = commandeSerializer(data=request.data['commande'])
        serializer.is_valid(raise_exception=True)
        verification=request.data['lignecommande']
        for i in verification:
            quantite =Produit.objects.values_list('stock', flat=True).filter(id=i['produit'])
            produit =Produit.objects.values_list('name', flat=True).filter(id=i['produit'])
            if i['quantite'] > quantite[0]:
                return Response({"message":"la quantite restant ("+str(quantite[0])+") du produit "+str(produit[0])+ " ne suffit pas a honorer cette commande"})
            if i['quantite']==0 or not i['quantite']:
                return Response({"message":"le nombre ne peut pas etre nul"})
        serializer.save()
        LastInsertId = (Commande.objects.last()).id
        serializer0=request.data['lignecommande']
        id_client=request.data['commande']['client']
        cursor = connection.cursor()
        cursor.callproc("nom_client_commande",(LastInsertId,id_client))
        cursor.close()
        for serializerent in serializer0:
            data1={
                "produit":serializerent["produit"],
                "quantite":serializerent["quantite"],
                "commande":LastInsertId
            }
            serializer1 = lignecommandeSerializer(data=data1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            id_prod =serializerent['produit']
            LastInsertId2 = (LigneCommande.objects.last()).id
            cursor = connection.cursor()
            cursor.callproc("prix_ligne_commande",(id_prod,LastInsertId2))
            cursor.close()

        return Response({"message":"Commande enregister avec succes"})

class annulecommande(APIView):
    def post(self , request):
        id_com= str(request.data['id'])
        id_com =Commande.objects.values_list('id', flat=True).filter(id=id_com)
        cursor = connection.cursor()
        cursor.callproc("annulercommande",(id_com))
        cursor.close()
        return Response({"message":"succes"})

# livraison
class livraisonview(APIView):
    def post(self,request):
        serializer = livraisonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        id_livr=(Livraison.objects.last()).id
        distance = request.data['distance']
        com =Livraison.objects.values_list('commande', flat=True).filter(id=id_livr)
        client=Livraison.objects.values_list('client', flat=True).filter(id=id_livr)
        prix=Livraison.objects.values_list('prix', flat=True).filter(id=id_livr)
        nom_client=Livraison.objects.values_list('client_name', flat=True).filter(id=id_livr)
        id_client=request.data['client']
        cursor = connection.cursor()
        cursor.callproc("livraison",(distance,id_livr,com[0]))
        cursor.close()
        cursor = connection.cursor()
        cursor.callproc("nom_client_livraison",(id_livr,id_client))
        cursor.close()
        cursor = connection.cursor()
        cursor.callproc("facture",(id_livr,com[0],client[0],nom_client[0],prix[0]))
        cursor.close()
        return Response("livraison N"+str(id_livr)+"enregistrer avec succes")
# login livreur 
class loginview(APIView):
    def post(self ,request):
        username1 =request.data['username']
        password =request.data['password']

        user = Utilisateur.objects.filter(username=username1,is_livreur=1).first()
        if user is None :
            raise AuthenticationFailed("utilisatteur introuvable")
        if not user.check_password(password) :
            raise AuthenticationFailed('mot de passe incorrect')
        
        payload = {
            'id' :user.id ,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }
        
        token =jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
        
        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        
        response.data = {
            'jwt':token,
            'message':'Vous etes connecter',
        }
        return response
##############################################################################
class Utilisateur_livr_view(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        user = Utilisateur.objects.filter(id=payload['id']).first()
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)
#logout livreur
class admin_view(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        user = Utilisateur.objects.filter(id=payload['id']).first()
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)

class listecommandeview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed({"message":'vous n\'etes pas connecté'})
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"message":"connexion expirée , \n veuillez vous reconnecter"})


        commande= Commande.objects.all().order_by('-date_ajout')
        serializer = commandeSerializer(commande,many=True)
        return Response(serializer.data)
###
class listeclientview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed({"message":'vous n\'etes pas connecté'})
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"message":"connexion expirée , \n veuillez vous reconnecter"})


        commande= Client.objects.all().order_by('-date_joined')
        serializer = ClientSerializer(commande,many=True)
        return Response(serializer.data)
#liste livraison
class listelivraisonview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')
        token2 = request.COOKIES.get('jwt1')

        if not token and not token2:
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            if token :
                payload= jwt.decode(token,'secret', algorithm=['HS256'])
            elif token2 :
                payload2= jwt.decode(token2,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        commande= Livraison.objects.all().order_by('-date_ajout')
        serializer = livraisonSerializer(commande,many=True)
        return Response(serializer.data)

class listelivreurview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        commande= Utilisateur.objects.filter(is_livreur=1)
        serializer = UtilisateurSerializer(commande,many=True)
        return Response(serializer.data)

class listemarqueview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        commande= Marque_eau.objects.all()
        serializer = marqueSerializer(commande,many=True)
        return Response(serializer.data)
class listefournisseurview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        fournisseur= Fournisseur.objects.all()
        serializer = fournisseurSerializer(fournisseur,many=True)
        return Response(serializer.data)

class detailscommandeview(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        id =request.data['id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM detailscommandes WHERE commande_id = %s", [id])
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
#################################################################
class detailsduproduit(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        id =request.data['id']
        resultat = Produit.objects.filter(id=id)
        resultat= produitSerializer(resultat,many=True)
        return Response(resultat.data)

##############################################################
class listeentreeview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        list= Entree.objects.all().order_by('-id')
        serializer = entreeSerializer(list,many=True)
        return Response(serializer.data)
#####################################
class detailsentreeview(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        id =request.data['id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM detailsentree WHERE entree_id = %s", [id])
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class listproduitview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        produit= Produit.objects.all()
        serializer = produitSerializer(produit,many=True)
        return Response(serializer.data)
class listfacture(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        facture= Facture.objects.all().order_by('-date_ajout')
        serializer = factureSerializer(facture,many=True)
        return Response({'facture':serializer.data})
class facturedetails(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt1')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM essivi_sarl_facture WHERE commande_id = %s", [request.data['id']])
        resultat=cursor.fetchall()
        cursor.close()
        return Response(resultat)


class Logoutview(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data ={
            "message":"vous etes déconnecter"
        }
        return response

class adminlogoutview(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt1')
        response.data ={
            "message":"vous etes déconnecter"
        }
        return response


class adminloginview(APIView):
    def post(self ,request):
        username1 =request.data['username']
        password =request.data['password']

        user = Utilisateur.objects.filter(username=username1,is_admin=1).first()
        if user is None :
            raise AuthenticationFailed("utilisatteur introuvable")
        if not user.check_password(password) :
            raise AuthenticationFailed('mot de passe incorrect')
        
        payload = {
            'id' :user.id ,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat' : datetime.datetime.utcnow()
        }
        
        token1 =jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
        
        response = Response()

        response.set_cookie(key='jwt1',value=token1,httponly=True)
        
        response.data = {
            'jwt1':token1,
            'message':'Vous etes connecter',
        }
        return response

class livraisonterminer(APIView):
    def post(self ,request):
        id_livr=request.data['id']
        id_comm=request.data['commande']
        cursor = connection.cursor()
        cursor.callproc("livraisonterminer",(id_livr,id_comm))
        cursor.close()
        Livraison.objects.filter(id=id_livr).update(date_livr=timezone.now())
        return Response({"message":"la  livraison N"+id_livr+" a ete effectuer"})
class facturepaye(APIView):
    def post(self ,request):
        id_fac= (request.data['id'])
        id_fac =Facture.objects.values_list('id', flat=True).filter(id=id_fac)
        cursor = connection.cursor()
        cursor.callproc("facturepaye",id_fac)
        cursor.close()
        return Response({"message":"la  facture N "+str(id_fac)+" a ete payée"})
class nomlivreurlivraison(APIView):
    def post(self ,request):
        token = request.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        id_livr= (request.data['id_livr'])
        cursor = connection.cursor()
        cursor.callproc("nom_livreur_livraison",(id_livr,payload['id']))
        cursor.close()
        return Response({"message":"succes"})

class checkview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt1')
        if not token :
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            payload= jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        return Response("succes")

class listelivraisonenattenteview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')
        token2 = request.COOKIES.get('jwt1')

        if not token and not token2:
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            if token :
                payload= jwt.decode(token,'secret', algorithm=['HS256'])
            elif token2 :
                payload2= jwt.decode(token2,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        commande= Livraison.objects.filter(statut='en cours').order_by('-date_ajout')
        serializer = livraisonSerializer(commande,many=True)
        return Response(serializer.data)
class listehistoriqueview(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')
        token2 = request.COOKIES.get('jwt1')

        if not token and not token2:
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            if token :
                payload= jwt.decode(token,'secret', algorithm=['HS256'])
            elif token2 :
                payload2= jwt.decode(token2,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")


        commande= Livraison.objects.filter(livreur=payload['id']).order_by('-date_livr')
        serializer = livraisonSerializer(commande,many=True)
        return Response(serializer.data)


class modifierlivreurview(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt')
        token2 = request.COOKIES.get('jwt1')

        if not token and not token2:
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            if token :
                payload= jwt.decode(token,'secret', algorithm=['HS256'])
            elif token2 :
                payload2= jwt.decode(token2,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        nom =request.data['nom']
        prenom = request.data['prenom']
        email = request.data['email']
        username = request.data['username']

        Utilisateur.objects.filter(id=payload['id']).update(first_name=prenom,last_name =nom,email=email,username=username)
        return Response("succes")

###
class modifierproduit(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt')
        token2 = request.COOKIES.get('jwt1')

        if not token and not token2:
            raise AuthenticationFailed('vous n\'etes pas connecté')
        try:
            if token :
                payload= jwt.decode(token,'secret', algorithm=['HS256'])
            elif token2 :
                payload2= jwt.decode(token2,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("connexion expirée , \n veuillez vous reconnecter")
        serializer = produitSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        produit = Produit.objects.get(id=request.data['id'])
        serializer.update(produit, serializer.validated_data)
        return Response("succes")
class tartview(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM commande_nombre ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class venteproduit(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produit_vendu ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)

class lastcommande(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM last_commande ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class lastlivraison(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM last_livraison ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class livreuracte(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM livreur_livraison ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class chiffreaffairesemaine(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM chiffre_affaire_semaine ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class conteneur(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM conteneur ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class client(APIView):
    def get(self , request):
        cursor = connection.cursor()
        cursor.execute("SELECT * from client ")
        resultat = cursor.fetchall()
        cursor.close()
        return Response(resultat)
class home(APIView):
    def get(self , request):
        com = Commande.objects.all().count()
        total_prix =Commande.objects.aggregate(total_prix=Sum('prix'))['total_prix']
        comat =Commande.objects.filter(statut='en attente').count()
        livat =Livraison.objects.filter(statut='en cours').count()
        resultat ={
            'com':com,
            'total':total_prix,
            'comat':comat,
            'livat':livat
        }
        return Response(resultat)