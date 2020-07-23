from datetime import timedelta

from django.utils.timezone import now

import factory

from ..aidants.factories import OrganisationFactory
from ..usagers.factories import UsagerFactory

from .models import Autorisation, Connection, Mandat


class MandatFactory(factory.DjangoModelFactory):
    organisation = factory.SubFactory(OrganisationFactory)
    usager = factory.SubFactory(UsagerFactory)
    creation_date = factory.LazyAttribute(lambda f: now())
    duree_keyword = "SHORT"
    expiration_date = factory.LazyAttribute(lambda f: now() + timedelta(days=1))

    class Meta:
        model = Mandat


class AutorisationFactory(factory.DjangoModelFactory):
    demarche = "justice"
    mandat = factory.SubFactory(MandatFactory)
    revocation_date = None

    class Meta:
        model = Autorisation


class LegacyAutorisationFactory(AutorisationFactory):

    # Used to test the migration script that actually *creates* mandats ^^
    mandat = None

    class Meta:
        model = Autorisation


class ConnectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Connection
