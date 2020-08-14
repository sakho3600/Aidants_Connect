import sys

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login

from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice
from otp_yubikey.models import RemoteYubikeyDevice, ValidationService
from phonenumber_field.formfields import PhoneNumberField
from two_factor.models import PhoneDevice


from .. import constants


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

    def authenticate(self, request):
        return NotImplementedError


class AppSecondFactorForm(BaseSecondFactorForm):
    def authenticate(self, request):
        user = request.user
        totp = user.totp_device
        token = self.cleaned_data['second_factor']
        if totp.verify_token(token):
            otp_login(request, totp)
            return True


class PhoneDeviceSecondFactorForm(BaseSecondFactorForm):
    def authenticate(self, request):
        user = request.user
        phone = user.phone_device
        token = self.cleaned_data['second_factor']
        if phone.verify_token(token):
            otp_login(request, phone)
            return True


class SmsSecondFactorForm(PhoneDeviceSecondFactorForm):
    pass


class CallSecondFactorForm(PhoneDeviceSecondFactorForm):
    pass


class KeySecondFactorForm(BaseSecondFactorForm):
    def authenticate(self, request):
        user = request.user
        yubikey = user.yubikey_device
        token = self.cleaned_data['second_factor']
        if yubikey.verify_token(token):
            otp_login(request, yubikey)
            return True
