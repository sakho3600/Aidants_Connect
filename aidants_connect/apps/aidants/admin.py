from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field as ImportExportField
from import_export.widgets import ForeignKeyWidget as ImportExportForeignKeyWidget

from aidants_connect.apps.web.admin import VisibleToStaff

from .forms import AidantChangeForm, AidantCreationForm
from .models import Aidant, Organisation


class OrganisationResource(resources.ModelResource):
    class Meta:
        model = Organisation
        fields = (
            "id",
            "name", "address", "zip_code", "city",
            "siret",
            "contact_firstname", "contact_lastname",
            "contact_email", "contact_phone",
        )


class OrganisationAdmin(VisibleToStaff, ImportExportMixin, ModelAdmin):
    resource_class = OrganisationResource

    list_display = (
        "name", "city", "contact_email", "contact_phone",
        "admin_num_aidants", "admin_num_mandats"
    )
    search_fields = (
        "name", "address", "zip_code", "city",
        "contact_firstname", "contact_lastname"
    )

    fieldsets = (
        (
            "",
            {"fields": (
                "name", "address", "zip_code", "city", "siret"
            )},
        ),
        (
            "Contact",
            {"fields": (
                "contact_firstname", "contact_lastname",
                "contact_email", "contact_phone",
            )},
        ),
    )


class AidantResource(resources.ModelResource):

    # See: https://django-import-export.readthedocs.io/en/latest/api_widgets.html#import_export.widgets.ForeignKeyWidget  # noqa

    organisation = ImportExportField(
        column_name='organisation',
        attribute='organisation',
        widget=ImportExportForeignKeyWidget(
            Organisation, 'name'
        )
    )

    class Meta:
        model = Aidant
        fields = (
            "id",
            "first_name", "last_name", "email",
            "username", "organisation", "profession"
        )

    def after_save_instance(self, instance, using_transactions, dry_run):
        if not dry_run:
            instance.is_active = False
            instance.set_unusable_password()
            instance.save()


class AidantAdmin(VisibleToStaff, ImportExportMixin, DjangoUserAdmin):
    resource_class = AidantResource

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Prevent non-superusers from being able to set
        # the `is_staff` and `is_superuser` flags.
        if not request.user.is_superuser:
            if "is_superuser" in form.base_fields:
                form.base_fields["is_superuser"].disabled = True
            if "is_staff" in form.base_fields:
                form.base_fields["is_staff"].disabled = True

        return form

    # The forms to add and change `Aidant` instances
    form = AidantChangeForm
    add_form = AidantCreationForm

    # The fields to be used in displaying the `Aidant` model.
    # These override the definitions on the base `UserAdmin`
    # that references specific fields on `auth.User`.
    list_display = (
        "__str__", "email", "organisation",
        "has_completed_registration",
        "is_active", "is_staff", "is_superuser",
        "first_factor", "second_factor",
    )
    list_filter = (
        "has_completed_registration",
        "is_active", "is_staff", "is_superuser",
        "first_factor", "second_factor",
    )
    search_fields = ("first_name", "last_name", "email", "organisation__name")
    ordering = ("email",)

    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (
            "Informations personnelles",
            {"fields": (
                "username", "first_name", "last_name", "email", "password"
            )},
        ),
        ("Informations professionnelles", {"fields": ("organisation", "profession")}),
        (
            "Authentification flexible",
            {"fields": (
                "has_completed_registration", "first_factor", "second_factor"
            )},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    # `add_fieldsets` is not a standard `ModelAdmin` attribute. `AidantAdmin`
    # overrides `get_fieldsets` to use this attribute when creating an `Aidant`.
    add_fieldsets = (
        (
            "Informations personnelles",
            {"fields": ("first_name", "last_name", "email", "password", "username")},
        ),
        ("Informations professionnelles", {"fields": ("profession", "organisation")}),
    )


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Aidant, AidantAdmin)
