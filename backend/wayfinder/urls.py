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
    path("visits/", VisitPlotView.as_view(), name="visits"),
    path("trips/", TripPlotView.as_view(), name="trips"),
    path("activity/history/", ActivityHistoryView.as_view(), name="activity-history"),
]
