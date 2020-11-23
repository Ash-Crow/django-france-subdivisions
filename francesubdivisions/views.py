from francesubdivisions.models import Region, Departement, Epci, Commune
from francesubdivisions.serializers import (
    RegionSerializer,
    DepartementSerializer,
    EpciSerializer,
    CommuneSerializer,
)
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from unidecode import unidecode


@api_view(["GET"])
def api_root(request, format=None):
    """
    The root of the api for France Subdivisions
    """
    return Response(
        {
            "regions": reverse("region-list", request=request, format=format),
            "departements": reverse("departement-list", request=request, format=format),
            "epci": reverse("epci-list", request=request, format=format),
            "communes": reverse("commune-list", request=request, format=format),
        }
    )


@api_view(["GET"])
def SearchAll(request, query):
    """
    Search within all categories
    """
    # Initiate the lists
    communes_raw = []
    epcis_raw = []
    departements_raw = []
    regions_raw = []
    response = []

    query = unidecode(query).lower()

    if len(query) < 3:
        shortnamed_communes = [
            "by",
            "bu",
            "eu",
            "gy",
            "oz",
            "oo",
            "py",
            "ri",
            "ry",
            "sy",
            "ur",
            "us",
            "uz",
            "y",
        ]
        if query in shortnamed_communes:
            communes_raw = Commune.objects.filter(name__unaccent__iexact=query)
    else:
        regions_raw = Region.objects.filter(name__unaccent__istartswith=query)
        departements_raw = Departement.objects.filter(name__unaccent__istartswith=query)
        epcis_raw = Epci.objects.filter(name__unaccent__icontains=query)
        communes_raw = Commune.objects.filter(name__unaccent__istartswith=query)

    if len(regions_raw):
        regions = []
        for r in regions_raw:
            regions.append({"value": r.siren, "text": r.name})

        response.append({"groupName": "Régions", "items": regions})

    if len(departements_raw):
        departements = []
        for d in departements_raw:
            departements.append({"value": d.siren, "text": d.name})

        response.append({"groupName": "Départements", "items": departements})

    if len(epcis_raw):
        epcis = []
        for e in epcis_raw:
            epcis.append({"value": e.siren, "text": e.name})

        response.append({"groupName": "Intercommunalités", "items": epcis})

    if len(communes_raw):
        communes = []
        for c in communes_raw:
            communes.append({"value": c.siren, "text": f"{c.name} ({c.insee})"})

        response.append({"groupName": "Communes", "items": communes})

    return Response(response)


class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DepartementList(generics.ListCreateAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class DepartementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EpciList(generics.ListCreateAPIView):
    queryset = Epci.objects.all()
    serializer_class = EpciSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class EpciDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Epci.objects.all()
    serializer_class = EpciSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommuneList(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["population"]


class CommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
