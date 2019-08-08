from django.urls import path
from aidants_connect_web import views


urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("mandats/", views.mandats, name="mandats"),
    path("new_mandat/", views.new_mandat, name="new_mandat"),
    path("recap/", views.recap, name="recap"),
    path("authorize/", views.authorize, name="authorize"),
    path("token/", views.token, name="token"),
    path("userinfo/", views.user_info, name="user_info"),
    path("logout/", views.logout_page, name="logout"),
    path("fc_authorize/", views.fc_authorize, name="fc_authorize"),
    path("callback/", views.fc_callback, name="fc_callback"),
    path("logout-callback/", views.recap, name="recap"),
    path("select_demarche/", views.fi_select_demarche, name="fi_select_demarche"),
    path("generate_mandat_pdf/", views.generate_mandat_pdf, name="generate_mandat_pdf"),
]
