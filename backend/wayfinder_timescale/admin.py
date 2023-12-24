from django.contrib import admin

from .models import Location, Visit


# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "time",
        "coordinates_longitude",
        "coordinates_latitude",
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "time",
        "arrival_datetime",
        "departure_datetime",
    )
