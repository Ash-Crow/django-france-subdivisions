from ninja import NinjaAPI
from django.urls import path
from francesubdivisions.api import router as fs_router

api = NinjaAPI()

api.add_router("/", fs_router)

urlpatterns = [
    path("api/", api.urls),
]