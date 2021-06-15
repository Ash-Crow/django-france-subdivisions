import re

from francesubdivisions.services.datagouv import get_datagouv_file
from francesubdivisions.services.utils import parse_csv_from_distant_zip
from francesubdivisions.models import (
    Commune,
    DataSource,
    Departement,
    DepartementData,
    Region,
    DataYear,
    Metadata,
    RegionData,
)

from pprint import pprint

COG_ID = "58c984b088ee386cdb1261f3"
COG_MIN_YEAR = 2019


def import_regions_from_cog(year: int = 0) -> dict:
    region_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des régions")
    region_files = get_datagouv_file(COG_ID, region_regex, COG_MIN_YEAR)

    if not year:
        year = max(region_files)
    year_entry, _year_return_code = DataYear.objects.get_or_create(year=year)

    import_region_file = region_files[year]

    source_entry, _source_return_code = DataSource.objects.get_or_create(
        title=f"COG {import_region_file['title']}",
        url=import_region_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {
            "insee": "REG",
            "name": "LIBELLE",
            "seat_insee": "CHEFLIEU",
        }
    else:
        column_names = {
            "insee": "reg",
            "name": "libelle",
            "seat_insee": "cheflieu",
        }

    regions = parse_csv_from_distant_zip(
        import_region_file["url"],
        f"region{year}.csv",
        column_names,
    )

    for r in regions:
        # Create or update region item
        entry, return_code = Region.objects.get_or_create(
            name=r["name"], insee=r["insee"]
        )
        entry.save()
        if not year_entry in entry.years.all():
            new_year = True
        else:
            new_year = False
        entry.years.add(year_entry)

        if return_code:
            print(f"Région {entry} created.")
        elif new_year:
            print(f"Région {entry} already in database, updated year.")
        else:
            print(f"Région {entry} already in database, skipped.")

        # Import metadata
        seat_metadata, _seat_md_return_code = RegionData.objects.get_or_create(
            region=entry,
            year=year_entry,
            datacode="seat_insee",
            datatype="string",
            value=r["seat_insee"],
            source=source_entry,
        )
        seat_metadata.save()

    Metadata.objects.get_or_create(prop="cog_regions_year", value=year)

    return {"year_entry": year_entry}


def import_departements_from_cog(year):
    depts_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des départements")
    depts_files = get_datagouv_file(COG_ID, depts_regex, COG_MIN_YEAR)

    if not year:
        year = max(depts_files)
    year_entry, _year_return_code = DataYear.objects.get_or_create(year=year)

    import_dept_file = depts_files[year]

    source_entry, _source_return_code = DataSource.objects.get_or_create(
        title=f"COG {import_dept_file['title']}",
        url=import_dept_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {
            "insee": "DEP",
            "name": "LIBELLE",
            "region": "REG",
            "seat_insee": "CHEFLIEU",
        }
    else:
        column_names = {
            "insee": "DEP",
            "name": "libelle",
            "region": "reg",
            "seat_insee": "cheflieu",
        }

    print(import_dept_file["url"])
    depts = parse_csv_from_distant_zip(
        import_dept_file["url"],
        f"departement{year}.csv",
        column_names,
    )

    for d in depts:
        region = Region.objects.get(years=year_entry, insee=d["region"])

        entry, return_code = Departement.objects.get_or_create(
            name=d["name"], insee=d["insee"], region=region
        )
        entry.save()

        if not year_entry in entry.years.all():
            new_year = True
        else:
            new_year = False
        entry.years.add(year_entry)

        if return_code:
            print(f"Département {entry} created.")
        elif new_year:
            print(f"Département {entry} already in database, updated year.")
        else:
            print(f"Département {entry} already in database, skipped.")

        # Import metadata
        seat_metadata, _seat_md_return_code = DepartementData.objects.get_or_create(
            departement=entry,
            year=year_entry,
            datacode="seat_insee",
            datatype="string",
            value=d["seat_insee"],
            source=source_entry,
        )
        seat_metadata.save()

    Metadata.objects.get_or_create(prop="cog_depts_year", value=year)

    return {"year_entry": year_entry}


def import_communes_from_cog(year):

    communes_regex = re.compile(r"^Millésime (?P<year>\d{4})\s:\s+Liste des communes")
    communes_files = get_datagouv_file(COG_ID, communes_regex, COG_MIN_YEAR)

    if not year:
        year = max(communes_files)
    year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

    import_communes_file = communes_files[year]

    if year == 2019:
        csv_filename = "communes-01012019.csv"
    elif year == 2021:
        csv_filename = "commune2021.csv"
    else:
        csv_filename = f"communes{year}.csv"

    source_entry, _source_return_code = DataSource.objects.get_or_create(
        title=f"COG {import_communes_file['title']}",
        url=import_communes_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {"insee": "COM", "name": "LIBELLE", "dept": "DEP"}
        typecheck = {"column": "TYPECOM", "value": "COM"}
    else:
        column_names = {"insee": "com", "name": "libelle", "dept": "dep"}
        typecheck = {"column": "typecom", "value": "COM"}

    communes = parse_csv_from_distant_zip(
        import_communes_file["url"], csv_filename, column_names, typecheck=typecheck
    )

    for c in communes:
        dept = Departement.objects.get(years=year_entry, insee=c["dept"])
        entry, return_code = Commune.objects.get_or_create(
            name=c["name"], insee=c["insee"], departement=dept
        )
        entry.save()

        if not year_entry in entry.years.all():
            new_year = True
        else:
            new_year = False
        entry.years.add(year_entry)

        if return_code:
            print(f"Commune {entry} created.")
        elif new_year:
            print(f"Commune {entry} already in database, updated year.")
        else:
            print(f"Commune {entry} already in database, skipped.")

    md_entry, md_return_code = Metadata.objects.get_or_create(
        prop="cog_communes_year", value=year
    )