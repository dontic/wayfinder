# models.py

from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


class TimescaleModel(models.Model):
    """
    A helper class for using Timescale within Django, has the TimescaleManager and
    TimescaleDateTimeField already present. This is an abstract class it should
    be inheritted by another class for use.
    """

    time = TimescaleDateTimeField(interval="1 day")

    objects = TimescaleManager()

    class Meta:
        abstract = True


class Location(TimescaleModel):
    """
    This is a TimescaleModel that stores the locations from Overland.
    It already inherits the 'time' field from the TimescaleModel.
    """

    # time = TimescaleDateTimeField(interval="1 day")

    longitude = models.DecimalField(max_digits=20, decimal_places=17)

    latitude = models.DecimalField(max_digits=20, decimal_places=17)

    # Properties

    # Altitude of the location in meters
    altitude = models.IntegerField()

    # The iPhone's battery level, between 0.00 and 1.00
    battery_level = models.DecimalField(max_digits=3, decimal_places=2)

    # The iPhone's battery state, it can be 'charging', 'full', 'unplugged', or 'unknown'
    battery_state = models.CharField(max_length=20)

    # Direction of travel in degrees (-1 if speed unknown)
    course = models.IntegerField()

    # The accuracy of the course in degrees (-1 if speed is unknown)
    course_accuracy = models.DecimalField(max_digits=5, decimal_places=2)

    # The device id set in Overland settings or an empty string if not set
    device_id = models.CharField(max_length=50, blank=True)

    # The accuracy of the position in meters
    horizontal_accuracy = models.IntegerField()

    # A list of motions, ['driving', 'walking', 'running', 'cycling', 'stationary']
    # Note that you can have several such as driving and stationary
    motion = models.JSONField()

    # The speed in meters per seocond (-1 if unknown)
    speed = models.IntegerField()

    # The accuracy of the speed in meters per second (-1 if speed is unknown)
    speed_accuracy = models.DecimalField(max_digits=5, decimal_places=2)

    # The timestamp of the location
    # Set to the Timescale's time field
    # timestamp = models.DateTimeField()

    # The unique if if set
    unique_id = models.CharField(max_length=50, blank=True, null=True)

    # The vertical accuracy in meters
    vertical_accuracy = models.IntegerField()

    # Wifi SSID if connected to a wifi network, an empty string if not connected
    wifi = models.CharField(max_length=100, blank=True)


class Visit(TimescaleModel):
    """
    This is a TimescaleModel that stores visits from Overland.
    It already inherits the 'time' field from the TimescaleModel.
    """

    # time = TimescaleDateTimeField(interval="1 day")

    longitude = models.DecimalField(max_digits=20, decimal_places=17)

    latitude = models.DecimalField(max_digits=20, decimal_places=17)

    # Properties

    # Altitude of the location in meters
    altitude = models.IntegerField(blank=True, null=True)

    # The arrival datetime of the visit
    arrival_date = models.DateTimeField()

    # The iPhone's battery level, between 0.00 and 1.00
    battery_level = models.DecimalField(max_digits=3, decimal_places=2)

    # The iPhone's battery state, it can be 'charging', 'full', 'unplugged', or 'unknown'
    battery_state = models.CharField(max_length=20)

    # The departure datetime of the visit
    # Is null when a visit is created and get's populated afterwards
    departure_date = models.DateTimeField()

    # The device id set in Overland settings or an empty string if not set
    device_id = models.CharField(max_length=50, blank=True)

    # The accuracy of the position in meters
    horizontal_accuracy = models.IntegerField()

    # The timestamp of the location
    # Set to the Timescale's time field
    # timestamp = models.DateTimeField()

    # The unique if if set
    unique_id = models.CharField(max_length=50, blank=True, null=True)

    # The vertical accuracy in meters
    vertical_accuracy = models.IntegerField(blank=True, null=True)

    # Wifi SSID if connected to a wifi network, an empty string if not connected
    wifi = models.CharField(max_length=100, blank=True)

    # Duration of the visit in hours
    # This is a calculated field and should not be set manually
    duration = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.arrival_date} - {self.departure_date} - {self.device_id}"

    def calculate_duration(self):
        """
        This function calculates the duration of the visit and returns it in seconds.
        """

        # Calculate the duration in seconds
        duration_seconds = (self.departure_date - self.arrival_date).seconds

        # Convert the seconds to hours
        duration_hours = duration_seconds / 3600

        # Round the value to 2 decimal places
        duration_hours = round(duration_hours, 2)

        return duration_hours

    # Modify the save method to calculate the duration
    def save(self, *args, **kwargs):
        """
        This function calculates the duration of the visit and saves it to the database.
        """
        # Calculate the duration
        self.duration = self.calculate_duration()

        # Call the parent's save method
        super().save(*args, **kwargs)
