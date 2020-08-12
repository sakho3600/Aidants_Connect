from django.db import models


# See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types


class FirstFactor(models.TextChoices):
    PASSWORD = 'password', "en tapant un mot de passe"
    EMAIL = 'email', "en cliquant sur un lien reçu par email"
    MFS = 'mfs', "en utilisant mon compte Maisons France Services"  # maybe later...?


class SecondFactor(models.TextChoices):
    SMS = 'sms', "en tapant un code reçu par SMS"
    CALL = 'call', "en tapant un code reçu par appel téléphonique"
    APP = 'app', "en utilisant une application mobile"
    KEY = 'key', "en utilisant une clé de sécurité"
