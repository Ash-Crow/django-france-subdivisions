# django-france-subdivisions
Provides a database structure, API and import scripts to manage French communes, intercommunalités, départements and régions, with their struture and data from Insee and the DGFL. 

# Unaccent extension
If the PostgreSQL user specified in the Django settings is not a superuser, connect to the postgres user and create the Unaccent extension manually

```
psql
\c <dbname>
 "CREATE EXTENSION unaccent;"
```