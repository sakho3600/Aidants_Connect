from django.db import models

from django_otp.plugins.otp_totp.models import TOTPDevice
from otp_yubikey.models import RemoteYubikeyDevice
from two_factor.models import PhoneDevice


from . import constants


class WithFlexAuth(models.Model):
    has_completed_registration = models.BooleanField(
        "a terminé son inscription",
        default=False,
    )
    first_factor = models.CharField(
        "préfère se connecter",
        max_length=8,
        blank=True,
        choices=constants.FirstFactor.choices,
    )
    second_factor = models.CharField(
        "confirme son identité",
        max_length=8,
        blank=True,
        choices=constants.SecondFactor.choices,
    )

    class Meta:
        abstract = True

    @property
    def totp_device(self):
        return TOTPDevice.objects.filter(user=self).first()

    @property
    def phone_device(self):
        return PhoneDevice.objects.filter(user=self).first()

    @property
    def yubikey_device(self):
        return RemoteYubikeyDevice.objects.filter(user=self).first()
