# urls.py

# Django
from django.urls import path, include

# REST Framework
from rest_framework.routers import DefaultRouter

# Local App
from .views import OverlandView, LocationViewSet, VisitViewSet, VisitPlotView, TripPlotView, TokenView


urlpatterns = [
    path("overland/", OverlandView.as_view(), name="overland"),
    path("token/", TokenView.as_view(), name="token"),
    path("visits/plot/", VisitPlotView.as_view(), name="visits-plot"),
    path("trips/plot/", TripPlotView.as_view(), name="trips-plot"),
]

router = DefaultRouter()
router.register(r"locations", LocationViewSet)
router.register(r"visits", VisitViewSet)

urlpatterns += [
    path("", include(router.urls)),
]
