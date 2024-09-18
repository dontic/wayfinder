# filters.py

# Django
from django_filters import rest_framework as filters

# Local App
from .models import Location


class LocationFilterSet(filters.FilterSet):
    time_after = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="gte", required=True
    )
    time_before = filters.IsoDateTimeFilter(
        field_name="time", lookup_expr="lte", required=True
    )
    motion_contains = filters.CharFilter(field_name="motion", lookup_expr="contains")
    h_accuracy_lte = filters.NumberFilter(
        field_name="horizontal_accuracy", lookup_expr="lte"
    )
    speed_gte = filters.NumberFilter(field_name="speed", lookup_expr="gte")

    class Meta:
        model = Location
        fields = ["time_after", "time_before"]
