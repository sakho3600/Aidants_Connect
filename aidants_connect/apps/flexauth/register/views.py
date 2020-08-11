from . import forms


FORMS = [
    ("identity", forms.IdentityForm),
    ("organisation", forms.OrganisationForm),
    ("first-factor", forms.FirstFactorForm),
    ("second-factor", forms.SecondFactorForm),
    ("second-factor-validation", forms.SecondFactorValidationForm),
]

TEMPLATES = {
    "identity": "flexauth/register/identity.html",
    "organisation": "flexauth/register/organisation.html",
    "first-factor": "flexauth/register/first-factor.html",
    "second-factor": "flexauth/register/second-factor.html",
    "second-factor-validation": "flexauth/register/second-factor-validation.html",
}
