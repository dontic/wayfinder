from rest_framework import serializers

from .models import Location, Visit


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"


class FrontentVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            "coordinates_longitude",
            "coordinates_latitude",
            "arrival_datetime",
            "departure_datetime",
        ]
        depth = 1
