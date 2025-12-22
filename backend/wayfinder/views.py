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
from wayfinder.utils import color_trips, remove_locations_during_visit

# Local App
from .models import Location, Visit
from .serializers import (
    ErrorResponseSerializer,
    LocationSerializer,
    VisitPlotlyResponseSerializer,
    VisitSerializer,
)
from .filters import LocationFilterSet, VisitFilterSet

# Plotly
# Plotly imports
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder


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


# This viewset is not necessary
class LocationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    authentication_classes = [BearerTokenAuthentication]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LocationFilterSet


# This viewset is not necessary
class VisitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    authentication_classes = [SessionAuthentication]

    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VisitFilterSet


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
                description="Flag to indicate if visits should be shown on the plot",
                required=False,
            ),
            OpenApiParameter(
                name="show_stationary",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if stationary locations should be shown on the plot",
                required=False,
            ),
            OpenApiParameter(
                name="color_trips",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if trips should be colored",
                required=False,
            ),
            OpenApiParameter(
                name="locations_during_visits",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Flag to indicate if locations during visits should be removed",
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
        responses={200: VisitPlotlyResponseSerializer, 400: ErrorResponseSerializer},
        description="Endpoint for generating a path plot of trips within a specified date range.",
    )
    def get(self, request):

        SHOW_STATIONARY = False
        SHOW_VISITS = False
        COLOR_TRIPS = False
        LOCATIONS_DURING_VISITS = False
        DESIRED_ACCURACY = 0

        log.debug("Received request to plot trips")

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
        if "color_trips" in request.query_params:
            COLOR_TRIPS = request.query_params.get("color_trips").lower() == "true"
        if "locations_during_visits" in request.query_params:
            LOCATIONS_DURING_VISITS = (
                request.query_params.get("locations_during_visits").lower() == "true"
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

        # Get the locations in the date range
        locations = Location.objects.filter(
            time__range=[start_date, end_date]
        ).time_bucket("time", "1 day")

        if not SHOW_STATIONARY:
            # Exclude the locations where motion = ["stationary"]
            # Note that motion can be ["driving", "stationary"]
            # We only want to exclude the fully stationary locations
            locations = locations.exclude(motion__contains="stationary").exclude(
                motion=[]
            )

        locations_count = locations.count()

        log.debug(f"Found {locations_count} locations in the date range")

        # If locations is empty, return an empty response
        if locations_count == 0:
            log.debug("No locations found in the selected date range")
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        # Convert the locations to a pandas dataframe
        locations_df = pd.DataFrame(list(locations.values()))

        def get_visits_df():
            log.debug("Getting visits dataframe")

            visits = Visit.objects.filter(
                time__range=[start_date, end_date]
            ).time_bucket("time", "1 day")
            visits_df = pd.DataFrame(list(visits.values()))

            visits_count = visits_df.shape[0]

            log.debug(f"Found {visits_count} visits in the date range")

            return visits_df

        # Initialize visits_df and generated variable
        visits_df = pd.DataFrame()
        visits_df_generated = False

        # Get the visits if the SHOW_VISITS flag is set
        if SHOW_VISITS:
            log.debug("Showing visits")
            visits_df = get_visits_df()
            visits_df_generated = True

        if COLOR_TRIPS:
            log.debug("Coloring trips")

            # Get the visits_df if it is empty
            if visits_df.empty and not visits_df_generated:
                visits_df = get_visits_df()
                visits_df_generated = True

            # Generate a "color" column in the locations_df
            locations_df = color_trips(locations_df, visits_df)
        else:
            # Generate a "color" column with NaN values
            locations_df["color"] = None

        if not LOCATIONS_DURING_VISITS:
            log.debug("Removing locations during visits")

            # Get the visits_df if it is empty
            if visits_df.empty and not visits_df_generated:
                visits_df = get_visits_df()
                visits_df_generated = True

            # Remove locations during visits
            locations_df = remove_locations_during_visit(locations_df, visits_df)

        if DESIRED_ACCURACY > 0:
            log.debug(f"Filtering locations with accuracy < {DESIRED_ACCURACY}")
            locations_df = locations_df[
                locations_df["horizontal_accuracy"] <= DESIRED_ACCURACY
            ]

        # Plot the trips
        fig = px.line_mapbox(
            locations_df,
            lat="latitude",
            lon="longitude",
            hover_data=["speed", "time", "motion"],
            zoom=8,
            color="color",
        )

        # Add visits waypoints
        if SHOW_VISITS and not visits_df.empty:
            fig.add_trace(
                go.Scattermapbox(
                    lat=visits_df["latitude"],
                    lon=visits_df["longitude"],
                    mode="markers",
                    marker=go.scattermapbox.Marker(
                        size=25, color="RoyalBlue", opacity=0.7
                    ),
                    hoverinfo="none",
                )
            )

        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(showlegend=False)

        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

        # GraphJSON is a json string, so you have to parse it into a json object
        # in order to return it
        parsed_graphJSON = json.loads(graphJSON)

        return Response(parsed_graphJSON, status=status.HTTP_200_OK)
