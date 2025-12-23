# views.py

import logging
import json
import pandas as pd

# Django
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend


# REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Spectacular
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Utils
from wayfinder.utils import (
    build_trips_feature_collection,
    build_visits_feature_collection,
    build_stationary_feature_collection,
)

# Plotly imports (used by VisitPlotView)
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# Local App
from .models import Location, Visit
from .serializers import (
    ErrorResponseSerializer,
    LocationSerializer,
    VisitPlotlyResponseSerializer,
    VisitSerializer,
)


log = logging.getLogger(__name__)


# Subclassing TokenAuthentication to accept Bearer instead of Token as the keyword
class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class OverlandView(APIView):

    authentication_classes = [BearerTokenAuthentication]

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

        # Log the token
        log.debug(f"Received token: {request.auth}")

        # Extract the list of locations
        locations_data = request.data.get("locations", [])
        log.info(f"Received {len(locations_data)} locations")
        log.debug(locations_data)

        locations_to_create = []
        visits_to_create = []

        # Use sets to keep track of unique timestamps
        unique_location_timestamps = set()
        unique_visit_timestamps = set()

        for item in locations_data:
            if "arrival_date" in item.get("properties", {}):

                # If there is no departure date, skip the visit
                departure_date = item.get("properties", {}).get("departure_date")
                if departure_date is None or departure_date == "":
                    log.debug("Skipping visit without valid departure date")
                    log.debug(f"Visit data: {item}")
                    continue

                # This is a visit
                visit_serializer = VisitSerializer(data=item)

                if visit_serializer.is_valid():
                    visit_timestamp = visit_serializer.validated_data.get("time")
                    if visit_timestamp not in unique_visit_timestamps:
                        unique_visit_timestamps.add(visit_timestamp)
                        visits_to_create.append(
                            Visit(**visit_serializer.validated_data)
                        )
                    else:
                        log.debug(
                            f"Skipping duplicate visit with time: {visit_timestamp}"
                        )
                else:
                    # Check if the error is due to a duplicate visit
                    if "time" in visit_serializer.errors and any(
                        error.code == "unique"
                        for error in visit_serializer.errors["time"]
                    ):
                        log.debug(
                            f"Skipping duplicate visit: {item.get('time', 'unknown time')}"
                        )
                    else:
                        log.error(f"Visit validation error: {visit_serializer.errors}")
                        log.info(f"Visit data: {item}")
            else:
                location_serializer = LocationSerializer(data=item)
                if location_serializer.is_valid():
                    location_timestamp = location_serializer.validated_data.get("time")
                    if location_timestamp not in unique_location_timestamps:
                        unique_location_timestamps.add(location_timestamp)
                        locations_to_create.append(
                            Location(**location_serializer.validated_data)
                        )
                    else:
                        log.debug(
                            f"Skipping duplicate location with time: {location_timestamp}"
                        )
                else:
                    # Check if the error is due to a duplicate location
                    if "time" in location_serializer.errors and any(
                        error.code == "unique"
                        for error in location_serializer.errors["time"]
                    ):
                        log.debug(
                            f"Skipping duplicate location: {item.get('time', 'unknown time')}"
                        )
                    else:
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


class TokenView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        summary="Get or regenerate authentication token",
        description="This endpoint gets or creates a new token for the authenticated user or regenerates an existing one if requested.",
        parameters=[
            OpenApiParameter(
                name="recreate",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Boolean flag to indicate if the token should be regenerated",
                required=False,
            ),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
                    }
                },
            },
            401: {},
        },
    )
    def get(self, request, *args, **kwargs):

        # Get the authenticated user
        user = request.user

        # Get the recreate parameter
        # recreate can be "true" or "false"
        recreate = request.query_params.get("recreate", "false").lower() == "true"

        # Get or create the token
        token, created = Token.objects.get_or_create(user=user)

        # If the token already exists and the recreate parameter is set to True, delete the token and create a new one
        if not created and recreate:
            print("Deleting token")
            token.delete()
            print("Creating new token")
            token = Token.objects.create(user=user)

        return Response({"token": token.key})


