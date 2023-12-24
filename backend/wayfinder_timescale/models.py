from django.conf import settings
from django.db import models

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


# Models change if TimescaleDB is used
class Location(models.Model):
    time = TimescaleDateTimeField(interval=settings.TIMESCALE_INTERVAL)

    type = models.CharField(max_length=50)

    # Geometry
    geometry_type = models.CharField(max_length=50)
    coordinates_longitude = models.DecimalField(max_digits=12, decimal_places=9)
    coordinates_latitude = models.DecimalField(max_digits=12, decimal_places=9)

    # Properties
    activity = models.CharField(max_length=50)
    altitude = models.IntegerField()
    battery_level = models.DecimalField(max_digits=3, decimal_places=2)
    battery_state = models.CharField(max_length=50)
    desired_accuracy = models.IntegerField()
    device_id = models.CharField(max_length=50)
    horizontal_accuracy = models.IntegerField()
    locations_in_payload = models.IntegerField()
    motion = models.CharField(max_length=50, blank=True)  # ['stationary']
    pauses = models.BooleanField()
    speed = models.IntegerField()
    tracking_mode = models.IntegerField()
    vertical_accuracy = models.IntegerField()
    wifi = models.CharField(max_length=50, blank=True)

    objects = models.Manager()
    timescale = TimescaleManager()

    def __str__(self):
        return f"{self.coordinates_latitude}, {self.coordinates_longitude}"


class Visit(models.Model):
    time = TimescaleDateTimeField(interval=settings.TIMESCALE_INTERVAL)

    type = models.CharField(max_length=50)

    # Geometry
    geometry_type = models.CharField(max_length=50)
    coordinates_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    coordinates_latitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Properties
    action = models.CharField(max_length=50)
    arrival_datetime = models.DateTimeField()
    battery_level = models.DecimalField(max_digits=3, decimal_places=2)
    battery_state = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField(blank=True, null=True)  # Can be None
    device_id = models.CharField(max_length=50)
    horizontal_accuracy = models.IntegerField()
    wifi = models.CharField(max_length=50, blank=True)

    objects = models.Manager()
    timescale = TimescaleManager()

    def __str__(self):
        return f"{self.coordinates_latitude}, {self.coordinates_longitude}"
