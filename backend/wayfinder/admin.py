from django.contrib import admin
from .models import DailyActivitySummary, Location, UserSettings, Visit

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


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "home_timezone")


@admin.register(DailyActivitySummary)
class DailyActivitySummaryAdmin(admin.ModelAdmin):
    list_display = ("date", "timezone", "location_count", "visit_count", "computed_at")
    list_filter = ("timezone",)
    ordering = ("-date",)
