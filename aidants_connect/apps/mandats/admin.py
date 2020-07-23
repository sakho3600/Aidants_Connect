from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from aidants_connect.apps.web.admin import VisibleToStaff

from .models import Autorisation, Mandat


class AutorisationInline(VisibleToStaff, TabularInline):
    model = Autorisation
    fields = ("demarche", "revocation_date")
    readonly_fields = fields
    extra = 0
    max_num = 0


class MandatAdmin(VisibleToStaff, ModelAdmin):
    list_display = (
        "id",
        "usager",
        "organisation",
        "creation_date",
        "expiration_date",
        "admin_is_active",
        "is_remote",
    )
    list_filter = ("organisation",)
    search_fields = ("usager__given_name", "usager__family_name", "organisation__name")

    fields = (
        "usager",
        "organisation",
        "duree_keyword",
        "creation_date",
        "expiration_date",
        "admin_is_active",
        "is_remote",
    )

    readonly_fields = fields

    inlines = (AutorisationInline,)


admin.site.register(Mandat, MandatAdmin)
