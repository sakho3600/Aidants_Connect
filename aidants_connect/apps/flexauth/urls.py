from django.urls import path

from .login import views as login_views
from .register import views as register_views


app_name = "flexauth"


urlpatterns = [

    path("connexion", login_views.login_username, name="login"),
    path(
        "connexion/premier_facteur",
        login_views.login_first_factor,
        name="login_first_factor"
    ),
    path(
        "connexion/second_facteur",
        login_views.login_second_factor,
        name="login_second_factor"
    ),

    path("inscription", register_views.register_identity, name="register"),
    path(
        "inscription/organisation",
        register_views.register_organisation,
        name="register_organisation"
    ),
    path(
        "inscription/premier_facteur",
        register_views.register_first_factor,
        name="register_first_factor"
    ),
    path(
        "inscription/second_facteur",
        register_views.register_second_factor,
        name="register_second_factor"
    ),
    path(
        "inscription/validation",
        register_views.validate_second_factor,
        name="validate_second_factor"
    ),
    path(
        "inscription/qrcode/<int:totp_device_id>",
        register_views.generate_totp_qrcode,
        name="generate_totp_qrcode"
    ),
    path(
        "inscription/terminee",
        register_views.success,
        name="register_success"
    ),
]
