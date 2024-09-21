# filters.py

# Django
from django_filters import rest_framework as filters

# Local App
from .models import Location, Visit


class LocationFilterSet(filters.FilterSet):
    start_datetime = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="gte", required=True
    )
    end_datetime = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="lte", required=True
    )
    motion_contains = filters.CharFilter(field_name="motion", lookup_expr="contains")
    h_accuracy_lte = filters.NumberFilter(
        field_name="horizontal_accuracy", lookup_expr="lte"
    )
    speed_gte = filters.NumberFilter(field_name="speed", lookup_expr="gte")

    class Meta:
        model = Location
        fields = [
            "start_datetime",
            "end_datetime",
            "motion_contains",
            "h_accuracy_lte",
            "speed_gte",
        ]


class VisitFilterSet(filters.FilterSet):
    start_datetime = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="gte", required=True
    )
    end_datetime = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="lte", required=True
    )

    class Meta:
        model = Visit
        fields = ["start_datetime", "end_datetime"]
