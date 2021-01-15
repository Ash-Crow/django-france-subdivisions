# django-france-subdivisions
Provides a database structure, API and import scripts to manage French communes, intercommunalités, départements and régions, with their structure and data from Insee and the DGFL. 

# Unaccent extension
If the PostgreSQL user specified in the Django settings is not a superuser, connect to the postgres user and create the Unaccent extension manually

```
psql
\c <dbname>
 "CREATE EXTENSION unaccent;"
```

# Load data
After installation in an operational Django instance, launch the following commands to load data to the database:
- `python manage.py cog_import --year=2020`
- `python manage.py banatic_import --year=2020` with year >= 2020, to load the following data from Banatic:
  - siren and municipal population for communes
  - 
  
# Commands
## `cog_import`:
- goal:load the following data from the Code officiel géographique (COG): list of regions, departements and communes, with how they are linked and: 
  - insee and siren ids for the regions/departements
  - insee for the communes
- parameters:
  - `--level`: partial import of only the specified level (the script expects the higher ones to already be installed) Allowed values: `regions`, `departements`, `communes`
  - `--years`: import the specified year (min: 2019), by default it imports the latest available one in https://www.data.gouv.fr/fr/datasets/code-officiel-geographique-cog/

## `banatic_import`:
- goal:load the following data from the Banatic : 
  - siren ids and population data for the communes
  - insee for the communes
- The script expects that `cog_import` was already run and that the communes level is passed before the epci level.
- parameters:
  - `--level`: partial import of only the specified level. Allowed values: `communes`, `epci`
  - `--years`: import the specified year
    - min: 2019 for the communes level (data is taken from the file `Table de correspondance code SIREN / Code Insee des communes` from https://www.banatic.interieur.gouv.fr/V5/fichiers-en-telechargement/fichiers-telech.php ), by default it imports the latest available one
    - min: 2020 for the epci level (data is taken from https://www.data.gouv.fr/fr/datasets/base-nationale-sur-les-intercommunalites/ )
