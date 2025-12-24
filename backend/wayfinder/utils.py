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


def get_sorted_visit_midtimes(visits_df):
    """
    Get a sorted list of visit midtimes from a visits DataFrame.
    
    Returns an empty list if visits_df is empty.
    """
    if visits_df.empty:
        return []
    
    visits_df = visits_df.sort_values("arrival_date").copy()
    visits_records = visits_df.to_dict('records')
    return [get_visit_midtime(visit) for visit in visits_records]


def find_last_complete_trip_boundary(locations_list, midtimes):
    """
    Find the index where we should truncate locations to avoid splitting a trip.
    
    When paginating with separate_trips=True, we want to ensure the last trip
    in the current page is complete. A trip is "complete" if it ends at a visit
    midtime (i.e., the next point would be >= a midtime).
    
    Args:
        locations_list: List of location dicts with 'time' field, sorted by time
        midtimes: Sorted list of visit midtimes (datetime objects)
    
    Returns:
        tuple: (truncated_locations_list, truncation_midtime or None)
        - truncated_locations_list: Locations up to (but not including) the last trip
          that might continue beyond this page
        - truncation_midtime: The midtime used for truncation, or None if no truncation
    """
    if not locations_list or not midtimes:
        return locations_list, None
    
    last_point_time = locations_list[-1]['time']
    
    # Find the largest midtime that is <= last_point_time
    # This is the start of the trip that the last point belongs to
    trip_start_midtime = None
    for m in reversed(midtimes):
        if m <= last_point_time:
            trip_start_midtime = m
            break
    
    if trip_start_midtime is None:
        # All locations are before the first visit midtime - this is one trip
        # that might continue, so we can't safely include any of it
        # But we need to return something, so check if there's a midtime we can use
        if midtimes and midtimes[0] > last_point_time:
            # The first midtime is after all our points - the entire page is one 
            # potentially incomplete trip. We must include it to make progress.
            return locations_list, None
        return locations_list, None
    
    # Truncate: keep only locations with time < trip_start_midtime
    truncated = [loc for loc in locations_list if loc['time'] < trip_start_midtime]
    
    # If truncation would remove ALL locations, don't truncate
    # (this happens when all locations belong to one trip that's larger than page_size)
    if not truncated:
        return locations_list, None
    
    return truncated, trip_start_midtime


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
    
    # Calculate midtimes for all visits using to_dict (faster than iterrows)
    visits_records = visits_df.to_dict('records')
    midtimes = [get_visit_midtime(visit) for visit in visits_records]
    
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
    
    # Convert to list of dicts once (much faster than iterrows)
    locations_records = locations_df.to_dict('records')
    
    # Build coordinates array [lon, lat]
    coordinates = [
        [float(loc["longitude"]), float(loc["latitude"])]
        for loc in locations_records
    ]
    
    # Build times array
    times = [
        loc["time"].isoformat() if hasattr(loc["time"], 'isoformat') else str(loc["time"])
        for loc in locations_records
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
    
    # Convert to list of dicts once (much faster than iterrows)
    visits_records = visits_df.to_dict('records')
    
    for idx, visit in enumerate(visits_records, start=1):
        visit_id = f"visit_{idx:03d}"
        feature = visit_to_geojson_point(visit, visit_id)
        features.append(feature)
    
    return {"type": "FeatureCollection", "features": features}
