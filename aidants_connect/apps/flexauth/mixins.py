from django.db import models

from . import constants


class WithFlexAuth(models.Model):
    first_factor = models.CharField(
        max_length=8, blank=True, choices=constants.FirstFactor.choices
    )
    second_factor = models.CharField(
        max_length=8, blank=True, choices=constants.SecondFactor.choices
    )

    class Meta:
        abstract = True
