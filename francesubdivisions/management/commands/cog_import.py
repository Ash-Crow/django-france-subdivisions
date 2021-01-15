#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from francesubdivisions.models import Commune, Departement, Region, DataYear, Metadata
from francesubdivisions.models import validate_insee_commune
from francesubdivisions.utils.datagouv import get_datagouv_file
import csv
from os import path
from pprint import pprint
import re
import requests
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper


"""
Ce script récupère les données de
https://www.data.gouv.fr/fr/datasets/code-officiel-geographique-cog/
pour les régions, départements et communes à partir de 2019

D'après https://www.insee.fr/fr/information/2560452:
"Depuis le millésime 2019, les fichiers ont sensiblement évolué 
dans leur format et leur structure."
"""

COG_ID = "58c984b088ee386cdb1261f3"
COG_MIN_YEAR = 2019


class Command(BaseCommand):
    help = "Import data from the Code officiel géographique"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
        )
        parser.add_argument(
            "--year", type=int, help="If specified, only that year will be parsed"
        )

    def handle(self, *args, **options):
        if options["level"]:
            level = options["level"]
            all_levels = False
        else:
            level = None
            all_levels = True

        if options["year"]:
            year = int(options["year"])
        else:
            year = 0

        # Now going down from higher level: Régions, Départements, Communes

        # Régions
        if all_levels or level == "regions":
            # First, the data from the COG
            region_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des régions")
            region_files = get_datagouv_file(COG_ID, region_regex, COG_MIN_YEAR)

            if not year:
                year = max(region_files)
            year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

            import_region_file = region_files[year]

            regions = parse_csv_from_distant_zip(
                import_region_file["url"],
                f"region{year}.csv",
                "reg",
            )

            for r in regions:
                entry, return_code = Region.objects.get_or_create(
                    name=r["name"], insee=r["insee"]
                )
                entry.save()
                entry.years.add(year_entry)

                if return_code:
                    print(f"Région {entry} created.")
                else:
                    print(f"Région {entry} already in database, skipped.")

            md_entry, md_return_code = Metadata.objects.get_or_create(
                prop="cog_regions_year", value=year
            )

            # Then the SIRENs from a local file
            regions_list = path.join(
                "francesubdivisions", "resources", "regions-siren.csv"
            )
            add_sirens_and_categories(regions_list, Region, year_entry)

        # Départements
        if all_levels or level == "departements":
            # First, the data from the COG
            depts_regex = re.compile(
                r"Millésime (?P<year>\d{4})\s: Liste des départements"
            )
            depts_files = get_datagouv_file(COG_ID, depts_regex, COG_MIN_YEAR)

            if not year:
                year = max(dept_files)
            year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

            import_dept_file = depts_files[year]

            depts = parse_csv_from_distant_zip(
                import_dept_file["url"],
                f"departement{year}.csv",
                "dep",
                "reg",
            )

            for d in depts:
                region = Region.objects.get(years=year_entry, insee=d["higher"])

                entry, return_code = Departement.objects.get_or_create(
                    name=d["name"], insee=d["insee"], region=region
                )
                entry.save()
                entry.years.add(year_entry)

                if return_code:
                    print(f"Département {entry} created.")
                else:
                    print(f"Département {entry} already in database, skipped.")

            md_entry, md_return_code = Metadata.objects.get_or_create(
                prop="cog_depts_year", value=year
            )

            # Then the SIRENs from a local file
            depts_list = path.join(
                "francesubdivisions", "resources", "departements-siren.csv"
            )
            add_sirens_and_categories(depts_list, Departement, year_entry)

        # Communes
        if all_levels or level == "communes":
            communes_regex = re.compile(
                r"^Millésime (?P<year>\d{4})\s: Liste des communes"
            )
            communes_files = get_datagouv_file(COG_ID, communes_regex, COG_MIN_YEAR)

            if not year:
                year = max(communes_files)
            year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

            import_communes_file = communes_files[year]

            if year == 2019:
                csv_filename = "communes-01012019.csv"
            else:
                csv_filename = f"communes{year}.csv"

            communes = parse_csv_from_distant_zip(
                import_communes_file["url"],
                csv_filename,
                "com",
                "dep",
                ("typecom", "COM"),
            )

            for c in communes:
                dept = Departement.objects.get(years=year_entry, insee=c["higher"])
                entry, return_code = Commune.objects.get_or_create(
                    name=c["name"], insee=c["insee"], departement=dept
                )

                entry.save()
                entry.years.add(year_entry)

                if return_code:
                    print(f"Commune {entry} created.")
                else:
                    print(f"Commune {entry} already in database, skipped.")

            md_entry, md_return_code = Metadata.objects.get_or_create(
                prop="cog_communes_year", value=year
            )


def parse_csv_from_distant_zip(
    zip_url, csv_name, insee_col, higher_col="", typecheck=False
):
    print(f"🗜️   Parsing archive {zip_url}")
    zip_name = requests.get(zip_url).content
    with ZipFile(BytesIO(zip_name)) as zip_file:
        with zip_file.open(csv_name) as csv_file:
            reader = csv.DictReader(TextIOWrapper(csv_file, encoding="utf-8-sig"))
            entries = []
            if typecheck:
                tc_col = typecheck[0]
                tc_val = typecheck[1]

            for row in reader:
                if typecheck:
                    if row[tc_col] != tc_val:
                        continue
                entry = {}
                entry["insee"] = row[insee_col]
                if higher_col:
                    entry["higher"] = row[higher_col]
                entry["name"] = row["libelle"]
                entries.append(entry)
            return entries


def add_sirens_and_categories(input_file, model_name, year_entry):
    with open(input_file, "r") as input_csv:
        reader = csv.DictReader(input_csv)
        for row in reader:
            insee = row["Insee"]
            siren = row["Siren"]
            category = row["CATEG"]

            if category != "ML":
                # The Métropole de Lyon is managed only at the EPCI level
                try:
                    collectivity_entry = model_name.objects.get(
                        insee=insee, years=year_entry
                    )
                    collectivity_entry.siren = siren
                    collectivity_entry.category = category
                    collectivity_entry.save()
                except:
                    print(f"{model_name} {insee} not found")
