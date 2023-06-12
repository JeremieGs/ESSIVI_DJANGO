# Generated by Django 4.1.4 on 2023-03-05 17:25

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_livreur', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('client_name', models.CharField(blank=True, max_length=50, null=True)),
                ('prix', models.FloatField(blank=True, null=True)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('nombre_article', models.IntegerField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en attente', 'en attente'), ('annulée', 'annulée'), ('livraison en cours', 'livraison en cours'), ('livrée', 'livrée')], default='en attente', max_length=250)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.client')),
            ],
        ),
        migrations.CreateModel(
            name='Entree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, error_messages={'unique': 'Un Fournisseur  avec ce nom existe deja dans la base , veuillez saisir un autre nom'}, max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'Un Fournisseur   avec cet email existe deja dans la base ,  veuillez saisir un autre email'}, max_length=254, unique=True)),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('ville', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Marque_eau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, error_messages={'unique': 'Une marque  avec ce nom existe deja dans la base , \n veuillez saisir un autre nom'}, max_length=150, unique=True)),
                ('libelle', models.TextField()),
                ('image', models.ImageField(upload_to='media')),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, error_messages={'unique': 'ce produit  existe deja dans la base , \n veuillez saisir un autre nom'}, max_length=150, unique=True)),
                ('image', models.ImageField(upload_to='media')),
                ('volume', models.FloatField()),
                ('nombre', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('poids', models.FloatField()),
                ('prix', models.FloatField()),
                ('conteneur', models.CharField(choices=[('bouteille', 'bouteille'), ('sachet', 'sachet'), ('canette', 'canette')], max_length=50)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('marque_eau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.marque_eau')),
            ],
        ),
        migrations.CreateModel(
            name='Livraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('client_name', models.CharField(blank=True, max_length=50, null=True)),
                ('utilisateur_name', models.CharField(blank=True, max_length=50, null=True)),
                ('prix', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en cours', 'en cours'), ('terminée', 'terminée')], default='en cours', max_length=50)),
                ('delai', models.DateTimeField(blank=True, null=True)),
                ('date_livr', models.DateField(blank=True, null=True)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.client')),
                ('commande', models.ForeignKey(error_messages={'unique': 'Une livraison  concernant cette commande existe deja '}, on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.commande', unique=True)),
                ('livreur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LigneEntree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('entree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.entree')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.produit')),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('prix', models.FloatField(blank=True, null=True)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('client_name', models.CharField(blank=True, max_length=50, null=True)),
                ('prix_com', models.FloatField(blank=True, null=True)),
                ('prix_livr', models.FloatField(blank=True, null=True)),
                ('prix_total', models.FloatField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('payée', 'payée'), ('nonpayée"', 'nonpayée')], default='nonpayée', max_length=50, null=True)),
                ('date_ajout', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.client')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.commande')),
                ('livraison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.livraison')),
            ],
        ),
        migrations.AddField(
            model_name='entree',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essivi_sarl.fournisseur'),
        ),
    ]
