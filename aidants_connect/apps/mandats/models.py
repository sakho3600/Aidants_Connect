from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.functional import cached_property

from aidants_connect import constants


class AutorisationDureeKeywords(models.TextChoices):
    SHORT = (
        "SHORT",
        "pour une durée de 1 jour",
    )
    LONG = (
        "LONG",
        "pour une durée de 1 an",
    )
    EUS_03_20 = (
        "EUS_03_20",
        "jusqu’à la fin de l’état d’urgence sanitaire ",
    )


def get_staff_organisation_name_id() -> int:
    from ..aidants.models import Organisation  # avoid circular import

    try:
        return Organisation.objects.get(name=settings.STAFF_ORGANISATION_NAME).pk
    except Organisation.DoesNotExist:
        return 1


class MandatQuerySet(models.QuerySet):
    def active(self):
        return (
            self.exclude(expiration_date__lt=timezone.now())
            .filter(autorisations__revocation_date__isnull=True)
            .distinct()
        )


class Mandat(models.Model):
    organisation = models.ForeignKey(
        "aidants.Organisation",
        on_delete=models.PROTECT,
        related_name="mandats",
        default=get_staff_organisation_name_id,
    )
    usager = models.ForeignKey(
        "usagers.Usager",
        on_delete=models.PROTECT,
        related_name="mandats"
    )
    creation_date = models.DateTimeField("Date de création", default=timezone.now)
    expiration_date = models.DateTimeField("Date d'expiration", default=timezone.now)
    duree_keyword = models.CharField(
        "Durée", max_length=16, choices=AutorisationDureeKeywords.choices, null=True
    )
    is_remote = models.BooleanField("Signé à distance ?", default=False)

    objects = MandatQuerySet.as_manager()

    class Meta:
        db_table = "aidants_connect_web_mandat"

    def __str__(self):
        return f"#{self.id}"

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expiration_date

    @cached_property
    def is_active(self):
        # A `mandat` is considered `active` if it contains
        # at least one active `autorisation`.
        return self.autorisations.active().exists()

    def admin_is_active(self):
        return self.is_active
    admin_is_active.boolean = True
    admin_is_active.short_description = "is active"


class AutorisationQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(
            mandat__expiration_date__lt=timezone.now()
        ).filter(
            revocation_date__isnull=True
        )

    def inactive(self):
        return self.filter(
            Q(mandat__expiration_date__lt=timezone.now())
            | (
                Q(mandat__expiration_date__gt=timezone.now())
                & Q(revocation_date__isnull=False)
            )
        )

    def expired(self):
        return self.filter(mandat__expiration_date__lt=timezone.now())

    def revoked(self):
        return self.filter(
            Q(mandat__expiration_date__gt=timezone.now())
            & Q(revocation_date__isnull=False)
        )

    def for_usager(self, usager):
        return self.filter(mandat__usager=usager)

    def for_demarche(self, demarche):
        return self.filter(demarche=demarche)

    def visible_by(self, aidant):
        return self.filter(mandat__organisation=aidant.organisation)


class Autorisation(models.Model):

    DEMARCHE_CHOICES = [
        (name, attributes["titre"]) for name, attributes in constants.DEMARCHES.items()
    ]

    # Autorisation information
    mandat = models.ForeignKey(
        Mandat, on_delete=models.CASCADE, related_name="autorisations", null=True
    )
    demarche = models.CharField(max_length=16, choices=DEMARCHE_CHOICES)

    # Autorisation expiration date management
    revocation_date = models.DateTimeField("Date de révocation", blank=True, null=True)

    # Journal entry creation information
    last_renewal_token = models.TextField(blank=False, default="No token provided")

    objects = AutorisationQuerySet.as_manager()

    class Meta:
        db_table = "aidants_connect_web_autorisation"

    def __str__(self):
        return f"#{self.id}"

    @cached_property
    def creation_date(self):
        return self.mandat.creation_date

    @cached_property
    def expiration_date(self):
        return self.mandat.expiration_date

    @cached_property
    def is_expired(self) -> bool:
        return self.mandat.is_expired

    @property
    def is_revoked(self) -> bool:
        return True if self.revocation_date else False

    @property
    def duration_for_humans(self) -> int:
        duration_for_computer = self.expiration_date - self.creation_date

        # We add one day so that duration is human-friendly.
        # i.e. for a human, there is one day between now and tomorrow at the same time,
        # and 0 for a computer.
        return duration_for_computer.days + 1


class ConnectionQuerySet(models.QuerySet):
    def expired(self):
        return self.filter(expires_on__lt=timezone.now())


def default_connection_expiration_date():
    now = timezone.now()
    return now + timedelta(seconds=settings.FC_CONNECTION_AGE)


class Connection(models.Model):
    state = models.TextField()  # FS
    nonce = models.TextField(default="No Nonce Provided")  # FS
    CONNECTION_TYPE = (("FS", "FC as FS"), ("FI", "FC as FI"))  # FS
    connection_type = models.CharField(
        max_length=2, choices=CONNECTION_TYPE, default="FI", blank=False
    )
    demarches = ArrayField(models.TextField(default="No démarche"), null=True)  # FS
    duree_keyword = models.CharField(
        max_length=16, choices=AutorisationDureeKeywords.choices, null=True
    )
    mandat_is_remote = models.BooleanField(default=False)
    usager = models.ForeignKey(
        "usagers.Usager",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="connections",
    )  # FS
    expires_on = models.DateTimeField(default=default_connection_expiration_date)  # FS
    access_token = models.TextField(default="No token provided")  # FS

    code = models.TextField()
    demarche = models.TextField(default="No demarche provided")
    aidant = models.ForeignKey(
        "aidants.Aidant",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="connections",
    )
    complete = models.BooleanField(default=False)
    autorisation = models.ForeignKey(
        Autorisation,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="connections",
    )

    objects = ConnectionQuerySet.as_manager()

    class Meta:
        db_table = "aidants_connect_web_connection"
        verbose_name = "connexion"

    def __str__(self):
        return f"Connexion #{self.id} - {self.usager}"

    @property
    def is_expired(self):
        return self.expires_on < timezone.now()
