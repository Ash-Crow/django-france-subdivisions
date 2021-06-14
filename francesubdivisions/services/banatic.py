import csv
import re
import requests
from zipfile import ZipFile
from io import BytesIO, StringIO
import openpyxl_dictreader

from francesubdivisions.models import Epci, Commune, DataYear, Metadata
from francesubdivisions.services.datagouv import get_datagouv_file

BANATIC_ID = "5e1f20058b4c414d3f94460d"


def import_commune_data_from_banatic(year: int = 0) -> None:
    # Imports the Siren <-> Insee table for Communes
    # Communes must have been imported beforehand from COG

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
                matched_year = int(m.group("year"))
                if matched_year >= 2014:
                    annual_files[matched_year] = f

        if not year:
            year = max(annual_files)
        year_entry, _year_return_code = DataYear.objects.get_or_create(year=year)
        print(year_entry)

        with zip_file.open(annual_files[year]) as xlsx_file:
            reader = openpyxl_dictreader.DictReader(xlsx_file, "insee_siren")
            for row in reader:
                import_commune_row_from_banatic(row, year_entry)

        Metadata.objects.get_or_create(prop="banatic_communes_year", value=year)


def import_commune_row_from_banatic(row: dict, year_entry: DataYear):
    name = row["nom_com"]
    insee = row["insee"]
    print(name, insee)
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


def import_epci_data_from_banatic(year: int) -> None:
    # Imports the EPCIs and EPCI <=> communes relations
    # Communes must have been imported beforehand from COG

    epci_regex = re.compile(
        r"Périmètre des EPCI à fiscalité propre - année (?P<year>\d{4})"
    )
    epci_files = get_datagouv_file(BANATIC_ID, epci_regex)

    if not year:
        year = max(epci_files)

    print(epci_files)

    year_entry, _year_return_code = DataYear.objects.get_or_create(year=year)

    epci_filename = epci_files[year]["url"]

    print(f"🧮   Parsing spreadsheet {epci_filename}")

    # Despite its .xls extension, it is actually a tsv.
    tsv_bytes = requests.get(epci_filename).content

    print(tsv_bytes)

    str_file = StringIO(tsv_bytes.decode("cp1252"), newline="\n")

    reader = csv.DictReader(str_file, delimiter="\t")

    rows_number = len(list(reader))

    if rows_number:
        for row in reader:
            import_epci_row_from_banatic(row, year_entry)

        Metadata.objects.get_or_create(prop="banatic_epci_year", value=year)
    else:
        raise ValueError("The spreadsheet is empty")


def import_epci_row_from_banatic(row, year_entry):
    epci_name = row["Nom du groupement"]
    epci_type = row["Nature juridique"]
    epci_siren = row["N° SIREN"]

    member_siren = row["Siren membre"]
    member_commune = Commune.objects.get(siren=member_siren, years=year_entry)

    # Get or create the EPCI
    epci_entry, return_code = Epci.objects.get_or_create(
        name=epci_name,
        epci_type=epci_type,
        siren=epci_siren,
    )
    epci_entry.save()

    if not year_entry in epci_entry.years.all():
        new_year = True
    else:
        new_year = False
    epci_entry.years.add(year_entry)

    if return_code:
        print(f"EPCI {epci_entry} created.")
    elif new_year:
        print(f"EPCI {epci_entry} already in database, updated year.")
    else:
        print(f"EPCI {epci_entry} already in database, skipped.")

    # Adds the membership data on the communes entries
    member_commune.epci = epci_entry
    member_commune.save()
