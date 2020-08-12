from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from two_factor.urls import urlpatterns as tfa_urls
from two_factor.gateways.twilio.urls import urlpatterns as tfa_twilio_urls


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(r"admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(r"auth/", include("aidants_connect.apps.flexauth.urls", namespace="flexauth")),
    path(r"tfa/", include(tfa_urls)),
    path(r"tfa/tw/", include(tfa_twilio_urls)),
    path(r"", include("aidants_connect.apps.web.urls")),
]
