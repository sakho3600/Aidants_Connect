from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from aidants_connect.apps.web.admin import VisibleToStaff

from .forms import AidantChangeForm, AidantCreationForm
from .models import Aidant, Organisation


class OrganisationAdmin(VisibleToStaff, ModelAdmin):
    list_display = ("name", "address", "admin_num_aidants", "admin_num_mandats")
    search_fields = ("name",)


class AidantAdmin(VisibleToStaff, DjangoUserAdmin):

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
    list_display = ("__str__", "email", "organisation", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("first_name", "last_name", "email", "organisation__name")
    ordering = ("email",)

    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (
            "Informations personnelles",
            {"fields": ("username", "first_name", "last_name", "email", "password")},
        ),
        ("Informations professionnelles", {"fields": ("profession", "organisation")}),
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
