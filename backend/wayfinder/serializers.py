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


# ------------------------- Visits Plotly serializers ------------------------ #
class VisitPlotlyDataSerializer(serializers.Serializer):
    coloraxis = serializers.CharField()
    customdata = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField())
    )
    hovertemplate = serializers.CharField()
    lat = serializers.ListField(child=serializers.FloatField())
    lon = serializers.ListField(child=serializers.FloatField())
    name = serializers.CharField()
    subplot = serializers.CharField()
    z = serializers.ListField(child=serializers.IntegerField())
    type = serializers.CharField()


class VisitPlotlyLayoutSerializer(serializers.Serializer):
    mapbox = serializers.DictField()
    coloraxis = serializers.DictField()
    legend = serializers.DictField()
    margin = serializers.DictField()
    template = serializers.DictField()


class VisitPlotlyResponseSerializer(serializers.Serializer):
    data = serializers.ListField(child=VisitPlotlyDataSerializer())
    layout = VisitPlotlyLayoutSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
