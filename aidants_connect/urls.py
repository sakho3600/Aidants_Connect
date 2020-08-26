from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from two_factor.urls import urlpatterns as tfa_urls
from two_factor.gateways.twilio.urls import urlpatterns as tfa_twilio_urls

from aidants_connect.apps.aidants import views as aidants_views
from aidants_connect.apps.franceconnect.views import (
    FC_as_FI as FC_as_FI_views,
    FC_as_FS as FC_as_FS_views,
)
from aidants_connect.apps.mandats import views as mandats_views
from aidants_connect.apps.web import views as web_views


urlpatterns = [

    path(settings.ADMIN_URL, admin.site.urls),
    path(r"admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(r"auth/", include("aidants_connect.apps.flexauth.urls", namespace="flexauth")),
    path(r"tfa/", include(tfa_urls)),
    path(r"tfa/tw/", include(tfa_twilio_urls)),


    # --- `aidants` app views

    path("dashboard/", aidants_views.dashboard, name="dashboard"),
    path("usagers/", aidants_views.usagers_index, name="usagers"),
    path("usagers/<int:usager_id>/", aidants_views.usager_details, name="usager_details"),
    path(
        "usagers/<int:usager_id>/mandats/<int:mandat_id>/autorisations/<int:autorisation_id>/cancel_confirm",  # noqa
        aidants_views.usagers_mandats_autorisations_cancel_confirm,
        name="usagers_mandats_autorisations_cancel_confirm",
    ),

    # --- `franceconnect` app views

    # FC_as_FI
    path("authorize/", FC_as_FI_views.authorize, name="authorize"),
    path("token/", FC_as_FI_views.token, name="token"),
    path("userinfo/", FC_as_FI_views.user_info, name="user_info"),
    path("select_demarche/", FC_as_FI_views.fi_select_demarche, name="fi_select_demarche"),

    # FC_as_FS
    path("fc_authorize/", FC_as_FS_views.fc_authorize, name="fc_authorize"),
    path("callback/", FC_as_FS_views.fc_callback, name="fc_callback"),


    # --- `mandats` app views

    path("creation_mandat/", mandats_views.new_mandat, name="new_mandat"),
    path(
        "creation_mandat/recapitulatif/",
        mandats_views.new_mandat_recap,
        name="new_mandat_recap",
    ),
    path(
        "logout-callback/",
        mandats_views.new_mandat_recap,
        name="new_mandat_recap"
    ),
    path(
        "creation_mandat/visualisation/projet/",
        mandats_views.attestation_projet,
        name="new_attestation_projet",
    ),
    path(
        "creation_mandat/succes/",
        mandats_views.new_mandat_success,
        name="new_mandat_success",
    ),
    path(
        "creation_mandat/visualisation/final/",
        mandats_views.attestation_final,
        name="new_attestation_final",
    ),
    path(
        "creation_mandat/qrcode/",
        mandats_views.attestation_qrcode,
        name="new_attestation_qrcode",
    ),


    # --- `web` app views

    path("activity_check/", web_views.activity_check, name="activity_check"),
    path("logout/", web_views.logout_page, name="logout"),
    path("stats/", web_views.statistiques, name="statistiques"),

    path("cgu/", web_views.cgu, name="cgu"),
    path("guide_utilisation/", web_views.guide_utilisation, name="guide_utilisation"),
    path("mentions_legales/", web_views.mentions_legales, name="mentions_legales"),
    path("ressources/", web_views.ressources, name="ressources"),

    path("faq/", web_views.faq_generale, name="faq_generale"),
    path("faq/mandat/", web_views.faq_mandat, name="faq_mandat"),
    path(
        "faq/donnees_personnelles/",
        web_views.faq_donnees_personnelles,
        name="faq_donnees_personnelles",
    ),

    path("", web_views.home_page, name="home_page"),
]
