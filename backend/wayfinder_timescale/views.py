import os
import dotenv

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import LocationSerializer, VisitSerializer

# Load the .env file
dotenv.load_dotenv()


class OverlandView(APIView):
    # Make the view public
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        # Get the authorization header
        # The authorization header is expected to be in the format:
        # "Bearer <token>"
        auth_header = request.headers.get("Authorization")

        # Extract the token
        token = auth_header.split(" ")[1]

        # Check if the token is valid
        verification_token = os.getenv("OVERLAND_VERIFICATION_TOKEN", "overlandtoken")
        if token != verification_token:
            return Response(
                {"result": "Token not valid"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Get the locations list
        overland_locations = request.data.get("locations")

        # To see which formats locatons can have, check the locations_format_examples.json file
        # or the Overland API documentation https://github.com/aaronpk/Overland-iOS/blob/main/README.md

        # Print the number of locations
        print(f"Saving {len(overland_locations)} locations to the database...")

        # Initialize the lists
        trips = []
        visits = []
        locations = []

        # For every location save it to the database
        for overland_location in overland_locations:
            # Trip case
            if "start" in overland_location["properties"]:
                # TODO: Save the trip to the database
                print("Location is a trip, skipping...")
                print(overland_location)
                continue

            # Visit case
            if "arrival_date" in overland_location["properties"]:
                # Try to parse the visit
                try:
                    clean_data = {}
                    clean_data["type"] = overland_location["type"]
                    clean_data["geometry_type"] = overland_location["geometry"]["type"]
                    clean_data["coordinates_longitude"] = overland_location["geometry"][
                        "coordinates"
                    ][0]
                    clean_data["coordinates_latitude"] = overland_location["geometry"][
                        "coordinates"
                    ][1]
                    clean_data["action"] = overland_location["properties"]["action"]
                    clean_data["arrival_datetime"] = overland_location["properties"][
                        "arrival_date"
                    ]
                    clean_data["battery_level"] = overland_location["properties"][
                        "battery_level"
                    ]
                    clean_data["battery_state"] = overland_location["properties"][
                        "battery_state"
                    ]
                    clean_data["departure_datetime"] = overland_location["properties"][
                        "departure_date"
                    ]
                    clean_data["device_id"] = overland_location["properties"][
                        "device_id"
                    ]
                    clean_data["horizontal_accuracy"] = overland_location["properties"][
                        "horizontal_accuracy"
                    ]
                    clean_data["time"] = overland_location["properties"]["timestamp"]
                    clean_data["wifi"] = overland_location["properties"]["wifi"]

                    # Add the visit to the visits list
                    visits.append(clean_data)

                except KeyError as e:
                    # Case not handled
                    print(f"KeyError: {e}")
                    print(f"Location: {overland_location}")
                    continue

            # Normal location case
            if "activity" in overland_location["properties"]:
                # Try to parse the location
                try:
                    clean_data = {}
                    clean_data["type"] = overland_location["type"]
                    clean_data["geometry_type"] = overland_location["geometry"]["type"]
                    clean_data["coordinates_longitude"] = overland_location["geometry"][
                        "coordinates"
                    ][0]
                    clean_data["coordinates_latitude"] = overland_location["geometry"][
                        "coordinates"
                    ][1]
                    clean_data["activity"] = overland_location["properties"]["activity"]
                    clean_data["altitude"] = overland_location["properties"]["altitude"]
                    clean_data["battery_level"] = overland_location["properties"][
                        "battery_level"
                    ]
                    clean_data["battery_state"] = overland_location["properties"][
                        "battery_state"
                    ]
                    clean_data["desired_accuracy"] = overland_location["properties"][
                        "desired_accuracy"
                    ]
                    clean_data["device_id"] = overland_location["properties"][
                        "device_id"
                    ]
                    clean_data["horizontal_accuracy"] = overland_location["properties"][
                        "horizontal_accuracy"
                    ]
                    clean_data["locations_in_payload"] = overland_location[
                        "properties"
                    ]["locations_in_payload"]
                    # Turn the motion list into a string
                    clean_data["motion"] = ",".join(
                        overland_location["properties"]["motion"]
                    )
                    clean_data["pauses"] = overland_location["properties"]["pauses"]
                    clean_data["speed"] = overland_location["properties"]["speed"]
                    clean_data["time"] = overland_location["properties"]["timestamp"]
                    clean_data["tracking_mode"] = overland_location["properties"][
                        "tracking_mode"
                    ]
                    clean_data["vertical_accuracy"] = overland_location["properties"][
                        "vertical_accuracy"
                    ]
                    clean_data["wifi"] = overland_location["properties"]["wifi"]
                except KeyError as e:
                    # Case not handled
                    print(f"KeyError: {e}")
                    print(f"Location: {overland_location}")
                    continue

                # Add the location to the locations list
                locations.append(clean_data)

        # Print the number of visits and locations
        print(f"Parsed visits: {len(visits)}")
        print(f"Parsed locations: {len(locations)}")

        # Serialize the data
        # Visits
        visits_serializer = VisitSerializer(data=visits, many=True)
        if visits_serializer.is_valid():
            print("Visits serializer is valid")
        else:
            print(visits_serializer.errors)
            return Response(
                {"result": "Serializer not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Locations
        locations_serializer = LocationSerializer(data=locations, many=True)
        if locations_serializer.is_valid():
            print("Locations serializer is valid")
        else:
            print(locations_serializer.errors)
            return Response(
                {"result": "Serializer not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the data to the database
        print("Saving data to the database...")
        visits_serializer.save()
        locations_serializer.save()

        print("Data saved to the database")

        return Response({"result": "ok"}, status=status.HTTP_200_OK)
