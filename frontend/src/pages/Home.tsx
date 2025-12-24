import { useState, useEffect, useMemo } from "react";
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
import { wayfinderActivityHistoryRetrieve } from "@/api/django/wayfinder/wayfinder";
import type { DailyActivity } from "@/api/django/api.schemas";
import { toast } from "sonner";
import { MapPin, Navigation } from "lucide-react";

const Home = () => {
  const [activityData, setActivityData] = useState<DailyActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchActivityHistory = async () => {
      try {
        const response = await wayfinderActivityHistoryRetrieve();
        setActivityData(response.data);
      } catch (error) {
        console.error("Error fetching activity history:", error);
        toast.error("Failed to load activity history");
      } finally {
        setIsLoading(false);
      }
    };

    fetchActivityHistory();
  }, []);

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

  return (
    <SideBarLayout title="Dashboard">
      <div className="flex flex-col gap-6 p-6 w-full items-center">
        <div className="grid gap-6">
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
                  `${totalLocations.toLocaleString()} location points recorded in the past year`
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="flex items-center justify-center h-[140px] w-full overflow-x-auto">
                  <CalendarHeatmapSkeleton />
                </div>
              ) : (
                <CalendarHeatmap data={locationsData} label="location" />
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
                  `${totalVisits.toLocaleString()} visits recorded in the past year`
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="flex items-center justify-center h-[140px] w-full overflow-x-auto">
                  <CalendarHeatmapSkeleton />
                </div>
              ) : (
                <CalendarHeatmap data={visitsData} label="visit" />
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </SideBarLayout>
  );
};

export default Home;
