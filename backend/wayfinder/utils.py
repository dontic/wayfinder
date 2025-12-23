import logging
from datetime import datetime


log = logging.getLogger(__name__)


def get_visit_midtime(visit):
    """Calculate the midpoint time of a visit."""
    arrival = visit["arrival_date"]
    departure = visit["departure_date"]
    
    # Handle pandas Timestamp or datetime objects
    if hasattr(arrival, 'timestamp'):
        arrival_ts = arrival.timestamp()
        departure_ts = departure.timestamp()
    else:
        arrival_ts = arrival.timestamp()
        departure_ts = departure.timestamp()
    
    mid_ts = (arrival_ts + departure_ts) / 2
    return datetime.fromtimestamp(mid_ts, tz=arrival.tzinfo)


def segment_trips_by_visits(locations_df, visits_df):
    """
    Segment trips based on visit midtimes.
    
    Returns a list of tuples: (trip_id, locations_df_segment)
    Each segment represents a trip between visit midpoints.
    """
    if locations_df.empty:
        return []
    
    # Sort dataframes by time
    locations_df = locations_df.sort_values("time").copy()
    
    if visits_df.empty:
        # No visits, return single trip
        return [("trip_001", locations_df)]
    
    visits_df = visits_df.sort_values("arrival_date").copy()
    
    # Calculate midtimes for all visits
    midtimes = [get_visit_midtime(row) for _, row in visits_df.iterrows()]
    
    segments = []
    trip_counter = 1
    
    # First segment: before first visit midtime
    mask = locations_df["time"] < midtimes[0]
    if mask.any():
        segments.append((f"trip_{trip_counter:03d}", locations_df[mask].copy()))
        trip_counter += 1
    
    # Segments between visit midtimes
    for i in range(len(midtimes) - 1):
        mask = (locations_df["time"] >= midtimes[i]) & (locations_df["time"] < midtimes[i + 1])
        if mask.any():
            segments.append((f"trip_{trip_counter:03d}", locations_df[mask].copy()))
            trip_counter += 1
    
    # Last segment: after last visit midtime
    mask = locations_df["time"] >= midtimes[-1]
    if mask.any():
        segments.append((f"trip_{trip_counter:03d}", locations_df[mask].copy()))
    
    return segments


def locations_to_geojson_linestring(trip_id, locations_df):
    """
    Convert a locations DataFrame to a GeoJSON LineString Feature.
    """
    if locations_df.empty:
        return None
    
    # Sort by time
    locations_df = locations_df.sort_values("time")
    
    # Build coordinates array [lon, lat]
    coordinates = [
        [float(row["longitude"]), float(row["latitude"])]
        for _, row in locations_df.iterrows()
    ]
    
    # Build times array
    times = [
        row["time"].isoformat() if hasattr(row["time"], 'isoformat') else str(row["time"])
        for _, row in locations_df.iterrows()
    ]
    
    return {
        "type": "Feature",
        "id": trip_id,
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        },
        "properties": {
            "trip_id": trip_id,
            "times": times
        }
    }


def visit_to_geojson_point(visit, visit_id):
    """
    Convert a visit row to a GeoJSON Point Feature.
    """
    arrival = visit["arrival_date"]
    departure = visit["departure_date"]
    
    # Calculate duration in seconds
    if hasattr(arrival, 'timestamp'):
        duration_s = int(departure.timestamp() - arrival.timestamp())
    else:
        duration_s = int((departure - arrival).total_seconds())
    
    return {
        "type": "Feature",
        "id": visit_id,
        "geometry": {
            "type": "Point",
            "coordinates": [float(visit["longitude"]), float(visit["latitude"])]
        },
        "properties": {
            "visit_id": visit_id,
            "start": arrival.isoformat() if hasattr(arrival, 'isoformat') else str(arrival),
            "end": departure.isoformat() if hasattr(departure, 'isoformat') else str(departure),
            "duration_s": duration_s,
            "radius_m": int(visit.get("horizontal_accuracy", 0))
        }
    }


def stationary_location_to_geojson_point(location, stationary_id):
    """
    Convert a stationary location row to a GeoJSON Point Feature.
    """
    time = location["time"]
    
    return {
        "type": "Feature",
        "id": stationary_id,
        "geometry": {
            "type": "Point",
            "coordinates": [float(location["longitude"]), float(location["latitude"])]
        },
        "properties": {
            "stationary_id": stationary_id,
            "start": time.isoformat() if hasattr(time, 'isoformat') else str(time),
            "end": time.isoformat() if hasattr(time, 'isoformat') else str(time),
            "duration_s": 0,
            "source": "location_samples"
        }
    }


def build_trips_feature_collection(locations_df, visits_df, separate_trips=False):
    """
    Build a GeoJSON FeatureCollection for trips.
    
    If separate_trips is False, returns a single trip.
    If separate_trips is True, segments trips by visit midtimes.
    """
    features = []
    
    if locations_df.empty:
        return {"type": "FeatureCollection", "features": features}
    
    if not separate_trips or visits_df.empty:
        # Single trip
        feature = locations_to_geojson_linestring("trip_001", locations_df)
        if feature:
            features.append(feature)
    else:
        # Segment trips by visit midtimes
        segments = segment_trips_by_visits(locations_df, visits_df)
        for trip_id, segment_df in segments:
            feature = locations_to_geojson_linestring(trip_id, segment_df)
            if feature:
                features.append(feature)
    
    return {"type": "FeatureCollection", "features": features}


def build_visits_feature_collection(visits_df):
    """
    Build a GeoJSON FeatureCollection for visits.
    """
    features = []
    
    if visits_df.empty:
        return {"type": "FeatureCollection", "features": features}
    
    for idx, (_, visit) in enumerate(visits_df.iterrows(), start=1):
        visit_id = f"visit_{idx:03d}"
        feature = visit_to_geojson_point(visit, visit_id)
        features.append(feature)
    
    return {"type": "FeatureCollection", "features": features}


def build_stationary_feature_collection(locations_df):
    """
    Build a GeoJSON FeatureCollection for stationary locations.
    Filters for locations where motion contains only "stationary".
    """
    features = []
    
    if locations_df.empty:
        return {"type": "FeatureCollection", "features": features}
    
    # Filter for stationary locations (motion == ["stationary"])
    stationary_mask = locations_df["motion"].apply(
        lambda m: m == ["stationary"] if isinstance(m, list) else False
    )
    stationary_df = locations_df[stationary_mask]
    
    for idx, (_, location) in enumerate(stationary_df.iterrows(), start=1):
        stationary_id = f"stationary_{idx:03d}"
        feature = stationary_location_to_geojson_point(location, stationary_id)
        features.append(feature)
    
    return {"type": "FeatureCollection", "features": features}
