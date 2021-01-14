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
- `python manage.py cog_import --year=2020` with year >= 2019, to load the following data from the Code officiel géographique (COG): list of regions, departements and communes, with how they are linked and: 
  - insee and siren ids for the regions/departements
  - insee for the communes 
