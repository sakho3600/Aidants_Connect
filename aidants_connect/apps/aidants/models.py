from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property


class Organisation(models.Model):
    name = models.TextField("Nom", default="No name provided")
    siret = models.PositiveIntegerField("N° SIRET", default=1)
    address = models.TextField("Adresse", default="No address provided")

    class Meta:
        db_table = "aidants_connect_web_organisation"

    def __str__(self):
        return f"{self.name}"

    @cached_property
    def num_aidants(self):
        return self.aidants.count()

    def admin_num_aidants(self):
        return self.num_aidants

    admin_num_aidants.short_description = "Nombre d'aidants"

    @cached_property
    def num_mandats(self):
        return self.mandats.count()

    def admin_num_mandats(self):
        return self.num_mandats

    admin_num_mandats.short_description = "Nombre de mandats"


class Aidant(AbstractUser):
    profession = models.TextField(blank=False)
    organisation = models.ForeignKey(
        Organisation, null=True, on_delete=models.CASCADE, related_name="aidants"
    )

    class Meta:
        db_table = "aidants_connect_web_aidant"
        verbose_name = "aidant"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_string_identifier(self):
        return f"{self.get_full_name()} - {self.organisation.name} - {self.email}"

    def get_valid_autorisation(self, demarche, usager):
        """
        :param demarche:
        :param usager:
        :return: Autorisation object if this aidant may perform the specified `demarche`
        for the specified `usager`, `None` otherwise.`
        """
        from ..mandats.models import Autorisation  # avoid circular import

        try:
            return (
                Autorisation.objects.active()
                .for_demarche(demarche)
                .for_usager(usager)
                .visible_by(self)
                .get()
            )
        except Autorisation.DoesNotExist:
            return None

    def get_usagers(self):
        """
        :return: a queryset of usagers who have at least one autorisation
        (active or expired) with the aidant's organisation.
        """
        from ..usagers.models import Usager  # avoid circular import

        return Usager.objects.visible_by(self).distinct()

    def get_usager(self, usager_id):
        """
        :return: an usager or `None` if the aidant isn't allowed
        by an autorisation to access this usager.
        """
        from ..usagers.models import Usager  # avoid circular import

        try:
            return self.get_usagers().get(pk=usager_id)
        except Usager.DoesNotExist:
            return None

    def get_usagers_with_active_autorisation(self):
        """
        :return: a queryset of usagers who have an active autorisation
        with the aidant's organisation.
        """
        return self.get_usagers().active()

    def get_autorisations(self):
        """
        :return: a queryset of autorisations visible by this aidant.
        """
        from ..mandats.models import Autorisation  # avoid circular import

        return Autorisation.objects.visible_by(self).distinct()

    def get_autorisation(self, autorisation_id):
        """
        :return: an autorisation or `None` if this autorisation is not
        visible by this aidant.
        """
        from ..mandats.models import Autorisation  # avoid circular import

        try:
            return self.get_autorisations().get(pk=autorisation_id)
        except Autorisation.DoesNotExist:
            return None

    def get_autorisations_for_usager(self, usager):
        """
        :param usager:
        :return: a queryset of the specified usager's autorisations.
        """
        return self.get_autorisations().for_usager(usager)

    def get_active_autorisations_for_usager(self, usager):
        """
        :param usager:
        :return: a queryset of the specified usager's active autorisations
        that are visible by this aidant.
        """
        return self.get_autorisations_for_usager(usager).active()

    def get_inactive_autorisations_for_usager(self, usager):
        """
        :param usager:
        :return: a queryset of the specified usager's inactive (expired or revoked)
        autorisations that are visible by this aidant.
        """
        return self.get_autorisations_for_usager(usager).inactive()

    def get_active_demarches_for_usager(self, usager):
        """
        :param usager:
        :return: a list of demarches the usager has active autorisations for
        in this aidant's organisation.
        """
        return self.get_active_autorisations_for_usager(usager).values_list(
            "demarche", flat=True
        )

    def get_last_action_timestamp(self):
        """
        :return: the timestamp of this aidant's last logged action or `None`.
        """
        from ..logs.models import Journal  # avoid circular import

        try:
            return (
                Journal.objects.filter(initiator=self.full_string_identifier)
                .last()
                .creation_date
            )
        except AttributeError:
            return None

    def get_journal_create_attestation(self, access_token):
        """
        :return: the corresponding 'create_attestation' Journal entry initiated
        by the aidant
        """
        from ..logs.models import Journal  # avoid circular import

        journal_create_attestation = Journal.objects.filter(
            initiator=self.full_string_identifier,
            action="create_attestation",
            access_token=access_token,
        ).last()
        return journal_create_attestation
