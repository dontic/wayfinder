# views.py

import logging

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.db import transaction

from wayfinder.models import Location, Visit

from .serializers import LocationSerializer, VisitSerializer, OverlandSerializer

log = logging.getLogger("app_logger")


class OverlandView(APIView):

    permission_classes = []

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                "Request Example",
                value={
                    "locations": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [-4.2838405, 38.665856],
                            },
                            "properties": {
                                "speed": -1,
                                "battery_state": "unplugged",
                                "motion": ["stationary"],
                                "timestamp": "2024-09-13T11:33:33Z",
                                "horizontal_accuracy": 3000,
                                "speed_accuracy": -1,
                                "vertical_accuracy": 30,
                                "battery_level": 0.75,
                                "wifi": "",
                                "course": -1,
                                "device_id": "iphone",
                                "altitude": 8,
                                "course_accuracy": -1,
                            },
                        },
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [-4.2702682, 38.6637597],
                            },
                            "properties": {
                                "arrival_date": "2024-09-13T11:33:35Z",
                                "departure_date": "",
                                "battery_state": "unplugged",
                                "timestamp": "2024-09-13T11:33:35Z",
                                "horizontal_accuracy": 3000,
                                "vertical_accuracy": 30,
                                "battery_level": 0.75,
                                "wifi": "",
                                "device_id": "iphone",
                                "altitude": 8,
                            },
                        },
                    ]
                },
                request_only=True,
            ),
            OpenApiExample(
                "Success Response",
                value={"result": "ok"},
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Error Response",
                value={"result": "not_ok"},
                response_only=True,
                status_codes=["500"],
            ),
        ],
        description="Endpoint for receiving and storing location and visit data from Overland app.",
    )
    def post(self, request):

        # Extract the list of locations
        locations_data = request.data.get("locations", [])
        log.info(f"Received {len(locations_data)} locations")
        log.debug(locations_data)

        locations_to_create = []
        visits_to_create = []

        for item in locations_data:
            if "arrival_date" in item.get("properties", {}):
                # This is a visit
                visit_serializer = VisitSerializer(data=item)
                if visit_serializer.is_valid():
                    visits_to_create.append(Visit(**visit_serializer.validated_data))
                else:
                    # Log validation errors
                    log.error(f"Visit validation error: {visit_serializer.errors}")
                    log.info(f"Visit data: {item}")
            else:
                location_serializer = LocationSerializer(data=item)
                if location_serializer.is_valid():
                    locations_to_create.append(
                        Location(**location_serializer.validated_data)
                    )
                else:
                    # Log validation errors
                    log.error(
                        f"Location validation error: {location_serializer.errors}"
                    )
                    log.info(f"Location data: {item}")

        log.info(f"Parsed {len(locations_to_create)} locations")
        log.info(f"Parsed {len(visits_to_create)} visits")

        try:
            with transaction.atomic():
                Location.objects.bulk_create(locations_to_create)
                Visit.objects.bulk_create(visits_to_create)
        except Exception as e:
            # Log the error
            log.error(f"Error saving data: {str(e)}")

            return Response(
                {"result": "not_ok"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        log.info("Data saved successfully")
        return Response({"result": "ok"}, status=status.HTTP_200_OK)
