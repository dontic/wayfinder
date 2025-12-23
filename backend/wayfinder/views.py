# views.py

import logging
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser as date_parser

# Django
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncDate


# ---------------------------------------------------------------------------- #
#                              PERFORMANCE SETTINGS                            #
# ---------------------------------------------------------------------------- #

# Maximum number of points to return in a single request
MAX_POINTS = 10000


def get_optimal_bucket_size(start_date, end_date, max_points=MAX_POINTS):
    """
    Calculate optimal time bucket size to return approximately max_points.
    Returns a TimescaleDB-compatible interval string.
    """
    date_range_seconds = (end_date - start_date).total_seconds()
    
    # Calculate bucket size in seconds to get approximately max_points
    bucket_seconds = date_range_seconds / max_points
    
    # Round to sensible intervals
    if bucket_seconds <= 1:
        return "1 second"  # No aggregation needed
    elif bucket_seconds < 60:
        return f"{max(1, int(bucket_seconds))} seconds"
    elif bucket_seconds < 300:
        return "1 minute"
    elif bucket_seconds < 900:
        return "5 minutes"
    elif bucket_seconds < 1800:
        return "15 minutes"
    elif bucket_seconds < 3600:
        return "30 minutes"
    elif bucket_seconds < 7200:
        return "1 hour"
    elif bucket_seconds < 21600:
        return "3 hours"
    elif bucket_seconds < 43200:
        return "6 hours"
    elif bucket_seconds < 86400:
        return "12 hours"
    else:
        return "1 day"


# REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
)

