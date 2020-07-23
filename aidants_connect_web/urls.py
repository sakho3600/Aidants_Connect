from django.urls import path

from aidants_connect_web.views import (
    FC_as_FS,
    id_provider,
    new_mandat,
    service,
    usagers,
)

urlpatterns = [
    # service
    path("activity_check/", service.activity_check, name="activity_check"),
    path("dashboard/", service.dashboard, name="dashboard"),
    # usagers
    path("usagers/", usagers.usagers_index, name="usagers"),
    path("usagers/<int:usager_id>/", usagers.usager_details, name="usager_details"),
    path(
        "usagers/<int:usager_id>/mandats/<int:mandat_id>/autorisations/<int:autorisation_id>/cancel_confirm",  # noqa
        usagers.usagers_mandats_autorisations_cancel_confirm,
        name="usagers_mandats_autorisations_cancel_confirm",
    ),
    # new mandat
    path("creation_mandat/", new_mandat.new_mandat, name="new_mandat"),
    path(
        "creation_mandat/recapitulatif/",
        new_mandat.new_mandat_recap,
        name="new_mandat_recap",
    ),
    path("logout-callback/", new_mandat.new_mandat_recap, name="new_mandat_recap"),
    path(
        "creation_mandat/visualisation/projet/",
        new_mandat.attestation_projet,
        name="new_attestation_projet",
    ),
    path(
        "creation_mandat/succes/",
        new_mandat.new_mandat_success,
        name="new_mandat_success",
    ),
    path(
        "creation_mandat/visualisation/final/",
        new_mandat.attestation_final,
        name="new_attestation_final",
    ),
    path(
        "creation_mandat/qrcode/",
        new_mandat.attestation_qrcode,
        name="new_attestation_qrcode",
    ),
    # id_provider
    path("authorize/", id_provider.authorize, name="authorize"),
    path("token/", id_provider.token, name="token"),
    path("userinfo/", id_provider.user_info, name="user_info"),
    path("logout/", service.logout_page, name="logout"),
    path("select_demarche/", id_provider.fi_select_demarche, name="fi_select_demarche"),
    # FC_as_FS
    path("fc_authorize/", FC_as_FS.fc_authorize, name="fc_authorize"),
    path("callback/", FC_as_FS.fc_callback, name="fc_callback"),
    # public_website
    path("", service.home_page, name="home_page"),
    path("stats/", service.statistiques, name="statistiques"),
    path("cgu/", service.cgu, name="cgu"),
    path("mentions-legales/", service.mentions_legales, name="mentions_legales"),
    path("guide_utilisation/", service.guide_utilisation, name="guide_utilisation"),
    path("ressources/", service.ressources, name="ressources"),
    # # FAQ
    path("faq/", service.faq_generale, name="faq_generale"),
    path("faq/mandat/", service.faq_mandat, name="faq_mandat"),
    path(
        "faq/donnees-personnelles/",
        service.faq_donnees_personnelles,
        name="faq_donnees_personnelles",
    ),
]
