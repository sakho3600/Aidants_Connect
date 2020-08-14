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
    second_factor = forms.CharField(label="Second facteur d'authentification")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sf_field = self.fields['second_factor']
        sf_field.widget.attrs.update({
            'autofocus': 'true'
        })

    def _get_otp_user(self, request):
        return request.user

    def _get_otp_device(self, request):
        return NotImplementedError

    def _get_otp_token(self):
        return self.cleaned_data['second_factor']

    def generate_challenge(self):
        pass  # noop if no challenge is required with this method

    def validate(self, request):
        otp_device = self._get_otp_device(request)
        if not otp_device:
            raise ValueError("No validation device found.")
        otp_token = self._get_otp_token(request)
        if not otp_token:
            raise ValueError("No validation token found.")

        if otp_device.verify_token(otp_token):
            return True

    def authenticate(self, request):
        if self.validate(request):
            otp_login(self.otp_device)
            return True


class AppSecondFactorForm(BaseSecondFactorForm):
    def _get_otp_device(self, request):
        return self._get_otp_user(request).totp_device


class KeySecondFactorForm(BaseSecondFactorForm):
    def _get_otp_device(self, request):
        return self._get_otp_user(request).yubikey_device


class PhoneDeviceSecondFactorForm(BaseSecondFactorForm):
    def _get_otp_device(self, request):
        return self._get_otp_user(request).phone_device

    def generate_challenge(self, request):
        self._get_otp_device(request).generate_challenge()


class CallSecondFactorForm(PhoneDeviceSecondFactorForm):
    pass


class SmsSecondFactorForm(PhoneDeviceSecondFactorForm):
    pass
