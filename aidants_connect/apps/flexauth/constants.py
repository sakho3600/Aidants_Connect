from django.conf import settings
from django.db import models


available_first_factors = settings.FLEXAUTH_AVAILABLE_1AF
available_second_factors = settings.FLEXAUTH_AVAILABLE_2AF


# See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types


class FirstFactor(models.TextChoices):
    if 'password' in available_first_factors:
        PASSWORD = 'password', "en tapant un mot de passe"
    if 'email' in available_first_factors:
        EMAIL = 'email', "en cliquant sur un lien reçu par email"
    if 'mfs' in available_first_factors:
        MFS = 'mfs', "en utilisant mon compte Maisons France Services"  # maybe later...?


class SecondFactor(models.TextChoices):
    if 'sms' in available_second_factors:
        SMS = 'sms', "en tapant un code reçu par SMS"
    if 'call' in available_second_factors:
        CALL = 'call', "en tapant un code reçu par appel téléphonique"
    if 'app' in available_second_factors:
        APP = 'app', "en utilisant une application mobile"
    if 'key' in available_second_factors:
        KEY = 'key', "en utilisant une clé de sécurité"
