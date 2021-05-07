from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from francesubdivisions import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", "insee", "siren")
    list_display = ("name", "insee", "siren", "view_departements_link")
    ordering = ["name"]

    def view_departements_link(self, obj):
        count = obj.departement_set.count()
        url = (
            reverse("admin:francesubdivisions_departement_changelist")
            + "?"
            + urlencode({"region__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} départements</a>', url, count)

    view_departements_link.short_description = "Departements"


@admin.register(models.Departement)
class DepartementAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", "insee", "siren")
    list_display = ("name", "insee", "siren", "view_communes_link")
    ordering = ["name"]

    def view_communes_link(self, obj):
        count = obj.commune_set.count()
        url = (
            reverse("admin:francesubdivisions_commune_changelist")
            + "?"
            + urlencode({"departement__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} communes</a>', url, count)

    view_communes_link.short_description = "Communes"


@admin.register(models.Epci)
class EpciAdmin(admin.ModelAdmin):
    search_fields = ("name", "siren")
    list_display = ("name", "siren", "view_communes_link")
    ordering = ["name"]

    def view_communes_link(self, obj):
        count = obj.commune_set.count()
        url = (
            reverse("admin:francesubdivisions_commune_changelist")
            + "?"
            + urlencode({"epci__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} communes</a>', url, count)

    view_communes_link.short_description = "Communes"


@admin.register(models.Commune)
class CommuneAdmin(admin.ModelAdmin):
    search_fields = ("name", "insee", "siren")
    list_display = ("name", "insee", "siren")
    list_filter = ("years", "departement", "epci")
    ordering = ["name", "insee"]


admin.site.register(models.Metadata)
admin.site.register(models.DataYear)
