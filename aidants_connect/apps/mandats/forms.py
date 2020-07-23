from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django_otp import match_token

from aidants_connect import constants


class MandatForm(forms.Form):

    DEMARCHES = [(key, value) for key, value in constants.DEMARCHES.items()]
    demarche = forms.MultipleChoiceField(
        choices=DEMARCHES, required=True, widget=forms.CheckboxSelectMultiple
    )

    # models.MandatDureeKeywords
    DUREES = [
        ("SHORT", {"title": "Mandat court", "description": "(expire demain)"}),
        (
            "EUS_03_20",
            {
                "title": "Mandat confinement",
                "description": "(expire à la fin de l'état d'urgence sanitaire)",
            },
        ),
        ("LONG", {"title": "Mandat long", "description": "(12 mois)"}),
    ]
    duree = forms.ChoiceField(choices=DUREES, required=True, initial=3)

    is_remote = forms.BooleanField(required=False)

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        mandat_duree = cleaned_data.get("duree")
        mandat_is_remote = cleaned_data.get("is_remote")
        if not mandat_is_remote and (mandat_duree == "EUS_03_20"):
            self.add_error(
                "duree",
                forms.ValidationError(
                    "Le mandat confinement ne peut s'effectuer qu'à distance."
                ),
            )
        if mandat_is_remote and (mandat_duree == "LONG"):
            self.add_error(
                "duree",
                forms.ValidationError(
                    "Le mandat long ne peut pas s'effectuer à distance."
                ),
            )


class OTPForm(forms.Form):
    otp_token = forms.CharField(
        max_length=6,
        min_length=6,
        validators=[RegexValidator(r"^\d{6}$")],
        label="Entrez le code à 6 chiffres généré par votre téléphone",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )

    def __init__(self, aidant, *args, **kwargs):
        super(OTPForm, self).__init__(*args, **kwargs)
        self.aidant = aidant

    def clean_otp_token(self):
        otp_token = self.cleaned_data["otp_token"]
        aidant = self.aidant
        good_token = match_token(aidant, otp_token)
        if good_token:
            return otp_token
        else:
            raise ValidationError("Ce code n'est pas valide.")


class RecapMandatForm(OTPForm, forms.Form):
    personal_data = forms.BooleanField(
        label="J’autorise mon aidant à utiliser mes données à caractère personnel."
    )
    brief = forms.BooleanField(label="brief")
