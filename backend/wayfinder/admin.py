from django.contrib import admin
from .models import Location, Visit

# Register your models here.


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "time",
        "longitude",
        "latitude",
        "altitude",
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "arrival_date",
        "departure_date",
        "latitude",
        "longitude",
    )
