import django.utils.timezone
from django.db import models
from django.contrib.auth.models import AbstractUser ,AbstractBaseUser
# Create your models here.
class Utilisateur(AbstractUser):
    Nom : models.CharField(max_length=255)
    Prenom : models.CharField(max_length=255)
    username : None
    password : models.CharField( max_length=255) 
    email : models.CharField(max_length=255 , unique=True)
    ville : models.CharField(max_length=225)
    adresse :models.CharField(max_length=255)
    date_de_nais :models.DateField()
    is_admin =models.BooleanField(default=False)
    is_livreur =models.BooleanField(default=False)
    is_deleted =models.BooleanField(default=False)
    REQUIRED_FIELDS=[]

class Client(AbstractBaseUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    email = models.EmailField(blank=True, max_length=254 ,unique=True)
    date_joined= models.DateTimeField(default=django.utils.timezone.now)
    is_deleted =models.BooleanField(default=False)
    REQUIRED_FIELDS=['first_name','last_name']    

class Marque_eau(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(blank=True, max_length=150 ,unique=True ,error_messages={'unique': 'Une marque  avec ce nom existe deja dans la base , \n veuillez saisir un autre nom'} )
    libelle = models.TextField()
    image = models.ImageField(upload_to='media')
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)
    is_deleted =models.BooleanField(default=False)
    REQUIRED_FIELDS=['name']    

class Produit(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(blank=True, max_length=150 ,unique=True ,error_messages={'unique': 'ce produit  existe deja dans la base , \n veuillez saisir un autre nom'} )
    marque_eau = models.ForeignKey(Marque_eau, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    volume = models.FloatField()
    nombre = models.IntegerField()
    stock = models.IntegerField()
    poids = models.FloatField()
    prix = models.FloatField()
    CHOICES = (
        ('bouteille', 'bouteille'),
        ('sachet', 'sachet'),
        ('canette', 'canette'),
    )
    conteneur= models.CharField( max_length=50,choices=CHOICES)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)
    is_deleted =models.BooleanField(default=False)
    REQUIRED_FIELDS=['name','volume','nombre','poids','conteneur','marque_eau']    


class Fournisseur(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField( blank=True, max_length=150 ,unique=True ,error_messages={'unique': 'Un Fournisseur  avec ce nom existe deja dans la base , veuillez saisir un autre nom'})
    email = models.EmailField(blank=True, max_length=254 ,unique=True , error_messages={'unique': 'Un Fournisseur   avec cet email existe deja dans la base ,  veuillez saisir un autre email'})
    telephone = models.IntegerField(null=True,blank=True)
    ville =models.CharField(max_length=50 ,null=True,blank=True)
    pays =models.CharField(max_length=50 ,null=True,blank=True)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)
    is_deleted =models.BooleanField(default=False)
    REQUIRED_FIELDS=['name','email']

class Entree(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    fournisseur = models.ForeignKey(Fournisseur ,on_delete=models.CASCADE)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)
    REQUIRED_FIELDS=['fournisseur']
class LigneEntree(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    entree = models.ForeignKey(Entree ,on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit ,on_delete=models.CASCADE)
    quantite = models.IntegerField()
    REQUIRED_FIELDS=['name','telephone','email','produit']

class Commande(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    client =models.ForeignKey(Client ,on_delete=models.CASCADE , )
    client_name =models.CharField(null=True,blank=True, max_length=50)
    prix =models.FloatField( blank=True,null=True)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)
    poids =models.FloatField( blank=True,null=True)
    nombre_article =models.IntegerField( null=True , blank=True)
    CHOICES = (
        ('en attente', 'en attente'),
        ('annulée', 'annulée'),
        ('livraison en cours', 'livraison en cours'),
        ('livrée', 'livrée'),
    )
    statut =models.CharField(null=False,blank=False,choices=CHOICES ,default='en attente',max_length=250)
    REQUIRED_FIELDS=['client','statut']

class LigneCommande(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    commande =models.ForeignKey(Commande,on_delete=models.CASCADE)
    produit =models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite =models.IntegerField( )
    prix = models.FloatField( blank=True ,null=True)
    REQUIRED_FIELDS=['produit','quantite']
class Livraison(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE,unique=True ,error_messages={'unique': 'Une livraison  concernant cette commande existe deja '})
    client =models.ForeignKey(Client, on_delete=models.CASCADE)
    client_name =models.CharField(null=True,blank=True, max_length=50)
    livreur =models.ForeignKey(Utilisateur, on_delete=models.CASCADE ,null=True ,blank=True)
    livreur_name =models.CharField(null=True,blank=True, max_length=50)
    prix =models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    long =models.FloatField(null=True,blank=True)
    distance =models.FloatField(null=True,blank=True)
    CHOICES = (
        ('en cours', 'en cours'),
        ('terminée', 'terminée'),
    )
    statut = models.CharField( choices=CHOICES, default='en cours', max_length=50)
    delai =models.DateTimeField( auto_now=False, auto_now_add=False, null=True,blank=True,)
    date_livr =models.DateField( auto_now=False, auto_now_add=False ,null=True,blank=True)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now)

class Facture(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    commande = models.ForeignKey(Commande,on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_name =models.CharField(null=True,blank=True, max_length=50)
    livraison =models.ForeignKey(Livraison, on_delete=models.CASCADE)
    prix_com = models.FloatField(null=True,blank=True)
    prix_livr = models.FloatField(null=True,blank=True)
    prix_total =models.FloatField(null=True,blank=True)
    CHOICES = (
        ('payée', 'payée'),
        ('nonpayée"', 'nonpayée'),
    )
    statut = models.CharField( choices=CHOICES, default='nonpayée', max_length=50 ,null=True)
    date_ajout= models.DateTimeField(default=django.utils.timezone.now )
