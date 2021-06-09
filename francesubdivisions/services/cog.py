import re

from francesubdivisions.services.datagouv import get_datagouv_file
from francesubdivisions.services.utils import parse_csv_from_distant_zip
from francesubdivisions.models import DataSource, Region, DataYear, Metadata, RegionData

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
    pprint(import_region_file)

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
        seat_metadata, _seat_metadata_return_code = RegionData.objects.get_or_create(
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
