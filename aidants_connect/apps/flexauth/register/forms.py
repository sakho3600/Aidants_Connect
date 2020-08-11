from django import forms


class IdentityForm(forms.Form):
    first_name
    last_name
    email


class OrganisationForm(forms.Form):
    organisation
    is_mfs


class FirstFactorForm(forms.Form):
    first_factor
    password
    password_confirmation


class SecondFactorForm(forms.Form):
    second_factor
    phone_number


class SecondFactorValidationForm(forms.Form):
    validation_code
