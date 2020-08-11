from django.db import models


# See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types


class FirstFactor(models.TextChoices):
    PASSWORD = 'password', "Mot de passe"
    EMAIL = 'email', "Lien envoyé par email"
    MFS = 'mfs', "Compte Maisons France Services"  # maybe later...?


class SecondFactor(models.TextChoices):
    SMS = 'sms', "Code envoyé par SMS"
    CALL = 'call', "Code communiqué par appel téléphonique"
    APP = 'app', "Application TOTP (ex: Authy...)"
    KEY = 'key', "Clé de sécurité (ex: YubiKey...)"
