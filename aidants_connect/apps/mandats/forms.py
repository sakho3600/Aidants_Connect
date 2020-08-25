from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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


class RecapMandatForm(forms.Form):
    personal_data = forms.BooleanField(
        label="J’autorise mon aidant à utiliser mes données à caractère personnel."
    )
    brief = forms.BooleanField(label="brief")
