import re

from francesubdivisions.services.datagouv import get_datagouv_file
from francesubdivisions.services.utils import parse_csv_from_distant_zip
from francesubdivisions.models import Region, DataYear, Metadata

from pprint import pprint

COG_ID = "58c984b088ee386cdb1261f3"
COG_MIN_YEAR = 2019


def import_regions_from_cog(year: int):
    region_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des régions")
    region_files = get_datagouv_file(COG_ID, region_regex, COG_MIN_YEAR)

    if not year:
        year = max(region_files)
    year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

    import_region_file = region_files[year]
    pprint(import_region_file)

    if year >= 2021:
        column_names = {"insee_col": "REG", "name_col": "LIBELLE"}
    else:
        column_names = {"insee_col": "reg", "name_col": "libelle"}

    regions = parse_csv_from_distant_zip(
        import_region_file["url"],
        f"region{year}.csv",
        column_names,
    )

    for r in regions:
        entry, return_code = Region.objects.get_or_create(
            name=r["name"], insee=r["insee"]
        )
        entry.create_slug()
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

    md_entry, md_return_code = Metadata.objects.get_or_create(
        prop="cog_regions_year", value=year
    )

    return year_entry