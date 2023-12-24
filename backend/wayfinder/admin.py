from django.contrib import admin

from .models import Location, Visit


# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "coordinates_longitude",
        "coordinates_latitude",
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "arrival_datetime",
        "departure_datetime",
    )
