from francesubdivisions.models import Commune, Epci, Departement, Region


def commune_data_from_slug(slug: str):
    # Given a slug, returns a dictionary of the Commune object
    response = Commune.objects.get(slug=slug).__dict__
    response.pop("_state", None)
    return response


def epci_data_from_slug(slug: str):
    # Given a slug, returns a dictionary of the EPCI object
    response = Epci.objects.get(slug=slug).__dict__
    response.pop("_state", None)
    return response


def departement_data_from_slug(slug: str):
    # Given a slug, returns a dictionary of the Département object
    response = Departement.objects.get(slug=slug).__dict__
    response.pop("_state", None)
    return response


def region_data_from_slug(slug: str):
    # Given a slug, returns a dictionary of the Region object
    response = Region.objects.get(slug=slug).__dict__
    response.pop("_state", None)
    return response
