import { useState, useEffect, useRef, useCallback } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import TripsFilterCard from "@/components/trips/TripsFilterCard";
import TripsMap from "@/components/trips/TripsMap";
import { wayfinderTripsPlotRetrieve } from "@/api/django/wayfinder/wayfinder";
import type {
  TripPlotResponse,
  GeoJSONFeature
} from "@/api/django/api.schemas";
import { toast } from "sonner";

// Helper function to format date for datetime-local input
const formatDateTimeLocal = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

// Helper function to convert datetime-local string to timezone-aware ISO string
const toTimezoneAwareISO = (datetimeLocal: string): string => {
  // Create a date object from the datetime-local value
  const date = new Date(datetimeLocal);

  // Get timezone offset in minutes and convert to hours and minutes
  const offset = -date.getTimezoneOffset();
  const offsetHours = Math.floor(Math.abs(offset) / 60);
  const offsetMinutes = Math.abs(offset) % 60;
  const offsetSign = offset >= 0 ? "+" : "-";

  // Format: YYYY-MM-DDTHH:mm:ss±HH:MM
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}${offsetSign}${String(offsetHours).padStart(2, "0")}:${String(offsetMinutes).padStart(2, "0")}`;
};

// Helper to merge line features by appending coordinates for same IDs
const mergeLineFeatures = (
  existing: GeoJSONFeature[],
  incoming: GeoJSONFeature[]
): GeoJSONFeature[] => {
  if (existing.length === 0) return incoming;
  if (incoming.length === 0) return existing;

  // Create a map of existing features by their trip_id
  const featureMap = new Map<string, GeoJSONFeature>();

  // Add existing features to map
  for (const feature of existing) {
    const tripId = feature.properties?.trip_id as string | undefined;
    if (tripId) {
      featureMap.set(tripId, feature);
    } else {
      // Features without trip_id - use a unique key
      featureMap.set(`_no_id_${featureMap.size}`, feature);
    }
  }

  // Merge incoming features
  for (const feature of incoming) {
    const tripId = feature.properties?.trip_id as string | undefined;

    if (tripId && featureMap.has(tripId)) {
      // Merge coordinates with existing feature
      const existingFeature = featureMap.get(tripId)!;
      if (
        existingFeature.geometry.type === "LineString" &&
        feature.geometry.type === "LineString"
      ) {
        // Append coordinates from incoming feature
        existingFeature.geometry.coordinates = [
          ...(existingFeature.geometry.coordinates as number[][]),
          ...(feature.geometry.coordinates as number[][])
        ];
      }
    } else if (tripId) {
      // New trip_id, add to map
      featureMap.set(tripId, feature);
    } else {
      // No trip_id, add as new feature
      featureMap.set(`_no_id_${featureMap.size}`, feature);
    }
  }

  return Array.from(featureMap.values());
};

interface LoadingProgress {
  loaded: number;
  total: number;
}

const Trips = () => {
  const [tripData, setTripData] = useState<TripPlotResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingProgress, setLoadingProgress] =
    useState<LoadingProgress | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Cancel any ongoing fetch when component unmounts or new fetch starts
  const cancelOngoingFetch = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => cancelOngoingFetch();
  }, [cancelOngoingFetch]);

  const handleFilterSubmit = async (
    startDateTime: string,
    endDateTime: string,
    showVisits: boolean,
    separateTrips: boolean,
    desiredAccuracy: number
  ) => {
    // Cancel any ongoing fetch
    cancelOngoingFetch();

    setIsLoading(true);
    setLoadingProgress(null);
    setTripData(null);

    // Create new abort controller for this fetch
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    try {
      // Convert datetime-local format to timezone-aware ISO string
      const startDate = toTimezoneAwareISO(startDateTime);
      const endDate = toTimezoneAwareISO(endDateTime);

      let cursor: string | undefined = undefined;
      let accumulatedTrips: GeoJSONFeature[] = [];
      let accumulatedVisits: GeoJSONFeature[] = [];
      let latestResponse: TripPlotResponse | null = null;
      let totalPoints = 0;
      let loadedPoints = 0;

      // Fetch pages until no more data
      do {
        // Check if aborted
        if (abortController.signal.aborted) {
          return;
        }

        const response = await wayfinderTripsPlotRetrieve({
          start_datetime: startDate,
          end_datetime: endDate,
          show_visits: showVisits,
          separate_trips: separateTrips,
          desired_accuracy: desiredAccuracy,
          no_bucket: true, // Get raw points for pagination
          cursor
        });

        // Check if aborted after fetch
        if (abortController.signal.aborted) {
          return;
        }

        latestResponse = response;

        // On first page, get total from meta
        if (!cursor) {
          totalPoints = response.meta.trip_locations_raw;
        }

        // Accumulate trip features
        if (response.trips?.features) {
          accumulatedTrips = mergeLineFeatures(
            accumulatedTrips,
            response.trips.features
          );
        }

        // Accumulate visit features (only on first page typically)
        if (response.visits?.features && cursor === undefined) {
          accumulatedVisits = response.visits.features;
        }

        // Update loaded points count
        loadedPoints += response.meta.trip_locations;

        // Update progress
        setLoadingProgress({
          loaded: loadedPoints,
          total: totalPoints
        });

        // Update trip data progressively so the map shows data as it loads
        setTripData({
          ...response,
          trips: {
            type: "FeatureCollection",
            features: accumulatedTrips
          },
          visits: {
            type: "FeatureCollection",
            features: accumulatedVisits
          }
        });

        // Get next cursor
        cursor = response.pagination.has_more
          ? (response.pagination.next_cursor ?? undefined)
          : undefined;
      } while (cursor);

      // Final update
      if (latestResponse) {
        const finalData: TripPlotResponse = {
          ...latestResponse,
          trips: {
            type: "FeatureCollection",
            features: accumulatedTrips
          },
          visits: {
            type: "FeatureCollection",
            features: accumulatedVisits
          }
        };

        setTripData(finalData);

        const totalFeatures =
          accumulatedTrips.length + accumulatedVisits.length;

        if (totalFeatures === 0) {
          toast.info("No trips found for the selected date range");
        } else {
          toast.success(
            `Loaded ${accumulatedTrips.length} trip${accumulatedTrips.length !== 1 ? "s" : ""} (${loadedPoints.toLocaleString()} points)`
          );
        }
      }
    } catch (error) {
      // Ignore abort errors
      if (error instanceof Error && error.name === "AbortError") {
        return;
      }
      console.error("Error fetching trips:", error);
      toast.error("Failed to load trips. Please try again.");
      setTripData(null);
    } finally {
      setIsLoading(false);
      setLoadingProgress(null);
      abortControllerRef.current = null;
    }
  };

  // Automatically query with default filters on component mount
  useEffect(() => {
    const now = new Date();
    const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

    handleFilterSubmit(
      formatDateTimeLocal(twentyFourHoursAgo),
      formatDateTimeLocal(now),
      false, // showVisits
      false, // separateTrips
      0 // desiredAccuracy
    );
  }, []); // Empty dependency array ensures this runs only once on mount

  return (
    <SideBarLayout title="Trips" defaultOpen={false}>
      <div className="relative flex flex-col h-full w-full">
        <TripsMap
          data={tripData}
          isLoading={isLoading}
          loadingProgress={loadingProgress}
        />
        <TripsFilterCard onSubmit={handleFilterSubmit} />
      </div>
    </SideBarLayout>
  );
};

export default Trips;
