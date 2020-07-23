from django.conf import settings
from django.db import models

from ..aidants.models import Aidant
from ..mandats.models import Autorisation
from ..usagers.models import Usager


class JournalQuerySet(models.QuerySet):
    def excluding_staff(self):
        return self.exclude(initiator__icontains=settings.STAFF_ORGANISATION_NAME)


class Journal(models.Model):
    ACTIONS = (
        ("connect_aidant", "Connexion d'un aidant"),
        ("activity_check_aidant", "Reprise de connexion d'un aidant"),
        ("franceconnect_usager", "FranceConnexion d'un usager"),
        ("update_email_usager", "L'email de l'usager a été modifié"),
        ("create_attestation", "Création d'une attestation"),
        ("create_autorisation", "Création d'une autorisation"),
        ("use_autorisation", "Utilisation d'une autorisation"),
        ("cancel_autorisation", "Révocation d'une autorisation"),
    )

    INFO_REMOTE_MANDAT = "Mandat conclu à distance pendant l'état d'urgence sanitaire (23 mars 2020)"  # noqa

    # mandatory
    action = models.CharField(max_length=30, choices=ACTIONS, blank=False)
    initiator = models.TextField(blank=False)

    # automatic
    creation_date = models.DateTimeField(auto_now_add=True)

    # action dependant
    demarche = models.CharField(max_length=100, blank=True, null=True)
    usager = models.TextField(blank=True, null=True)
    duree = models.IntegerField(blank=True, null=True)  # En jours
    access_token = models.TextField(blank=True, null=True)
    autorisation = models.IntegerField(blank=True, null=True)
    attestation_hash = models.CharField(max_length=100, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    is_remote_mandat = models.BooleanField(default=False)

    objects = JournalQuerySet.as_manager()

    class Meta:
        db_table = "aidants_connect_web_journal"
        verbose_name = "entrée de journal"
        verbose_name_plural = "entrées de journal"

    def __str__(self):
        return f"Entrée #{self.id} : {self.action} - {self.initiator}"

    def save(self, *args, **kwargs):
        if self.id:
            raise NotImplementedError("Editing is not allowed on journal entries")
        else:
            # COVID-19
            if self.is_remote_mandat:
                self.additional_information = self.INFO_REMOTE_MANDAT
            super(Journal, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Deleting is not allowed on journal entries")

    @property
    def usager_id(self):
        try:
            return int(self.usager.split(" - ")[1])
        except (IndexError, ValueError):
            return None

    @classmethod
    def log_connection(cls, aidant: Aidant):
        return cls.objects.create(
            initiator=aidant.full_string_identifier, action="connect_aidant"
        )

    @classmethod
    def log_activity_check(cls, aidant: Aidant):
        return cls.objects.create(
            initiator=aidant.full_string_identifier, action="activity_check_aidant"
        )

    @classmethod
    def log_franceconnection_usager(cls, aidant: Aidant, usager: Usager):
        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=usager.full_string_identifier,
            action="franceconnect_usager",
        )

    @classmethod
    def log_update_email_usager(cls, aidant: Aidant, usager: Usager):
        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=usager.full_string_identifier,
            action="update_email_usager",
        )

    @classmethod
    def log_attestation_creation(
        cls,
        aidant: Aidant,
        usager: Usager,
        demarches: list,
        duree: int,
        is_remote_mandat: bool,
        access_token: str,
        attestation_hash: str,
    ):
        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=usager.full_string_identifier,
            action="create_attestation",
            demarche=",".join(demarches),
            duree=duree,
            access_token=access_token,
            attestation_hash=attestation_hash,

            # COVID-19
            is_remote_mandat=is_remote_mandat,
            additional_information=(cls.INFO_REMOTE_MANDAT if is_remote_mandat else ""),
        )

    @classmethod
    def log_autorisation_creation(cls, autorisation: Autorisation, aidant: Aidant):
        mandat = autorisation.mandat
        usager = mandat.usager

        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=usager.full_string_identifier,
            action="create_autorisation",
            demarche=autorisation.demarche,
            duree=autorisation.duration_for_humans,
            autorisation=autorisation.id,

            # COVID-19
            is_remote_mandat=mandat.is_remote,
            additional_information=(cls.INFO_REMOTE_MANDAT if mandat.is_remote else ""),
        )

    @classmethod
    def log_autorisation_use(
        cls,
        aidant: Aidant,
        usager: Usager,
        demarche: str,
        access_token: str,
        autorisation: Autorisation,
    ):
        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=usager.full_string_identifier,
            action="use_autorisation",
            demarche=demarche,
            access_token=access_token,
            autorisation=autorisation.id,
        )

    @classmethod
    def log_autorisation_cancel(cls, autorisation: Autorisation, aidant: Aidant):
        return cls.objects.create(
            initiator=aidant.full_string_identifier,
            usager=autorisation.mandat.usager.full_string_identifier,
            action="cancel_autorisation",
            demarche=autorisation.demarche,
            duree=autorisation.duration_for_humans,
            autorisation=autorisation.id,
        )
