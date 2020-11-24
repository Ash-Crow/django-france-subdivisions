#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from francesubdivisions.models import Metadata, Departement, Region
import csv
from os import path
from pprint import pprint

year = int(Metadata.objects.get(prop="departements_latest").value)

"""
Import des numéros SIREN des départements et régions depuis des fichiers de l'OFGL
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        # First the regions
        regions_list = path.join("resources", "reg2019.csv")
        with open(regions_list, "r") as input_csv:
            reader = csv.DictReader(input_csv)
            for row in reader:
                reg_id = row["Code Région"]
                siren = row["Siren"]
                try:
                    region_entry = Region.objects.get(insee=reg_id, year=year)
                    region_entry.siren = siren
                    region_entry.save()
                except:
                    print(f"Region {reg_id} not found")

        # Then the departements
        dep_list = path.join("resources", "dep2019.csv")
        with open(dep_list, "r") as input_csv:
            reader = csv.DictReader(input_csv)
            for row in reader:
                dep_id = row["Code Département"]
                siren = row["Code Siren Collectivité"]
                try:
                    dep_entry = Departement.objects.get(insee=dep_id, year=year)
                    dep_entry.siren = siren
                    dep_entry.save()
                except:
                    print(f"Departement {dep_id} not found")
