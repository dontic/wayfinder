import { useState, useEffect } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import VisitsFilterCard from "@/components/visits/VisitsFilterCard";
import VisitsHeatmap from "@/components/visits/VisitsHeatmap";
import { wayfinderVisitsRetrieve } from "@/api/django/wayfinder/wayfinder";
import type { VisitPlotResponse } from "@/api/django/api.schemas";
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

const Visits = () => {
  const [visitData, setVisitData] = useState<VisitPlotResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFilterSubmit = async (
    startDateTime: string,
    endDateTime: string
  ) => {
    setIsLoading(true);

    try {
      // Convert datetime-local format to timezone-aware ISO string
      const startDate = toTimezoneAwareISO(startDateTime);
      const endDate = toTimezoneAwareISO(endDateTime);

      const response = await wayfinderVisitsRetrieve({
        start_datetime: startDate,
        end_datetime: endDate
      });

      setVisitData(response);

      const totalVisits = response.visits?.features?.length || 0;

      if (totalVisits === 0) {
        toast.info("No visits found for the selected date range");
      } else {
        toast.success(`Loaded ${totalVisits} visits`);
      }
    } catch (error) {
      console.error("Error fetching visits:", error);
      toast.error("Failed to load visits. Please try again.");
      setVisitData(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Automatically query with default filters on component mount
  useEffect(() => {
    const now = new Date();
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

    handleFilterSubmit(
      formatDateTimeLocal(thirtyDaysAgo),
      formatDateTimeLocal(now)
    );
  }, []); // Empty dependency array ensures this runs only once on mount

  return (
    <SideBarLayout title="Visits" defaultOpen={false}>
      <div className="relative flex flex-col h-full w-full">
        <div className="flex-1">
          <VisitsHeatmap data={visitData} isLoading={isLoading} />
        </div>
        <VisitsFilterCard onSubmit={handleFilterSubmit} />
      </div>
    </SideBarLayout>
  );
};

export default Visits;
