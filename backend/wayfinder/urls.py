# urls.py

# Django
from django.urls import path, include


# Local App
from .views import (
    ActivityHistoryView,
    OverlandView,
    TripPlotView,
    TokenView,
    VisitPlotView,
)


urlpatterns = [
    path("overland/", OverlandView.as_view(), name="overland"),
    path("token/", TokenView.as_view(), name="token"),
    path("visits/plot/", VisitPlotView.as_view(), name="visits-plot"),
    path("trips/plot/", TripPlotView.as_view(), name="trips-plot"),
    path("activity/history/", ActivityHistoryView.as_view(), name="activity-history"),
]
