# serializers.py

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

        # Extract data from the GeoJSON structure
        properties = data.get("properties", {})
        geometry = data.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

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
            "device_id": properties.get("device_id"),
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

        # Extract data from the GeoJSON structure
        properties = data.get("properties", {})
        geometry = data.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

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
            "device_id": properties.get("device_id"),
            "horizontal_accuracy": properties.get("horizontal_accuracy"),
            "unique_id": properties.get("unique_id"),
            "vertical_accuracy": properties.get("vertical_accuracy"),
            "wifi": properties.get("wifi"),
        }

        # Use the parent's to_internal_value to do the actual validation
        return super().to_internal_value(prepared_data)
