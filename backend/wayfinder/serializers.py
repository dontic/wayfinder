# serializers.py

from datetime import datetime
from rest_framework import serializers

from .models import Location, Visit


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "time",
            "longitude",
            "latitude",
            "altitude",
            "battery_level",
            "battery_state",
            "course",
            "course_accuracy",
            "device_id",
            "horizontal_accuracy",
            "motion",
            "speed",
            "speed_accuracy",
            "unique_id",
            "vertical_accuracy",
            "wifi",
        ]

    def to_internal_value(self, data):
        """
        This function transforms the GeoJSON data received by Overland
        into a format that the serializer can understand so it can then
        be saved into the database.
        """

        # Validate that data is a dictionary
        if not isinstance(data, dict):
            raise serializers.ValidationError(
                "Invalid data format: expected a dictionary"
            )

        # Extract data from the GeoJSON structure
        properties = data.get("properties", {})
        geometry = data.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        # Validate GeoJSON structure
        if not isinstance(properties, dict):
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'properties' must be a dictionary"
            )

        if not isinstance(geometry, dict):
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'geometry' must be a dictionary"
            )

        # Validate coordinates
        if not isinstance(coordinates, list) or len(coordinates) < 2:
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'coordinates' must be a list with at least 2 elements [longitude, latitude]"
            )

        # Prepare the data for the serializer
        prepared_data = {
            "time": properties.get("timestamp"),
            "longitude": coordinates[0] if len(coordinates) > 0 else None,
            "latitude": coordinates[1] if len(coordinates) > 1 else None,
            "altitude": properties.get("altitude"),
            "battery_level": properties.get("battery_level"),
            "battery_state": properties.get("battery_state"),
            "course": properties.get("course"),
            "course_accuracy": properties.get("course_accuracy"),
            "device_id": properties.get("device_id") or "",
            "horizontal_accuracy": properties.get("horizontal_accuracy"),
            "motion": properties.get("motion"),
            "speed": properties.get("speed"),
            "speed_accuracy": properties.get("speed_accuracy"),
            "unique_id": properties.get("unique_id"),
            "vertical_accuracy": properties.get("vertical_accuracy"),
            "wifi": properties.get("wifi"),
        }

        # Use the parent's to_internal_value to do the actual validation
        return super().to_internal_value(prepared_data)

    def validate_longitude(self, value):
        """Validate longitude is within valid range"""
        if value is None:
            raise serializers.ValidationError("Longitude is required")
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees"
            )
        return value

    def validate_latitude(self, value):
        """Validate latitude is within valid range"""
        if value is None:
            raise serializers.ValidationError("Latitude is required")
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees"
            )
        return value

    def validate_battery_level(self, value):
        """Validate battery level is between 0.00 and 1.00"""
        if value is None:
            raise serializers.ValidationError("Battery level is required")
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                "Battery level must be between 0.00 and 1.00"
            )
        return value

    def validate_battery_state(self, value):
        """Validate battery state is one of the valid options"""
        valid_states = ["charging", "full", "unplugged", "unknown"]
        if not value:
            raise serializers.ValidationError("Battery state is required")
        if value not in valid_states:
            raise serializers.ValidationError(
                f"Battery state must be one of: {', '.join(valid_states)}"
            )
        return value

    def validate_motion(self, value):
        """Validate motion is a list"""
        if value is None:
            raise serializers.ValidationError("Motion field is required")
        if not isinstance(value, list):
            raise serializers.ValidationError("Motion must be a list")

        valid_motions = ["driving", "walking", "running", "cycling", "stationary"]
        for motion in value:
            if motion not in valid_motions:
                raise serializers.ValidationError(
                    f"Invalid motion type '{motion}'. Must be one of: {', '.join(valid_motions)}"
                )
        return value

    def validate_time(self, value):
        """Validate timestamp is present"""
        if value is None:
            raise serializers.ValidationError("Timestamp is required")
        return value


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            "time",
            "longitude",
            "latitude",
            "altitude",
            "arrival_date",
            "battery_level",
            "battery_state",
            "departure_date",
            "device_id",
            "horizontal_accuracy",
            "unique_id",
            "vertical_accuracy",
            "wifi",
            "duration",
        ]

    def to_internal_value(self, data):
        """
        This function transforms the GeoJSON data received by Overland
        into a format that the serializer can understand so it can then
        be saved into the database.
        """

        # Validate that data is a dictionary
        if not isinstance(data, dict):
            raise serializers.ValidationError(
                "Invalid data format: expected a dictionary"
            )

        # Extract data from the GeoJSON structure
        properties = data.get("properties", {})
        geometry = data.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        # Validate GeoJSON structure
        if not isinstance(properties, dict):
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'properties' must be a dictionary"
            )

        if not isinstance(geometry, dict):
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'geometry' must be a dictionary"
            )

        # Validate coordinates
        if not isinstance(coordinates, list) or len(coordinates) < 2:
            raise serializers.ValidationError(
                "Invalid GeoJSON: 'coordinates' must be a list with at least 2 elements [longitude, latitude]"
            )

        # Calculate the duration of the visit
        arrival_date = properties.get("arrival_date")
        departure_date = properties.get("departure_date")

        # Validate that both dates are present
        if not arrival_date:
            raise serializers.ValidationError("arrival_date is required for visits")
        if not departure_date:
            raise serializers.ValidationError("departure_date is required for visits")

        if arrival_date and departure_date:
            try:
                # Convert the dates to datetime objects
                arrival_datetime = datetime.strptime(arrival_date, "%Y-%m-%dT%H:%M:%SZ")
                departure_datetime = datetime.strptime(
                    departure_date, "%Y-%m-%dT%H:%M:%SZ"
                )
            except ValueError as e:
                raise serializers.ValidationError(
                    f"Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SSZ. Error: {str(e)}"
                )

            # Validate that departure is after arrival
            if departure_datetime <= arrival_datetime:
                raise serializers.ValidationError(
                    "departure_date must be after arrival_date"
                )

            # Calculate the duration in seconds
            duration = (departure_datetime - arrival_datetime).total_seconds()

            # Convert the duration to hours
            properties["duration"] = duration / 3600

            # Ensure duration has 2 decimal places
            properties["duration"] = round(properties["duration"], 2)

            # Validate duration is positive
            if properties["duration"] <= 0:
                raise serializers.ValidationError("Visit duration must be positive")

        # Prepare the data for the serializer
        prepared_data = {
            "time": properties.get("timestamp"),
            "longitude": coordinates[0] if len(coordinates) > 0 else None,
            "latitude": coordinates[1] if len(coordinates) > 1 else None,
            "altitude": properties.get("altitude"),
            "arrival_date": properties.get("arrival_date"),
            "battery_level": properties.get("battery_level"),
            "battery_state": properties.get("battery_state"),
            "departure_date": properties.get("departure_date") or None,
            "device_id": properties.get("device_id") or "",
            "horizontal_accuracy": properties.get("horizontal_accuracy"),
            "unique_id": properties.get("unique_id"),
            "vertical_accuracy": properties.get("vertical_accuracy"),
            "wifi": properties.get("wifi"),
            "duration": properties.get("duration"),
        }

        # Use the parent's to_internal_value to do the actual validation
        return super().to_internal_value(prepared_data)

    def validate_longitude(self, value):
        """Validate longitude is within valid range"""
        if value is None:
            raise serializers.ValidationError("Longitude is required")
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees"
            )
        return value

    def validate_latitude(self, value):
        """Validate latitude is within valid range"""
        if value is None:
            raise serializers.ValidationError("Latitude is required")
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees"
            )
        return value

    def validate_battery_level(self, value):
        """Validate battery level is between 0.00 and 1.00"""
        if value is None:
            raise serializers.ValidationError("Battery level is required")
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                "Battery level must be between 0.00 and 1.00"
            )
        return value

    def validate_battery_state(self, value):
        """Validate battery state is one of the valid options"""
        valid_states = ["charging", "full", "unplugged", "unknown"]
        if not value:
            raise serializers.ValidationError("Battery state is required")
        if value not in valid_states:
            raise serializers.ValidationError(
                f"Battery state must be one of: {', '.join(valid_states)}"
            )
        return value

    def validate_time(self, value):
        """Validate timestamp is present"""
        if value is None:
            raise serializers.ValidationError("Timestamp is required")
        return value

    def validate(self, data):
        """
        Object-level validation to ensure arrival_date is before departure_date
        """
        arrival = data.get("arrival_date")
        departure = data.get("departure_date")

        if arrival and departure and departure <= arrival:
            raise serializers.ValidationError(
                "departure_date must be after arrival_date"
            )

        return data


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


