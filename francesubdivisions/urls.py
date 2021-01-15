from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from francesubdivisions import views

urlpatterns = [
    path("all/<str:query>", views.SearchAll, name="search-all"),
    path("regions/", views.RegionList.as_view(), name="region-list"),
    path("regions/<int:pk>/", views.RegionDetail.as_view(), name="region-detail"),
    path(
        "regions/siren/<int:siren>/",
        views.RegionDetailSiren.as_view(),
        name="region-detail-siren",
    ),
    path("departements/", views.DepartementList.as_view(), name="departement-list"),
    path(
        "departements/<int:pk>/",
        views.DepartementDetail.as_view(),
        name="departement-detail",
    ),
    path(
        "departements/siren/<int:siren>/",
        views.DepartementDetailSiren.as_view(),
        name="departement-detail-siren",
    ),
    path("epci/", views.EpciList.as_view(), name="epci-list"),
    path("epci/<int:pk>/", views.EpciDetail.as_view(), name="epci-detail"),
    path(
        "epci/siren/<int:siren>/",
        views.EpciDetailSiren.as_view(),
        name="epci-detail-siren",
    ),
    path("communes/", views.CommuneList.as_view(), name="commune-list"),
    path("communes/<int:pk>/", views.CommuneDetail.as_view(), name="commune-detail"),
    path(
        "communes/siren/<int:siren>/",
        views.CommuneDetailSiren.as_view(),
        name="commune-detail-siren",
    ),
    path(
        "communes/insee/<int:insee>/",
        views.CommuneDetailInsee.as_view(),
        name="commune-detail-insee",
    ),
    path("datayear/", views.DataYearList.as_view(), name="datayear-list"),
    path("datayear/<int:pk>/", views.DataYearDetail.as_view(), name="datayear-detail"),
    path("", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)