from django.conf import settings
from django.db import models


AVAILABLE_FIRST_FACTORS = settings.FLEXAUTH_AVAILABLE_1AF
NUM_AVAILABLE_FIRST_FACTORS = len(AVAILABLE_FIRST_FACTORS)

AVAILABLE_SECOND_FACTORS = settings.FLEXAUTH_AVAILABLE_2AF
NUM_AVAILABLE_SECOND_FACTORS = len(AVAILABLE_SECOND_FACTORS)


# See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types


class FirstFactor(models.TextChoices):
    if 'password' in AVAILABLE_FIRST_FACTORS:
        PASSWORD = 'password', "en tapant un mot de passe"
    if 'email' in AVAILABLE_FIRST_FACTORS:
        EMAIL = 'email', "en cliquant sur un lien reçu par email"
    if 'mfs' in AVAILABLE_FIRST_FACTORS:
        MFS = 'mfs', "en utilisant mon compte Maisons France Services"  # maybe later


class SecondFactor(models.TextChoices):
    if 'sms' in AVAILABLE_SECOND_FACTORS:
        SMS = 'sms', "en tapant un code reçu par SMS"
    if 'call' in AVAILABLE_SECOND_FACTORS:
        CALL = 'call', "en tapant un code reçu par appel téléphonique"
    if 'app' in AVAILABLE_SECOND_FACTORS:
        APP = 'app', "en utilisant une application mobile"
    if 'key' in AVAILABLE_SECOND_FACTORS:
        KEY = 'key', "en utilisant une clé de sécurité"
