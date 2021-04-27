#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from francesubdivisions.models import Epci, Commune, DataYear, Metadata
from francesubdivisions.utils.datagouv import get_datagouv_file

import csv
import re
import requests
from zipfile import ZipFile
from io import BytesIO, StringIO
import openpyxl_dictreader

BANATIC_ID = "5e1f20058b4c414d3f94460d"

"""
Import de divers fichiers pour récupérer les données extraites de Banatic
- soit directement depuis le site web https://www.banatic.interieur.gouv.fr/
- soit depuis Datagouv https://www.data.gouv.fr/fr/datasets/base-nationale-sur-les-intercommunalites/

À rendre plus générique.

Ce script part du principe que les communes, départements et régions sont déjà importés
et doit donc être appelé après cog_import.py
"""


class Command(BaseCommand):
    help = "Import data from Banatic"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
            choices=["communes", "epci"],
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

        # Now adding the Siren <-> Insee table for Communes first, then the epci and EPCI <=> communes relations

        # Import of the Siren <-> Insee table for Communes
        # That file also has population data
        if all_levels or level == "communes":
            zip_url = "https://www.banatic.interieur.gouv.fr/V5/ressources/documents/document_reference/TableCorrespondanceSirenInsee.zip"
            print(f"🗜️   Parsing archive {zip_url}")

            zip_name = requests.get(zip_url).content

            with ZipFile(BytesIO(zip_name)) as zip_file:
                files_in_zip = zip_file.namelist()
                annual_files = {}
                title_regex = re.compile(r"Banatic_SirenInsee(?P<year>\d{4})\.xlsx")

                for f in files_in_zip:
                    m = title_regex.match(f)
                    if m:
                        year = int(m.group("year"))
                        if year >= 2014:
                            annual_files[year] = f

                if not year:
                    year = max(annual_files)
                year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

                with zip_file.open(annual_files[year]) as xlsx_file:
                    reader = openpyxl_dictreader.DictReader(xlsx_file, "insee_siren")
                    for row in reader:
                        name = row["nom_com"]
                        insee = row["insee"]
                        try:
                            commune = Commune.objects.get(years=year_entry, insee=insee)
                            if commune.name != name:
                                print(
                                    f"Commune name {name} ({insee}) doesn't match with database entry {commune}"
                                )
                            commune.siren = row["siren"]
                            commune.population = row["ptot_2020"]
                            commune.save()
                        except:
                            raise ValueError(f"Commune {name} ({insee}) not found")

                md_entry, md_return_code = Metadata.objects.get_or_create(
                    prop="banatic_communes_year", value=year
                )

        if all_levels or level == "epci":
            epci_regex = re.compile(
                r"Périmètre des EPCI à fiscalité propre - année (?P<year>\d{4})"
            )
            epci_files = get_datagouv_file(BANATIC_ID, epci_regex)

            if not year:
                year = 2020
            year_entry, year_return_code = DataYear.objects.get_or_create(year=year)

            epci_filename = epci_files[year]["url"]

            print(f"🧮   Parsing spreadsheet {epci_filename}")

            # Despite its .xls extension, it is actually a tsv.
            tsv_bytes = requests.get(epci_filename).content

            str_file = StringIO(tsv_bytes.decode("cp1252"), newline="\n")

            reader = csv.DictReader(str_file, delimiter="\t")
            for row in reader:
                epci_name = row["Nom du groupement"]
                epci_type = row["Nature juridique"]
                epci_siren = row["N° SIREN"]

                member_siren = row["Siren membre"]
                member_commune = Commune.objects.get(
                    siren=member_siren, years=year_entry
                )

                epci_entry, return_code = Epci.objects.get_or_create(
                    name=epci_name,
                    epci_type=epci_type,
                    siren=epci_siren,
                )

                epci_entry.create_slug()
                epci_entry.save()
                epci_entry.years.add(year_entry)

                member_commune.epci = epci_entry
                member_commune.save()

            md_entry, md_return_code = Metadata.objects.get_or_create(
                prop="banatic_epci_year", value=year
            )
