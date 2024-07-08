from django.urls import path, include
from rest_framework import routers

from building.views import BuildingViewSet, EntranceViewSet, ApartmentViewSet

router = routers.DefaultRouter()
router.register("buildings", BuildingViewSet, basename="building")
router.register("entrances", EntranceViewSet, basename="entrance")
router.register("apartments", ApartmentViewSet, basename="apartment")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "building"
