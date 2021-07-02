from django import test
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from francesubdivisions.models import (
    Commune,
    Epci,
    Metadata,
    DataYear,
    DataSource,
    Region,
    Departement,
)


class MetadataTestCase(TestCase):
    def setUp(self) -> None:
        Metadata.objects.create(prop="Test", value="first")
        Metadata.objects.create(prop="Test", value="second")

    def test_metadata_is_created(self) -> None:
        test_item = Metadata.objects.get(prop="Test", value="first")
        self.assertEqual(test_item.value, "first")

    def test_metadata_prop_can_have_several_values(self) -> None:
        test_items = Metadata.objects.filter(prop="Test")
        self.assertEqual(test_items.count(), 2)


class DataYearTestCase(TestCase):
    def setUp(self) -> None:
        DataYear.objects.create(year=2020)

    def test_datayear_is_created(self) -> None:
        test_item = DataYear.objects.get(year=2020)
        self.assertEqual(test_item.year, 2020)

    def test_datayear_has_no_duplicate(self) -> None:
        with self.assertRaises(IntegrityError):
            DataYear.objects.create(year=2020)


class DataSourceTestCase(TestCase):
    def setUp(self) -> None:
        year = DataYear.objects.create(year=2020)
        DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )

    def test_datasource_is_created(self) -> None:
        test_item = DataSource.objects.get(year__year=2020)
        self.assertEqual(test_item.title, "Test title")
        self.assertEqual(test_item.url, "http://test-url.com")

    def test_datasource_has_no_duplicate(self) -> None:
        with self.assertRaises(IntegrityError):
            year = DataYear.objects.create(year=2020)
            DataSource.objects.create(
                title="Test title", url="http://test-url.com", year=year
            )


class RegionTestCase(TestCase):
    def setUp(self) -> None:
        test_item = Region.objects.create(insee=11, name="Test region")
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)
        test_item.years.add(year1, year2)
        test_item.save()

        dept01 = Departement.objects.create(name="Dept 1", insee="01", region=test_item)
        dept02 = Departement.objects.create(name="Dept 2", insee="02", region=test_item)
        dept03 = Departement.objects.create(name="Dept 3", insee="03")

        Commune.objects.create(name="Commune 11", insee="01001", departement=dept01)
        Commune.objects.create(name="Commune 12", insee="01002", departement=dept01)
        Commune.objects.create(name="Commune 21", insee="02001", departement=dept02)
        Commune.objects.create(name="Commune 31", insee="03001", departement=dept03)

    def test_region_is_created(self) -> None:
        test_item = Region.objects.get(insee=11)
        self.assertEqual(test_item.name, "Test region")

    def test_region_has_years(self) -> None:
        test_item = Region.objects.get(insee=11)
        self.assertQuerysetEqual(
            test_item.years.values_list("year", flat=True), [2020, 2021], ordered=False
        )

    def test_region_has_no_duplicate(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11, name="Test region")

    def test_region_name_is_not_empty(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11, name="")

        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11)

    def test_region_has_departements(self) -> None:
        test_region = Region.objects.get(insee=11)

        self.assertEqual(test_region.subdivisions_count()["departements"], 2)

    def test_region_has_communes(self) -> None:
        test_region = Region.objects.get(insee=11)

        self.assertEqual(test_region.subdivisions_count()["communes"], 3)


class DepartementTestCase(TestCase):
    def setUp(self) -> None:
        region = Region.objects.create(insee="11", name="Test region")
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)
        region.years.add(year1, year2)
        region.save()

        test_departement = Departement.objects.create(
            name="Test département", insee="01", region=region
        )
        test_departement.years.add(year1, year2)
        test_departement.save()

        epci1 = Epci.objects.create(name="EPCI 1")

        epci2 = Epci.objects.create(name="EPCI 2")

        Commune.objects.create(
            name="Commune 11", insee="01001", departement=test_departement, epci=epci1
        )
        Commune.objects.create(
            name="Commune 12", insee="01002", departement=test_departement, epci=epci2
        )

    def test_departement_is_created(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertEqual(test_item.name, "Test département")

    def test_departement_has_years(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertQuerysetEqual(
            test_item.years.values_list("year", flat=True), [2020, 2021], ordered=False
        )

    def test_departement_name_is_not_empty(self) -> None:
        with self.assertRaises(ValidationError):
            Departement.objects.create(insee="02", name="")

        with self.assertRaises(ValidationError):
            Departement.objects.create(insee="03")

    def test_departement_has_communes(self) -> None:
        test_item = Departement.objects.get(insee="01")

        self.assertEqual(test_item.commune_set.count(), 2)

    def test_departement_has_epcis(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertEqual(test_item.list_epcis().count(), 2)
