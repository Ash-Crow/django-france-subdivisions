import csv
import requests
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper


def parse_csv_from_distant_zip(zip_url, csv_name, column_names, typecheck=False):

    insee_col = column_names["insee_col"]
    name_col = column_names["name_col"]
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
                if "higher_col" in column_names:
                    higher_col = column_names["higher_col"]
                    entry["higher"] = row[higher_col]
                entry["name"] = row[name_col]
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