# Local App
from .models import Location, Visit
from .serializers import (
    ActivityHistoryResponseSerializer,
    ErrorResponseSerializer,
    LocationSerializer,
    TripPlotResponseSerializer,
    VisitPlotResponseSerializer,
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
        responses={
            200: VisitPlotResponseSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description="Endpoint for retrieving visit data as GeoJSON within a specified date range.",
    )
    def get(self, request):
        log.debug("Received request to get visits")

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

        # If visits is empty, return 404
        if visits_count == 0:
            log.debug("No visits found in the date range")
            return Response(
                {"message": "No visits found in the selected date range"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Convert the visits to a pandas dataframe
        visits_df = pd.DataFrame(list(visits.values()))

        # Build GeoJSON feature collection
        visits_collection = build_visits_feature_collection(visits_df)

        # Build response
        response_data = {
            "visits": visits_collection,
            "meta": {
                "start_datetime": start_date,
                "end_datetime": end_date,
                "visits_count": visits_count,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)


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
            OpenApiParameter(
                name="cursor",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="Pagination cursor (ISO datetime). Use the 'next_cursor' from previous response to get next page.",
                required=False,
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description=f"Number of points per page (default and max: {MAX_POINTS})",
                required=False,
            ),
            OpenApiParameter(
                name="no_bucket",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Disable time bucketing to get raw points (use with pagination for full data)",
                required=False,
            ),
        ],
        responses={
            200: TripPlotResponseSerializer,
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description="Endpoint for retrieving trip data as GeoJSON within a specified date range. Supports pagination for large datasets.",
    )
    def get(self, request):

        SHOW_VISITS = False
        SEPARATE_TRIPS = False
        DESIRED_ACCURACY = 0

        log.debug("Received request to get trips")

        # The request should always receive a date range
        # Otherwise, return an error
        start_date_str = request.query_params.get("start_datetime")
        end_date_str = request.query_params.get("end_datetime")

        if start_date_str is None or end_date_str is None:
            log.error("No date range provided")

            return Response(
                {"message": "Please provide a start_date and end_date query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse dates for bucket size calculation
        start_date_parsed = date_parser.parse(start_date_str)
        end_date_parsed = date_parser.parse(end_date_str)

        # Get the optional parameters
        if "show_visits" in request.query_params:
            SHOW_VISITS = request.query_params.get("show_visits").lower() == "true"
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

        # Pagination parameters
        cursor_str = request.query_params.get("cursor")
        cursor_datetime = None
        if cursor_str:
            try:
                cursor_datetime = date_parser.parse(cursor_str)
            except (ValueError, TypeError):
                return Response(
                    {"message": "Invalid cursor format. Use ISO datetime."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        page_size = MAX_POINTS
        if "page_size" in request.query_params:
            try:
                page_size = min(int(request.query_params.get("page_size")), MAX_POINTS)
                page_size = max(page_size, 1)  # At least 1
            except ValueError:
                page_size = MAX_POINTS

        # Whether to disable time bucketing (for pagination with raw data)
        NO_BUCKET = request.query_params.get("no_bucket", "").lower() == "true"

        # Build full range query for counting (always use full date range for counts)
        full_range_query = Location.objects.filter(
            time__range=[start_date_str, end_date_str]
        )

        # Apply accuracy filter at database level (more efficient)
        if DESIRED_ACCURACY > 0:
            full_range_query = full_range_query.filter(horizontal_accuracy__lte=DESIRED_ACCURACY)

        # Get total count for metadata (quick count query) - always for full range
        all_locations_count = full_range_query.count()
        log.debug(f"Found {all_locations_count} total locations in the date range")

        # If no locations at all, return empty response
        if all_locations_count == 0:
            log.debug("No locations found in the selected date range")
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        # Get non-stationary locations count for trip data (full range)
        full_trip_query = full_range_query.exclude(motion__contains="stationary").exclude(
            motion=[]
        )
        trip_locations_count = full_trip_query.count()
        log.debug(f"Found {trip_locations_count} trip locations")

        # Build paginated query - if cursor is provided, start from after the cursor time
        if cursor_datetime:
            trip_query = full_trip_query.filter(time__gt=cursor_datetime)
        else:
            trip_query = full_trip_query

        # Calculate optimal bucket size based on data volume (skip if pagination with raw data)
        if NO_BUCKET:
            bucket_size = None
            log.info(f"Time bucketing disabled, returning raw points (page_size={page_size})")
        else:
            bucket_size = get_optimal_bucket_size(
                start_date_parsed, end_date_parsed, page_size
            )
            log.info(f"Using time bucket: {bucket_size} for {trip_locations_count} points")

        # Apply time_bucket aggregation for efficient data retrieval (if enabled)
        # Only fetch required fields: time, longitude, latitude
        if bucket_size:
            trip_locations = trip_query.time_bucket(
                "time", bucket_size
            ).values(
                'time', 'longitude', 'latitude'
            ).order_by('time')[:page_size + 1]  # Fetch one extra to check for more
        else:
            # No bucketing - return raw points with pagination
            trip_locations = trip_query.only(
                'time', 'longitude', 'latitude'
            ).values(
                'time', 'longitude', 'latitude'
            ).order_by('time')[:page_size + 1]  # Fetch one extra to check for more

        # Convert to list efficiently (avoid pandas overhead for simple case)
        trip_locations_list = list(trip_locations)

        # Check if there are more results beyond this page
        has_more = len(trip_locations_list) > page_size
        if has_more:
            trip_locations_list = trip_locations_list[:page_size]  # Remove the extra item

        # Get the next cursor (timestamp of the last point)
        next_cursor = None
        if has_more and trip_locations_list:
            last_point = trip_locations_list[-1]
            next_cursor = last_point['time'].isoformat() if hasattr(last_point['time'], 'isoformat') else str(last_point['time'])
        
        # Convert to DataFrame only if needed for SEPARATE_TRIPS
        trip_locations_df = pd.DataFrame(trip_locations_list) if trip_locations_list else pd.DataFrame()

        def get_visits_df():
            log.debug("Getting visits dataframe")

            # Only fetch required fields for visits
            visits = Visit.objects.filter(
                time__range=[start_date_str, end_date_str]
            ).time_bucket("time", "1 day").only(
                'time', 'longitude', 'latitude', 'arrival_date', 
                'departure_date', 'horizontal_accuracy'
            ).values(
                'time', 'longitude', 'latitude', 'arrival_date',
                'departure_date', 'horizontal_accuracy'
            )
            visits_list = list(visits)
            visits_df = pd.DataFrame(visits_list) if visits_list else pd.DataFrame()

            visits_count = len(visits_list)
            log.debug(f"Found {visits_count} visits in the date range")

            return visits_df

        # Initialize visits_df
        visits_df = pd.DataFrame()

        # Get visits if needed (for SHOW_VISITS or SEPARATE_TRIPS)
        if SHOW_VISITS or SEPARATE_TRIPS:
            visits_df = get_visits_df()

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

        # Build response
        response_data = {
            "trips": trips_collection,
            "visits": visits_collection,
            "meta": {
                "start_datetime": start_date_str,
                "end_datetime": end_date_str,
                "total_locations": all_locations_count,
                "trip_locations": len(trip_locations_list),
                "trip_locations_raw": trip_locations_count,
                "visits_count": len(visits_df) if not visits_df.empty else 0,
                "trips_count": len(trips_collection["features"]),
                "separate_trips": SEPARATE_TRIPS,
                "show_visits": SHOW_VISITS,
                "bucket_size": bucket_size,
                "downsampled": bucket_size is not None and trip_locations_count > page_size,
            },
            "pagination": {
                "page_size": page_size,
                "has_more": has_more,
                "next_cursor": next_cursor,
                "is_first_page": cursor_datetime is None,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ActivityHistoryView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        responses={
            200: ActivityHistoryResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description="Endpoint for retrieving the count of locations and visits per day for the past 365 days.",
    )
    def get(self, request):
        log.debug("Received request to get activity history")

        # Calculate date range: past 365 days from today
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)

        log.debug(f"Querying data from {start_date} to {end_date}")

        # Query locations grouped by date
        locations_by_date = (
            Location.objects.filter(time__date__gte=start_date, time__date__lte=end_date)
            .annotate(date=TruncDate("time"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        # Query visits grouped by date
        visits_by_date = (
            Visit.objects.filter(time__date__gte=start_date, time__date__lte=end_date)
            .annotate(date=TruncDate("time"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        # Convert to dictionaries for easy lookup
        locations_dict = {item["date"]: item["count"] for item in locations_by_date}
        visits_dict = {item["date"]: item["count"] for item in visits_by_date}

        log.debug(f"Found data for {len(locations_dict)} days with locations")
        log.debug(f"Found data for {len(visits_dict)} days with visits")

        # Build the data array with all dates in the range
        data = []
        current_date = start_date
        total_locations = 0
        total_visits = 0

        while current_date <= end_date:
            location_count = locations_dict.get(current_date, 0)
            visit_count = visits_dict.get(current_date, 0)
            
            total_locations += location_count
            total_visits += visit_count

            data.append({
                "date": current_date.isoformat(),
                "location_count": location_count,
                "visit_count": visit_count,
            })

            current_date += timedelta(days=1)

        # Check if there's any data at all
        if total_locations == 0 and total_visits == 0:
            log.debug("No activity data found in the past 365 days")
            return Response(
                {"message": "No activity data found in the past 365 days"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Build response
        response_data = {
            "data": data,
            "meta": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": len(data),
                "total_locations": total_locations,
                "total_visits": total_visits,
            },
        }

        log.info(
            f"Returning activity history: {len(data)} days, "
            f"{total_locations} locations, {total_visits} visits"
        )

        return Response(response_data, status=status.HTTP_200_OK)
