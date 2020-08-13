from django import forms
from django.contrib.auth import get_user_model

from django_otp.plugins.otp_totp.models import TOTPDevice
from otp_yubikey.models import RemoteYubikeyDevice, ValidationService
from phonenumber_field.formfields import PhoneNumberField
from two_factor.models import PhoneDevice

from aidants_connect.apps.aidants.models import Aidant, Organisation

from .. import constants


class IdentityForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom de famille")
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(),
    )

    class Meta:
        model = Aidant
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'autofocus': 'true'
        })

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        new_aidant = super().save(commit=False)

        new_aidant.username = new_aidant.email
        new_aidant.set_unusable_password()
        new_aidant.is_active = False
        new_aidant = super().save(commit=commit)

        return new_aidant

class OrganisationForm(forms.ModelForm):
    organisation = forms.ModelChoiceField(
        label="Organisation",
        queryset=Organisation.objects.order_by('name'),
    )

    class Meta:
        model = Aidant
        fields = (
            "organisation",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organisation'].widget.attrs.update({
            'autofocus': 'true'
        })


class FirstFactorForm(forms.ModelForm):
    first_factor = forms.ChoiceField(
        label="Je préfère me connecter...",
        widget=forms.RadioSelect(),
        choices=constants.FirstFactor.choices,
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(),
        required=False,  # only mandatory if password is chosen as first factor
    )
    password2 = forms.CharField(
        label="Mot de passe (confirmation)",
        widget=forms.PasswordInput(),
        required=False,  # only mandatory if password is chosen as first factor
    )

    class Meta:
        model = Aidant
        fields = (
            "first_factor",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data['first_factor'] == 'password' and (
                cleaned_data['password1'] == '' or
                cleaned_data['password2'] == '' or
                cleaned_data['password2'] != cleaned_data['password1']
            )
        ):
            raise forms.ValidationError("Les mots de passe saisis sont différents.")

        return cleaned_data

    def save(self, commit=True):
        new_aidant = super().save(commit=commit)

        if self.cleaned_data['first_factor'] == 'password':
            new_aidant.set_password(self.cleaned_data['password1'])
            new_aidant.save()

        return new_aidant


class SecondFactorForm(forms.ModelForm):
    second_factor = forms.ChoiceField(
        label="Je préfère confirmer mon identité...",
        widget=forms.RadioSelect(),
        choices=constants.SecondFactor.choices,
    )
    phone_number_sms = PhoneNumberField(
        label="... à ce numéro",
        required=False,  # only mandatory if second factor requires phone communication
    )
    phone_number_call = PhoneNumberField(
        label="... à ce numéro",
        required=False,  # only mandatory if second factor requires phone communication
    )

    class Meta:
        model = Aidant
        fields = (
            "second_factor",
            "phone_number_sms",
            "phone_number_call",
        )

    def clean(self):
        cleaned_data = super().clean()

        second_factor = cleaned_data['second_factor']
        if (
            (
                second_factor == 'sms' and
                cleaned_data['phone_number_sms'] == ''
            )
            or
            (
                second_factor == 'call' and
                cleaned_data['phone_number_call'] == ''
            )
        ):
            raise forms.ValidationError("Vous devez saisir un numéro de téléphone.")

        return cleaned_data

    def save(self, commit=True):
        new_aidant = super().save(commit=commit)

        second_factor = self.cleaned_data['second_factor']

        if second_factor in ('sms', 'call'):
            PhoneDevice.objects.create(
                user=new_aidant,
                name='default',
                method=second_factor,
                number=self.cleaned_data['phone_number_%s' % second_factor]
            )

        elif second_factor == 'app':
            TOTPDevice.objects.create(
                user=new_aidant,
                name='default',
            )

        elif second_factor == 'key':
            RemoteYubikeyDevice.objects.create(
                user=new_aidant,
                name='default',
                service=ValidationService.objects.get(name='default'),
            )

        return new_aidant


class SecondFactorValidationForm(forms.Form):
    security_token = forms.CharField(label="Jeton de sécurité")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['security_token'].widget.attrs.update({
            'autofocus': 'true'
        })

    def save(self, user):
        tfa_device = user.tfa_device
        second_factor = user.second_factor

        if second_factor in ('sms', 'call'):
            pass

        elif second_factor == 'app':
            pass

        elif second_factor == 'key':
            tfa_device.public_id = self.cleaned_data['security_token'][:-32]
            tfa_device.save()

        return tfa_device
