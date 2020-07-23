from django.conf import settings
from django.urls import path, include

from two_factor.urls import urlpatterns as tf_urls
from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls

from aidants_connect_web.admin import admin_site


urlpatterns = [
    path(settings.ADMIN_URL, admin_site.urls),
    path(r"admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(r"auth/", include(tf_urls)),
    path(r"auth/twilio/", include(tf_twilio_urls)),
    path(r"", include("aidants_connect_web.urls")),
]