# ------------------------- Trip Plot serializers ---------------------------- #
class GeoJSONGeometrySerializer(serializers.Serializer):
    type = serializers.CharField(help_text="GeoJSON geometry type (e.g., 'Point', 'LineString')")
    coordinates = serializers.ListField(
        help_text="Coordinates array - format depends on geometry type"
    )


class GeoJSONFeatureSerializer(serializers.Serializer):
    type = serializers.CharField(default="Feature", help_text="Always 'Feature'")
    geometry = GeoJSONGeometrySerializer()
    properties = serializers.DictField(
        help_text="Feature properties (varies by feature type)"
    )


class GeoJSONFeatureCollectionSerializer(serializers.Serializer):
    type = serializers.CharField(
        default="FeatureCollection", help_text="Always 'FeatureCollection'"
    )
    features = serializers.ListField(
        child=GeoJSONFeatureSerializer(),
        help_text="Array of GeoJSON Feature objects",
    )


class VisitPlotMetaSerializer(serializers.Serializer):
    start_datetime = serializers.CharField(help_text="Start datetime of the query range")
    end_datetime = serializers.CharField(help_text="End datetime of the query range")
    visits_count = serializers.IntegerField(help_text="Number of visits in range")


class VisitPlotResponseSerializer(serializers.Serializer):
    visits = GeoJSONFeatureCollectionSerializer(
        help_text="GeoJSON FeatureCollection containing visit Point features"
    )
    meta = VisitPlotMetaSerializer(help_text="Metadata about the query and results")


