from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Journal


class JournalAdmin(ModelAdmin):
    list_display = ("id", "action", "initiator", "creation_date")
    list_filter = ("action",)
    search_fields = ("action", "initiator")
    ordering = ("-creation_date",)


admin.site.register(Journal, JournalAdmin)
