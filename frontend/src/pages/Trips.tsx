import { useState } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import TripsFilterCard from "@/components/trips/TripsFilterCard";
import TripsMap from "@/components/trips/TripsMap";
import { wayfinderTripsPlotRetrieve } from "@/api/django/wayfinder/wayfinder";
import type { TripPlotResponse } from "@/api/django/api.schemas";
import { toast } from "sonner";

const Trips = () => {
  const [tripData, setTripData] = useState<TripPlotResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFilterSubmit = async (
    startDateTime: string,
    endDateTime: string,
    showVisits: boolean,
    showStationary: boolean,
    separateTrips: boolean,
    desiredAccuracy: number
  ) => {
    setIsLoading(true);

    try {
      // Convert datetime-local format to ISO string
      const startDate = new Date(startDateTime).toISOString();
      const endDate = new Date(endDateTime).toISOString();

      const response = await wayfinderTripsPlotRetrieve({
        start_datetime: startDate,
        end_datetime: endDate,
        show_visits: showVisits,
        show_stationary: showStationary,
        separate_trips: separateTrips,
        desired_accuracy: desiredAccuracy
      });

      setTripData(response);

      const totalFeatures =
        (response.trips?.features?.length || 0) +
        (response.visits?.features?.length || 0) +
        (response.stationary?.features?.length || 0);

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