class TripPlotMetaSerializer(serializers.Serializer):
    start_datetime = serializers.CharField(help_text="Start datetime of the query range")
    end_datetime = serializers.CharField(help_text="End datetime of the query range")
    total_locations = serializers.IntegerField(help_text="Total number of locations in range")
    trip_locations = serializers.IntegerField(help_text="Number of non-stationary locations in current page")
    trip_locations_raw = serializers.IntegerField(help_text="Total number of trip locations without pagination")
    visits_count = serializers.IntegerField(help_text="Number of visits in range")
    trips_count = serializers.IntegerField(help_text="Number of trip segments")
    separate_trips = serializers.BooleanField(help_text="Whether trips were separated by visits")
    show_visits = serializers.BooleanField(help_text="Whether visits are included")
    bucket_size = serializers.CharField(
        allow_null=True, 
        help_text="Time bucket size used for downsampling (e.g., '1 hour', '15 minutes')"
    )
    downsampled = serializers.BooleanField(help_text="Whether the data was downsampled")


class PaginationSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(help_text="Number of points per page")
    has_more = serializers.BooleanField(help_text="Whether there are more pages available")
    next_cursor = serializers.CharField(
        allow_null=True,
        help_text="Cursor for the next page (ISO datetime). Use this in the 'cursor' query parameter."
    )
    is_first_page = serializers.BooleanField(help_text="Whether this is the first page")


class TripPlotResponseSerializer(serializers.Serializer):
    trips = GeoJSONFeatureCollectionSerializer(
        help_text="GeoJSON FeatureCollection containing trip LineString features"
    )
    visits = GeoJSONFeatureCollectionSerializer(
        help_text="GeoJSON FeatureCollection containing visit Point features"
    )
    meta = TripPlotMetaSerializer(help_text="Metadata about the query and results")
    pagination = PaginationSerializer(help_text="Pagination information for navigating through large datasets")


# ------------------------- Activity History serializers --------------------- #
class DailyActivitySerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Date in YYYY-MM-DD format")
    location_count = serializers.IntegerField(help_text="Number of locations recorded on this date")
    visit_count = serializers.IntegerField(help_text="Number of visits recorded on this date")


class ActivityHistoryMetaSerializer(serializers.Serializer):
    start_date = serializers.DateField(help_text="Start date of the data range")
    end_date = serializers.DateField(help_text="End date of the data range")
    days = serializers.IntegerField(help_text="Number of days in the range")
    total_locations = serializers.IntegerField(help_text="Total number of locations in the range")
    total_visits = serializers.IntegerField(help_text="Total number of visits in the range")


class ActivityHistoryResponseSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=DailyActivitySerializer(),
        help_text="Array of daily activity data"
    )
    meta = ActivityHistoryMetaSerializer(help_text="Metadata about the activity history")
