import sys

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login

from django_otp import login as otp_login


def _get_login_form_class(form_class_name):
    this_module = sys.modules[__name__]
    try:
        return getattr(this_module, form_class_name)
    except AttributeError:
        return None


def get_first_factor_login_form_class(first_factor=None):
    first_factor = first_factor or settings.FLEXAUTH_DEFAULT_1AF
    return _get_login_form_class(
        '%sFirstFactorForm' % first_factor.title()
    )


def get_second_factor_login_form_class(second_factor=None):
    second_factor = second_factor or settings.FLEXAUTH_DEFAULT_2AF
    return _get_login_form_class(
        '%sSecondFactorForm' % second_factor.title()
    )


class BaseUsernameForm(forms.Form):
    username = forms.CharField(label="Identifiant")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id_field = self.fields['username']
        id_field.widget.attrs.update({
            'autofocus': 'true'
        })


class EmailUsernameForm(BaseUsernameForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id_field = self.fields['username']
        id_field.label = "Adresse email"
        id_field.widget = forms.EmailInput()


class BaseFirstFactorForm(forms.Form):
    first_factor = forms.CharField(label="Premier facteur d'authentification")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ff_field = self.fields['first_factor']
        ff_field.widget.attrs.update({
            'autofocus': 'true'
        })

    def authenticate(self, request, username):
        return NotImplementedError


class PasswordFirstFactorForm(BaseFirstFactorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ff_field = self.fields['first_factor']
        ff_field.label = "Mot de passe"
        ff_field.widget = forms.PasswordInput()

    def authenticate(self, request, username):
        password = self.cleaned_data['first_factor']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True


class EmailFirstFactorForm(BaseFirstFactorForm):
    pass


class MfsFirstFactorForm(BaseFirstFactorForm):
    pass


class BaseSecondFactorForm(forms.Form):
    second_factor = forms.CharField(
        label="Second facteur d'authentification",
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.widget.attrs.update({
            'autofocus': 'true'
        })

    def get_otp_device(self):
        try:
            return self.user.tfa_device
        except AttributeError:
            raise RuntimeError("No user found for 2FA validation.")

    def get_otp_token(self):
        return self.cleaned_data['second_factor']

    def generate_challenge(self):
        pass  # noop if no challenge is required with this device type

    def validate(self):
        otp_device = self.get_otp_device()
        if not otp_device:
            raise ValueError("No 2FA validation device found.")
        otp_token = self.get_otp_token()
        if not otp_token:
            raise ValueError("No 2FA validation token found.")

        if otp_device.verify_token(otp_token):
            return True
        else:
            raise forms.ValidationError("Le code de sécurité est invalide.")

    def authenticate(self, request):
        if self.validate():
            otp_login(request, self.get_otp_device())
            return True


class AppSecondFactorForm(BaseSecondFactorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.label = "Code de sécurité"


class KeySecondFactorForm(BaseSecondFactorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.label = "Empreinte de la clé de sécurité"


class PhoneDeviceSecondFactorForm(BaseSecondFactorForm):
    def generate_challenge(self):

        # Those OTP devices need a "challenge" to be generated,
        # ie. a message to be sent (via sms or phone call).
        self.get_otp_device().generate_challenge()


class CallSecondFactorForm(PhoneDeviceSecondFactorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.label = "Code reçu par téléphone"


class SmsSecondFactorForm(PhoneDeviceSecondFactorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.label = "Code reçu par SMS"