class VisitPlotView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_datetime",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Start date for the date range filter (inclusive)",
                required=True,
            ),
            OpenApiParameter(
                name="end_datetime",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="End date for the date range filter (inclusive)",
                required=True,
            ),
        ],
        responses={200: VisitPlotlyResponseSerializer, 400: ErrorResponseSerializer},
        description="Endpoint for generating a density map of visits within a specified date range.",
    )
    def get(self, request):
        log.debug("Received request to plot visits")

        # The request should always receive a date range
        # Otherwise, return an error
        start_date = request.query_params.get("start_datetime")
        end_date = request.query_params.get("end_datetime")

        if start_date is None or end_date is None:
            log.error("No date range provided")
            return Response(
                {"message": "Please provide a start_date and end_date query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the visits in the date range
        visits = Visit.objects.filter(time__range=[start_date, end_date]).time_bucket(
            "time", "1 day"
        )

        visits_count = visits.count()

        log.debug(f"Found {visits_count} visits in the date range")

        # If visists is empty, return an empty response
        if visits_count == 0:
            log.debug("No visits found in the date range")
            return Response({}, status=status.HTTP_200_OK)

        # Convert the visits to a pandas dataframe
        visits = pd.DataFrame(list(visits.values()))

        # Plot the visits
        fig = px.density_mapbox(
            visits,
            lat="latitude",
            lon="longitude",
            z="duration",
            hover_data=["arrival_date", "departure_date"],
            zoom=1,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(coloraxis_showscale=False)

        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

        # GraphJSON is a json string, so you have to parse it into a json object
        # in order to return it
        parsed_graphJSON = json.loads(graphJSON)

        return Response(parsed_graphJSON, status=status.HTTP_200_OK)


class TripPlotView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_datetime",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Start date for the date range filter (inclusive)",
                required=True,
            ),
            OpenApiParameter(
                name="end_datetime",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="End date for the date range filter (inclusive)",
                required=True,
            ),
            OpenApiParameter(
                name="show_visits",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if visits should be included in the response",
                required=False,
            ),
            OpenApiParameter(
                name="show_stationary",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if stationary locations should be included in the response",
                required=False,
            ),
            OpenApiParameter(
                name="separate_trips",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if trips should be segmented by visit midtimes",
                required=False,
            ),
            OpenApiParameter(
                name="desired_accuracy",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description="Desired accuracy in meters. 0 means no filtering",
                required=False,
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: ErrorResponseSerializer,
            404: OpenApiTypes.OBJECT,
        },
        description="Endpoint for retrieving trip data as GeoJSON within a specified date range.",
    )
    def get(self, request):

        SHOW_STATIONARY = False
        SHOW_VISITS = False
        SEPARATE_TRIPS = False
        DESIRED_ACCURACY = 0

        log.debug("Received request to get trips")

        # The request should always receive a date range
        # Otherwise, return an error
        start_date = request.query_params.get("start_datetime")
        end_date = request.query_params.get("end_datetime")

        if start_date is None or end_date is None:
            log.error("No date range provided")

            return Response(
                {"message": "Please provide a start_date and end_date query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the optional parameters
        if "show_visits" in request.query_params:
            SHOW_VISITS = request.query_params.get("show_visits").lower() == "true"
        if "show_stationary" in request.query_params:
            SHOW_STATIONARY = (
                request.query_params.get("show_stationary").lower() == "true"
            )
        if "separate_trips" in request.query_params:
            SEPARATE_TRIPS = (
                request.query_params.get("separate_trips").lower() == "true"
            )
        if "desired_accuracy" in request.query_params:
            DESIRED_ACCURACY = request.query_params.get("desired_accuracy")
            # Ensure that the desired accuracy is a number
            try:
                DESIRED_ACCURACY = float(DESIRED_ACCURACY)
            except ValueError:
                log.error("Desired accuracy is not a number")
                return Response(
                    {"message": "Desired accuracy must be a number"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Get all locations in the date range (including stationary for potential use)
        all_locations = Location.objects.filter(
            time__range=[start_date, end_date]
        ).time_bucket("time", "1 day")

        all_locations_count = all_locations.count()
        log.debug(f"Found {all_locations_count} total locations in the date range")

        # If no locations at all, return empty response
        if all_locations_count == 0:
            log.debug("No locations found in the selected date range")
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        # Convert all locations to dataframe for stationary extraction
        all_locations_df = pd.DataFrame(list(all_locations.values()))

        # Get non-stationary locations for trips
        trip_locations = all_locations.exclude(motion__contains="stationary").exclude(
            motion=[]
        )
        trip_locations_df = (
            pd.DataFrame(list(trip_locations.values()))
            if trip_locations.exists()
            else pd.DataFrame()
        )

        def get_visits_df():
            log.debug("Getting visits dataframe")

            visits = Visit.objects.filter(
                time__range=[start_date, end_date]
            ).time_bucket("time", "1 day")
            visits_df = pd.DataFrame(list(visits.values()))

            visits_count = visits_df.shape[0] if not visits_df.empty else 0

            log.debug(f"Found {visits_count} visits in the date range")

            return visits_df

        # Initialize visits_df
        visits_df = pd.DataFrame()

        # Get visits if needed (for SHOW_VISITS or SEPARATE_TRIPS)
        if SHOW_VISITS or SEPARATE_TRIPS:
            visits_df = get_visits_df()

        # Apply accuracy filter
        if DESIRED_ACCURACY > 0 and not trip_locations_df.empty:
            log.debug(f"Filtering locations with accuracy <= {DESIRED_ACCURACY}")
            trip_locations_df = trip_locations_df[
                trip_locations_df["horizontal_accuracy"] <= DESIRED_ACCURACY
            ]

        # Build GeoJSON feature collections
        trips_collection = build_trips_feature_collection(
            trip_locations_df,
            visits_df if SEPARATE_TRIPS else pd.DataFrame(),
            separate_trips=SEPARATE_TRIPS,
        )
        visits_collection = (
            build_visits_feature_collection(visits_df)
            if SHOW_VISITS
            else {"type": "FeatureCollection", "features": []}
        )
        stationary_collection = (
            build_stationary_feature_collection(all_locations_df)
            if SHOW_STATIONARY
            else {"type": "FeatureCollection", "features": []}
        )

        # Build response
        response_data = {
            "trips": trips_collection,
            "visits": visits_collection,
            "stationary": stationary_collection,
            "meta": {
                "start_datetime": start_date,
                "end_datetime": end_date,
                "total_locations": all_locations_count,
                "trip_locations": (
                    len(trip_locations_df) if not trip_locations_df.empty else 0
                ),
                "visits_count": len(visits_df) if not visits_df.empty else 0,
                "stationary_count": len(stationary_collection["features"]),
                "trips_count": len(trips_collection["features"]),
                "separate_trips": SEPARATE_TRIPS,
                "show_visits": SHOW_VISITS,
                "show_stationary": SHOW_STATIONARY,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)
