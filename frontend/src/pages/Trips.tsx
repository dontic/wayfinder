import { useState, useEffect } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import TripsFilterCard from "@/components/trips/TripsFilterCard";
import TripsMap from "@/components/trips/TripsMap";
import { wayfinderTripsPlotRetrieve } from "@/api/django/wayfinder/wayfinder";
import type { TripPlotResponse } from "@/api/django/api.schemas";
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

const Trips = () => {
  const [tripData, setTripData] = useState<TripPlotResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFilterSubmit = async (
    startDateTime: string,
    endDateTime: string,
    showVisits: boolean,
    separateTrips: boolean,
    desiredAccuracy: number
  ) => {
    setIsLoading(true);

    try {
      // Convert datetime-local format to timezone-aware ISO string
      const startDate = toTimezoneAwareISO(startDateTime);
      const endDate = toTimezoneAwareISO(endDateTime);

      const response = await wayfinderTripsPlotRetrieve({
        start_datetime: startDate,
        end_datetime: endDate,
        show_visits: showVisits,
        separate_trips: separateTrips,
        desired_accuracy: desiredAccuracy
      });

      setTripData(response);

      const totalFeatures =
        (response.trips?.features?.length || 0) +
        (response.visits?.features?.length || 0);

      if (totalFeatures === 0) {
        toast.info("No trips found for the selected date range");
      } else {
        toast.success(`Loaded ${response.trips?.features?.length || 0} trips`);
      }
    } catch (error) {
      console.error("Error fetching trips:", error);
      toast.error("Failed to load trips. Please try again.");
      setTripData(null);
    } finally {
      setIsLoading(false);
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
        <TripsMap data={tripData} isLoading={isLoading} />
        <TripsFilterCard onSubmit={handleFilterSubmit} />
      </div>
    </SideBarLayout>
  );
};

export default Trips;
