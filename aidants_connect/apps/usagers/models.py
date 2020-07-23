from django.db import models
from django.utils import timezone

from ..mandats.models import Autorisation, Mandat


class UsagerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(mandats__expiration_date__gt=timezone.now()).distinct()

    def visible_by(self, aidant):
        """
        :param aidant:
        :return: a new QuerySet instance only filtering in the usagers who have
        an autorisation with this aidant's organisation.
        """
        return self.filter(mandats__organisation=aidant.organisation).distinct()


class Usager(models.Model):

    GENDER_FEMALE = "female"
    GENDER_MALE = "male"
    GENDER_CHOICES = (
        (GENDER_FEMALE, "Femme"),
        (GENDER_MALE, "Homme"),
    )
    BIRTHCOUNTRY_FRANCE = "99100"
    EMAIL_NOT_PROVIDED = "noemailprovided@aidantconnect.beta.gouv.fr"

    given_name = models.CharField("Prénom", max_length=255, blank=False)
    family_name = models.CharField("Nom", max_length=255, blank=False)
    preferred_username = models.CharField(max_length=255, blank=True)

    gender = models.CharField(
        "Genre", max_length=6, choices=GENDER_CHOICES, default=GENDER_FEMALE,
    )

    birthdate = models.DateField("Date de naissance", blank=False)
    birthplace = models.CharField(
        "Lieu de naissance", max_length=5, blank=True, null=True
    )
    birthcountry = models.CharField(
        "Pays de naissance", max_length=5, default=BIRTHCOUNTRY_FRANCE,
    )

    sub = models.TextField(blank=False, unique=True)
    email = models.EmailField(blank=False, default=EMAIL_NOT_PROVIDED)
    creation_date = models.DateTimeField("Date de création", default=timezone.now)

    objects = UsagerQuerySet.as_manager()

    class Meta:
        db_table = "aidants_connect_web_usager"
        ordering = ["family_name", "given_name"]

    def __str__(self):
        return f"{self.given_name} {self.family_name}"

    @property
    def full_string_identifier(self):
        return f"{self.get_full_name()} - {self.id} - {self.email}"

    def get_full_name(self):
        return str(self)

    def get_mandat(self, mandat_id):
        try:
            return self.mandats.get(pk=mandat_id)
        except Mandat.DoesNotExist:
            return None

    def get_autorisation(self, mandat_id, autorisation_id):
        try:
            return self.get_mandat(mandat_id).autorisations.get(pk=autorisation_id)
        except (AttributeError, Autorisation.DoesNotExist):
            return None

    def normalize_birthplace(self):
        if not self.birthplace:
            return None

        normalized_birthplace = self.birthplace.zfill(5)
        if normalized_birthplace != self.birthplace:
            self.birthplace = normalized_birthplace
            self.save(update_fields=["birthplace"])

        return self.birthplace
