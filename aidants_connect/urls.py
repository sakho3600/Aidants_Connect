from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from two_factor.urls import urlpatterns as tf_urls
from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(r"admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(r"auth/", include(tf_urls)),
    path(r"auth/tw/", include(tf_twilio_urls)),
    path(r"", include("aidants_connect.apps.web.urls")),
]
