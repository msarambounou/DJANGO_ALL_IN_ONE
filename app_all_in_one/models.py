from django.db import models

class User_additional(models.Model):
    #genre = models.CharField(max_length=2, null=True, default=None)
    email = models.EmailField(null=False, default=None)
    path_profil = models.CharField(max_length=255, null=True, default=None)
    job = models.CharField(max_length=255, null=True, default=None)
    job_description = models.CharField(max_length=255, null=True, default=None)
    folder_path = models.CharField(max_length=255, null=False, default=None)

class UserConfirmation(models.Model):
    email = models.EmailField(null=False, default=None)
    code_confirmation = models.TextField(max_length=8)

class All_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)

class Entreprise_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)
    id_user = models.IntegerField(null=False, default=None)
    link = models.CharField(max_length=80, null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    phone_number = models.BigIntegerField(null=True, default=None)
    indicateur = models.CharField(max_length=10, default=None)

class Business_card_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)
    id_user = models.IntegerField(null=False, default=None)
    link = models.CharField(max_length=80, null=False, default=None)
    indicateur = models.CharField(max_length=10, default=None)
    phone_number = models.BigIntegerField(null=True, default=None)


class Telephonie(models.Model):
    country = models.CharField(max_length=25)
    indicateur = models.CharField(max_length=10)
    nb_chiffres = models.IntegerField(null=False, default=None)

class Secteur(models.Model):
    libelle_secteur = models.CharField(max_length=25)

class Entreprise(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    secteur = models.CharField(max_length=25)
    nom_entreprise = models.CharField(max_length=40)
    statut = models.IntegerField(null=False, default=None)

class User_qrcode(models.Model):
    name = models.CharField(max_length=25, null=False, default=None)
    path = models.CharField(max_length=255, null=False, default=None)
    modele = models.CharField(max_length=255, null=False, default=None)
    flag_plaque = models.IntegerField(null=False, default=None)
    flag_business_card = models.IntegerField(null=False, default=None)
    id_user = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)

