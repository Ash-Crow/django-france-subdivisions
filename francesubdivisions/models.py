from django.db.models.query import QuerySet
from django.db import models
from django.utils.text import slugify

from francesubdivisions.services.django_admin import TimeStampModel
from francesubdivisions.services.validators import (
    validate_insee_commune,
    validate_siren,
)


# Meta models
class Metadata(TimeStampModel):
    """
    The metadata, as property (prop)/value couples
    """

    prop = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prop}: {self.value}"

    class Meta:
        verbose_name = "métadonnée"


class DataYear(TimeStampModel):
    """
    The years for which we have data stored
    """

    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = "millésime"


class DataSource(TimeStampModel):
    """
    The source file for the data stored
    """

    title = models.CharField("titre", max_length=255)
    url = models.CharField("URL", max_length=255)
    year = models.ForeignKey(
        "DataYear", on_delete=models.RESTRICT, verbose_name="millésime"
    )

    class Meta:
        verbose_name = "source"


# France administrative structure models
class Region(TimeStampModel):
    """
    A French région
    """

    class RegionCategory(models.TextChoices):
        REG = "REG", "Région"
        CTU = "CTU", "Collectivité territoriale unique"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    insee = models.CharField("identifiant Insee", max_length=2)
    siren = models.CharField("numéro Siren", max_length=9)
    category = models.CharField(
        max_length=3,
        choices=RegionCategory.choices,
        null=True,
        verbose_name="catégorie",
    )
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "région"

    def __str__(self):
        return self.name

    def subdivisions_count(self):
        return {
            "departements": self.departement_set.all().count(),
            "communes": Commune.objects.filter(departement__region=self).count(),
        }

    def create_slug(self):
        self.slug = slugify(self.name)


class Departement(TimeStampModel):
    """
    A French département
    """

    class DepartementCategory(models.TextChoices):
        DEPT = "DEPT", "Département"
        PARIS = "PARIS", "Paris"
        ML = "ML", "Métropole de Lyon"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, verbose_name="région"
    )
    insee = models.CharField("identifiant Insee", max_length=3)
    siren = models.CharField("numéro Siren", max_length=9)
    category = models.CharField(
        max_length=5,
        choices=DepartementCategory.choices,
        null=True,
        verbose_name="catégorie",
    )
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "département"

    def __str__(self):
        return f"{self.insee} - {self.name}"

    def create_slug(self):
        self.slug = slugify(self.name)

    def list_epcis(self) -> QuerySet:
        epci_ids = list(
            self.commune_set.all().values_list("epci__id", flat=True).distinct()
        )
        if None in epci_ids:
            # It happens for departements that have isolated communes
            epci_ids.remove(None)

        return Epci.objects.filter(id__in=epci_ids)


class Epci(TimeStampModel):
    """
    A French établissement public de coopération intercommunale
    à fiscalité propre
    """

    class EpciType(models.TextChoices):
        CA = "CA", "Communauté d’agglomération"
        CC = "CC", "Communauté de communes"
        CU = "CU", "Communauté urbaine"
        MET69 = "MET69", "Métropole de Lyon"
        METRO = "METRO", "Métropole"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    epci_type = models.CharField(
        max_length=5, null=True, choices=EpciType.choices, verbose_name="type d’EPCI"
    )
    siren = models.CharField("numéro Siren", max_length=9)
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "EPCI"

    def __str__(self):
        return self.name

    def create_slug(self):
        self.slug = slugify(f"{self.name}-{self.siren}")


class Commune(TimeStampModel):
    """
    A French commune
    """

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    departement = models.ForeignKey(
        "Departement", on_delete=models.CASCADE, verbose_name="département"
    )
    epci = models.ForeignKey(
        "Epci", on_delete=models.CASCADE, null=True, verbose_name="EPCI"
    )
    insee = models.CharField("identifiant Insee", max_length=5)
    siren = models.CharField("numéro Siren", max_length=9)
    population = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "commune"

    def __str__(self):
        return f"{self.name} ({self.departement})"

    def create_slug(self):
        self.slug = slugify(f"{self.name}-{self.insee}")

    def save(self, *args, **kwargs):
        self.create_slug()
        return super().save(*args, **kwargs)


# France collectivities data models
class RegionData(TimeStampModel):
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, verbose_name="région"
    )
    year = models.ForeignKey(
        "DataYear", on_delete=models.PROTECT, verbose_name="millésime"
    )
    datacode = models.CharField("valeur", max_length=255)
    value = models.CharField("valeur", max_length=255, blank=True, null=True)
    datatype = models.CharField("type", max_length=255, blank=True, null=True)
    source = models.ForeignKey(
        "DataSource", on_delete=models.PROTECT, verbose_name="source"
    )

    class Meta:
        verbose_name = "données régions"

    def __str__(self):
        return f"{self.region.name} - {self.year.year} - {self.datacode}: {self.value}"
