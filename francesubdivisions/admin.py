from django.contrib import admin

from francesubdivisions import models
from francesubdivisions.services.django_admin import (
    TimeStampModelAdmin,
    related_object_link,
    view_reverse_changelink,
)


class RegionDataInline(admin.TabularInline):
    model = models.RegionData
    extra = 0


@admin.register(models.Region)
class RegionAdmin(TimeStampModelAdmin):
    search_fields = ("name__startswith", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren", "view_departements_link")
    ordering = ["name"]
    inlines = [RegionDataInline]

    def view_departements_link(self, obj):
        return view_reverse_changelink(
            obj, "francesubdivisions", "region", "departement"
        )

    view_departements_link.short_description = "Départements"

    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "view_departements_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "category",
                    "years",
                    "insee",
                    "siren",
                    "view_departements_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]


@admin.register(models.Departement)
class DepartementAdmin(TimeStampModelAdmin):
    search_fields = ("name__startswith", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren", "view_communes_link")
    list_filter = ("years", "region")
    ordering = ["name"]

    def view_communes_link(self, obj):
        return view_reverse_changelink(
            obj, "francesubdivisions", "departement", "commune"
        )

    view_communes_link.short_description = "Communes"

    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "region_link",
        "view_communes_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "category",
                    "years",
                    "insee",
                    "siren",
                    ("region", "region_link"),
                    "view_communes_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    def region_link(self, obj):
        return related_object_link(obj.region)

    region_link.short_description = "lien"


@admin.register(models.Epci)
class EpciAdmin(TimeStampModelAdmin):
    search_fields = ("name", "slug", "siren")
    list_display = ("name", "slug", "siren", "view_communes_link")
    ordering = ["name"]

    def view_communes_link(self, obj):
        return view_reverse_changelink(obj, "francesubdivisions", "epci", "commune")

    view_communes_link.short_description = "Communes"

    readonly_fields = ["id", "slug", "created_at", "updated_at", "view_communes_link"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "epci_type",
                    "years",
                    "siren",
                    "view_communes_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]


@admin.register(models.Commune)
class CommuneAdmin(TimeStampModelAdmin):
    search_fields = ("name", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren")
    list_filter = ("years", "departement", "epci")
    ordering = ["name", "insee"]
    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "epci_link",
        "departement_link",
        "region_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "population",
                    "years",
                    "insee",
                    "siren",
                    ("departement", "departement_link", "region_link"),
                    ("epci", "epci_link"),
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    def epci_link(self, obj):
        return related_object_link(obj.epci)

    epci_link.short_description = "lien"

    def departement_link(self, obj):
        return related_object_link(obj.departement)

    departement_link.short_description = "département"

    def region_link(self, obj):
        return related_object_link(obj.departement.region)

    region_link.short_description = "région"


admin.site.register(models.Metadata)
admin.site.register(models.DataYear)
admin.site.register(models.DataSource)
