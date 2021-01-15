from rest_framework import serializers
from francesubdivisions.models import Region, Departement, Epci, Commune


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "insee", "siren", "year"]


class DepartementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departement
        depth = 1
        fields = ["id", "name", "insee", "siren", "year", "region"]


class EpciSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Epci
        fields = ["id", "name", "insee", "siren", "year"]


class CommuneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commune
        depth = 2
        fields = [
            "id",
            "name",
            "insee",
            "siren",
            "year",
            "epci",
            "departement",
            "population",
        ]
