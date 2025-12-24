# urls.py

# Django
from django.urls import path, include


# Local App
from .views import (
    ActivityHistoryView,
    OverlandView,
    TripsView,
    TokenView,
    VisitsView,
)


urlpatterns = [
    path("overland/", OverlandView.as_view(), name="overland"),
    path("token/", TokenView.as_view(), name="token"),
    path("visits/", VisitsView.as_view(), name="visits"),
    path("trips/", TripsView.as_view(), name="trips"),
    path("activity/history/", ActivityHistoryView.as_view(), name="activity-history"),
]
