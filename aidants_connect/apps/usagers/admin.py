from django.contrib import admin

from nested_admin import NestedModelAdmin, NestedTabularInline
from tabbed_admin import TabbedModelAdmin

from aidants_connect.apps.web.admin import VisibleToStaff

from ..mandats.models import Autorisation, Mandat

from .models import Usager


class AutorisationInline(VisibleToStaff, NestedTabularInline):
    model = Autorisation
    fields = ("demarche", "revocation_date")
    readonly_fields = fields
    extra = 0
    max_num = 0


class MandatInline(VisibleToStaff, NestedTabularInline):
    model = Mandat
    fields = ("organisation", "creation_date", "expiration_date")
    readonly_fields = fields
    extra = 0
    max_num = 0
    inlines = (AutorisationInline,)


class UsagerAdmin(NestedModelAdmin, TabbedModelAdmin):
    list_display = ("__str__", "email", "creation_date")
    search_fields = ("given_name", "family_name", "email")

    tab_infos = (None, {"fields": ("given_name", "family_name", "email")})
    tab_mandats = MandatInline

    tabs = [("Informations", tab_infos), ("Mandats", tab_mandats)]


admin.site.register(Usager, UsagerAdmin)
