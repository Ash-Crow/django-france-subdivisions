from francesubdivisions.models import (
    Metadata,
    Region,
    Departement,
    Epci,
    Commune,
    DataYear,
)
from francesubdivisions.serializers import (
    RegionSerializer,
    DepartementSerializer,
    EpciSerializer,
    CommuneSerializer,
    DataYearSerializer,
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

    # year filter
    regions_year = int(Metadata.objects.get(prop="regions_latest").value)
    departements_year = int(Metadata.objects.get(prop="departements_latest").value)
    epcis_year = int(Metadata.objects.get(prop="epcis_latest").value)
    communes_year = int(Metadata.objects.get(prop="communes_latest").value)

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
            communes_raw = Commune.objects.filter(
                name__unaccent__iexact=query, year__exact=communes_year
            )
    else:
        regions_raw = Region.objects.filter(
            name__unaccent__istartswith=query, year__exact=regions_year
        ).exclude(
            siren__exact=""
        )  # Exclude Mayotte that has no region-level Siren
        departements_raw = Departement.objects.filter(
            name__unaccent__istartswith=query, year__exact=departements_year
        ).exclude(
            siren__exact=""
        )  # Exclude Haute-Corse, Corse-du-Sud, Martinique and Guyane that have no departement-level Siren
        epcis_raw = Epci.objects.filter(
            name__unaccent__icontains=query, year__exact=epcis_year
        )
        communes_raw = Commune.objects.filter(
            name__unaccent__istartswith=query, year__exact=communes_year
        )

    if len(regions_raw):
        regions = []
        for r in regions_raw:
            regions.append({"value": r.siren, "text": r.name, "type": "region"})

        response.append({"groupName": "Régions", "items": regions})

    if len(departements_raw):
        departements = []
        for d in departements_raw:
            departements.append(
                {"value": d.siren, "text": d.name, "type": "departement"}
            )

        response.append({"groupName": "Départements", "items": departements})

    if len(epcis_raw):
        epcis = []
        for e in epcis_raw:
            epcis.append({"value": e.siren, "text": e.name, "type": "epci"})

        response.append({"groupName": "Intercommunalités", "items": epcis})

    if len(communes_raw):
        communes = []
        for c in communes_raw:
            communes.append(
                {
                    "value": c.siren,
                    "text": f"{c.name} ({c.insee})",
                    "name": c.name,
                    "insee": c.insee,
                    "type": "commune",
                }
            )

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
    lookup_field = "pk"


class RegionDetailSiren(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "siren"


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
    lookup_field = "pk"


class DepartementDetailSiren(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "siren"


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


class EpciDetailSiren(generics.RetrieveUpdateDestroyAPIView):
    queryset = Epci.objects.all()
    serializer_class = EpciSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "siren"


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


class CommuneDetailSiren(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "siren"


class CommuneDetailInsee(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "insee"


class DataYearList(generics.ListCreateAPIView):
    queryset = DataYear.objects.all()
    serializer_class = DataYearSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"], ["acronym"]


class DataYearDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataYear.objects.all()
    serializer_class = DataYearSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
