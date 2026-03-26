import { useState, useEffect, useMemo } from "react";
import { format, subDays } from "date-fns";
import { useNavigate } from "react-router-dom";
import SideBarLayout from "@/layouts/SideBarLayout";
import {
  CalendarHeatmap,
  type CalendarHeatmapData
} from "@/components/home/CalendarHeatmap";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import CalendarHeatmapSkeleton from "@/components/home/CalendarHeatmapSkeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { wayfinderActivityHistoryRetrieve } from "@/api/django/wayfinder/wayfinder";
import type { DailyActivity } from "@/api/django/api.schemas";
import { useHomeStore, type Period } from "@/stores/HomeStore";
import { toast } from "sonner";
import { MapPin, Navigation } from "lucide-react";

const EARLIEST_YEAR = 2020;

function getPeriodDateRange(period: Period): {
  startDate: Date;
  endDate: Date;
  apiStart: string;
  apiEnd: string;
  showFutureGray: boolean;
} {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const currentYear = today.getFullYear();

  if (period === "past-year") {
    const start = subDays(today, 364);
    return {
      startDate: start,
      endDate: today,
      apiStart: format(start, "yyyy-MM-dd"),
      apiEnd: format(today, "yyyy-MM-dd"),
      showFutureGray: false
    };
  }

  if (period === "ytd") {
    const start = new Date(currentYear, 0, 1); // Jan 1 of current year
    const end = new Date(currentYear, 11, 31); // Dec 31 of current year
    return {
      startDate: start,
      endDate: end,
      apiStart: format(start, "yyyy-MM-dd"),
      apiEnd: format(today, "yyyy-MM-dd"),
      showFutureGray: true
    };
  }

  // Specific year
  const year = parseInt(period, 10);
  const start = new Date(year, 0, 1);
  const end = new Date(year, 11, 31);
  return {
    startDate: start,
    endDate: end,
    apiStart: format(start, "yyyy-MM-dd"),
    apiEnd: format(end, "yyyy-MM-dd"),
    showFutureGray: false
  };
}

function getPeriodLabel(period: Period): string {
  if (period === "past-year") return "in the past year";
  if (period === "ytd") return "year to date";
  return `in ${period}`;
}

const Home = () => {
  const navigate = useNavigate();
  const { selectedPeriod, setSelectedPeriod } = useHomeStore();
  const [activityData, setActivityData] = useState<DailyActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const currentYear = new Date().getFullYear();
  const previousYears = Array.from(
    { length: currentYear - EARLIEST_YEAR },
    (_, i) => String(currentYear - 1 - i)
  );

  const { startDate, endDate, apiStart, apiEnd, showFutureGray } = useMemo(
    () => getPeriodDateRange(selectedPeriod),
    [selectedPeriod]
  );

  useEffect(() => {
    const fetchActivityHistory = async () => {
      setIsLoading(true);
      setActivityData([]);
      try {
        const { data, status } = await wayfinderActivityHistoryRetrieve({
          start_date: apiStart,
          end_date: apiEnd
        });
        setActivityData(data.data);

        if (status === 206) {
          toast.info(
            "Some dates are still being computed in the background. Refresh the page shortly for complete data.",
            { id: "activity-history-206", duration: 8000 }
          );
        }
      } catch (error: unknown) {
        const status = (error as { response?: { status?: number } })?.response
          ?.status;
        if (status === 404) {
          const message = (
            error as { response?: { data?: { message?: string } } }
          )?.response?.data?.message;
          toast.info(message ?? "No activity data found.", {
            id: "activity-history-404"
          });
        } else {
          console.error("Error fetching activity history:", error);
          toast.error("Failed to load activity history");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchActivityHistory();
  }, [apiStart, apiEnd]);

  const locationsData: CalendarHeatmapData[] = useMemo(() => {
    return activityData.map((item) => ({
      date: new Date(item.date),
      count: item.location_count
    }));
  }, [activityData]);

  const visitsData: CalendarHeatmapData[] = useMemo(() => {
    return activityData.map((item) => ({
      date: new Date(item.date),
      count: item.visit_count
    }));
  }, [activityData]);

  const totalLocations = useMemo(() => {
    return activityData.reduce((sum, item) => sum + item.location_count, 0);
  }, [activityData]);

  const totalVisits = useMemo(() => {
    return activityData.reduce((sum, item) => sum + item.visit_count, 0);
  }, [activityData]);

  const periodLabel = getPeriodLabel(selectedPeriod);

  const periodSelector = (
    <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
      <SelectTrigger size="sm" className="w-36">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="past-year">Past year</SelectItem>
        <SelectItem value="ytd">YTD</SelectItem>
        {previousYears.map((year) => (
          <SelectItem key={year} value={year}>
            {year}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );

  return (
    <SideBarLayout title="Dashboard" actions={periodSelector}>
      <div className="flex flex-col gap-6 p-6 w-full items-center">
        <div className="grid gap-6 w-full md:w-fit mx-auto">
          {/* Locations Heatmap */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Navigation className="h-5 w-5 text-blue-500" />
                <CardTitle>Locations</CardTitle>
              </div>
              <CardDescription>
                {isLoading ? (
                  <Skeleton className="h-4 w-48" />
                ) : (
                  `${totalLocations.toLocaleString()} location points recorded ${periodLabel}`
                )}
              </CardDescription>
            </CardHeader>
            <CardContent className="min-w-0">
              {isLoading ? (
                <div className="flex items-center justify-center h-[140px] w-full overflow-x-auto">
                  <CalendarHeatmapSkeleton />
                </div>
              ) : (
                <CalendarHeatmap
                  data={locationsData}
                  startDate={startDate}
                  endDate={endDate}
                  showFutureGray={showFutureGray}
                  label="location"
                  onDateClick={(date) =>
                    navigate(`/trips?date=${format(date, "yyyy-MM-dd")}`)
                  }
                />
              )}
            </CardContent>
          </Card>

          {/* Visits Heatmap */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <MapPin className="h-5 w-5 text-rose-500" />
                <CardTitle>Visits</CardTitle>
              </div>
              <CardDescription>
                {isLoading ? (
                  <Skeleton className="h-4 w-48" />
                ) : (
                  `${totalVisits.toLocaleString()} visits recorded ${periodLabel}`
                )}
              </CardDescription>
            </CardHeader>
            <CardContent className="min-w-0">
              {isLoading ? (
                <div className="flex items-center justify-center h-[140px] w-full overflow-x-auto">
                  <CalendarHeatmapSkeleton />
                </div>
              ) : (
                <CalendarHeatmap
                  data={visitsData}
                  startDate={startDate}
                  endDate={endDate}
                  showFutureGray={showFutureGray}
                  label="visit"
                  onDateClick={(date) =>
                    navigate(`/visits?date=${format(date, "yyyy-MM-dd")}`)
                  }
                />
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </SideBarLayout>
  );
};

export default Home;
