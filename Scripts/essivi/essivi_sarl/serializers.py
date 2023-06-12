from rest_framework import serializers
from .models import Utilisateur  ,Client ,Marque_eau , Produit ,Fournisseur ,Entree ,LigneEntree,Commande,LigneCommande,Livraison,Facture

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur 
        fields ='__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }

        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance



        
    '''def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance'''

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =['id','first_name','last_name','email','date_joined']
        extra_kwargs={
            'password':{'write_only':True}
        }

        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

class marqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque_eau
        fields ='__all__'

class produitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields ='__all__'
    def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.marque_eau = validated_data.get('marque_eau', instance.marque_eau)
            instance.image = validated_data.get('image', instance.image)
            instance.volume = validated_data.get('volume', instance.volume)
            instance.nombre = validated_data.get('nombre', instance.nombre)
            instance.poids = validated_data.get('poids', instance.poids)
            instance.prix = validated_data.get('prix', instance.prix)
            instance.save()
            return instance

class fournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields ='__all__'
class entreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entree
        fields ='__all__'
class ligneentreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneEntree
        fields ='__all__'
    
class commandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields ='__all__'

class lignecommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneCommande
        fields ='__all__'

class livraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields ='__all__'

class factureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields ='__all__'

