from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from stdnum.fr import siren
from django.utils.translation import gettext_lazy as _

# Validators
validate_insee_commune = RegexValidator(r"^\d[0-9AB][0-9P]\d\d$")


def validate_siren(value):
    try:
        siren.validate(value)
    except (InvalidChecksum, InvalidFormat, InvalidLength):
        raise ValidationError(
            _("%(value)s is not an valid siren id"),
            params={"value": value},
        )


# Models
class Metadata(models.Model):
    """
    The metadata, as property (prop)/value couples
    """

    created = models.DateTimeField(auto_now_add=True)
    prop = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prop}: {self.value}"

    class Meta:
        verbose_name = "métadonnée"


class DataYear(models.Model):
    """
    The years for which we have data stored
    """

    created = models.DateTimeField(auto_now_add=True)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = "millésime"


class Region(models.Model):
    """
    A French région
    """

    class RegionCategory(models.TextChoices):
        REG = "REG", "Région"
        CTU = "CTU", "Collectivité territoriale unique"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    years = models.ManyToManyField(DataYear)
    insee = models.CharField(max_length=2)
    siren = models.CharField(max_length=9)
    category = models.CharField(max_length=3, choices=RegionCategory.choices, null=True)
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


class Departement(models.Model):
    """
    A French département
    """

    class DepartementCategory(models.TextChoices):
        DEPT = "DEPT", "Département"
        PARIS = "PARIS", "Paris"
        ML = "ML", "Métropole de Lyon"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    years = models.ManyToManyField(DataYear)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    insee = models.CharField(max_length=3)
    siren = models.CharField(max_length=9)
    category = models.CharField(
        max_length=5, choices=DepartementCategory.choices, null=True
    )
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "département"

    def __str__(self):
        return f"{self.insee} - {self.name}"

    def create_slug(self):
        self.slug = slugify(self.name)


class Epci(models.Model):
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

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    years = models.ManyToManyField(DataYear)
    epci_type = models.CharField(max_length=5, null=True, choices=EpciType.choices)
    siren = models.CharField(max_length=9)
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "EPCI"

    def __str__(self):
        return self.name

    def create_slug(self):
        self.slug = slugify(f"{self.name}-{self.siren}")


class Commune(models.Model):
    """
    A French commune
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    years = models.ManyToManyField(DataYear)
    departement = models.ForeignKey("Departement", on_delete=models.CASCADE)
    epci = models.ForeignKey("Epci", on_delete=models.CASCADE, null=True)
    insee = models.CharField(max_length=5)
    siren = models.CharField(max_length=9)
    population = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "commune"

    def __str__(self):
        return f"{self.name} ({self.departement})"

    def create_slug(self):
        self.slug = slugify(f"{self.name}-{self.insee}")