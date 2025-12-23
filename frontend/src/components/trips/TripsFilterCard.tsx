import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ChevronDown, ChevronUp } from "lucide-react";

interface TripsFilterCardProps {
  onSubmit?: (
    startDateTime: string,
    endDateTime: string,
    showVisits: boolean,
    showStationary: boolean,
    separateTrips: boolean,
    desiredAccuracy: number
  ) => void;
}

// Helper function to format date for datetime-local input
const formatDateTimeLocal = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

const TripsFilterCard = ({ onSubmit }: TripsFilterCardProps) => {
  // Default to last 24 hours
  const now = new Date();
  const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

  const [isOpen, setIsOpen] = useState(true);
  const [startDateTime, setStartDateTime] = useState(
    formatDateTimeLocal(twentyFourHoursAgo)
  );
  const [endDateTime, setEndDateTime] = useState(formatDateTimeLocal(now));
  const [showVisits, setShowVisits] = useState(false);
  const [showStationary, setShowStationary] = useState(false);
  const [separateTrips, setSeparateTrips] = useState(false);
  const [desiredAccuracy, setDesiredAccuracy] = useState(0);
  const [quickSelect, setQuickSelect] = useState<string>("last24h");

  // Quick select time frame handlers
  const handleQuickSelect = (type: string) => {
    setQuickSelect(type);
    const now = new Date();
    let start = new Date();

    switch (type) {
      case "last24h":
        start = new Date(now.getTime() - 24 * 60 * 60 * 1000);
        break;
      case "today":
        start = new Date(now);
        start.setHours(0, 0, 0, 0);
        break;
      case "yesterday":
        start = new Date(now);
        start.setDate(start.getDate() - 1);
        start.setHours(0, 0, 0, 0);
        const yesterdayEnd = new Date(now);
        yesterdayEnd.setDate(yesterdayEnd.getDate() - 1);
        yesterdayEnd.setHours(23, 59, 59, 999);
        setStartDateTime(formatDateTimeLocal(start));
        setEndDateTime(formatDateTimeLocal(yesterdayEnd));
        return;
      case "thisWeek":
        start = new Date(now);
        const dayOfWeek = start.getDay();
        const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // Monday as first day
        start.setDate(start.getDate() - diff);
        start.setHours(0, 0, 0, 0);
        break;
      case "past7d":
        start = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case "past30d":
        start = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case "thisMonth":
        start = new Date(now.getFullYear(), now.getMonth(), 1, 0, 0, 0, 0);
        break;
      case "lastMonth":
        start = new Date(now.getFullYear(), now.getMonth() - 1, 1, 0, 0, 0, 0);
        const lastMonthEnd = new Date(now.getFullYear(), now.getMonth(), 0, 23, 59, 59, 999);
        setStartDateTime(formatDateTimeLocal(start));
        setEndDateTime(formatDateTimeLocal(lastMonthEnd));
        return;
      default:
        return;
    }

    setStartDateTime(formatDateTimeLocal(start));
    setEndDateTime(formatDateTimeLocal(now));
  };

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(
        startDateTime,
        endDateTime,
        showVisits,
        showStationary,
        separateTrips,
        desiredAccuracy
      );
    }
  };

  return (
    <div className="absolute bottom-6 left-6 z-50">
      {!isOpen ? (
        <Button
          variant="outline"
          size="icon"
          onClick={() => setIsOpen(true)}
          aria-label="Open filter"
          className="shadow-lg hover:cursor-pointer hover:bg-gray-200/90"
        >
          <ChevronUp className="h-4 w-4" />
        </Button>
      ) : (
        <Card className="w-80 shadow-lg">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">Filter</CardTitle>
              <Button
                variant="ghost"
                size="icon-sm"
                onClick={() => setIsOpen(false)}
                aria-label="Close filter"
                className="hover:cursor-pointer hover:bg-gray-200/90"
              >
                <ChevronDown className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label
                htmlFor="start-datetime"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Start Date & Time
              </label>
              <Input
                id="start-datetime"
                type="datetime-local"
                value={startDateTime}
                onChange={(e) => setStartDateTime(e.target.value)}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <label
                htmlFor="end-datetime"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                End Date & Time
              </label>
              <Input
                id="end-datetime"
                type="datetime-local"
                value={endDateTime}
                onChange={(e) => setEndDateTime(e.target.value)}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-sm font-medium">Quick Select</Label>
              <Select value={quickSelect} onValueChange={handleQuickSelect}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select time range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="last24h">Last 24 hours</SelectItem>
                  <SelectItem value="today">Today</SelectItem>
                  <SelectItem value="yesterday">Yesterday</SelectItem>
                  <SelectItem value="thisWeek">This Week</SelectItem>
                  <SelectItem value="past7d">Past 7 days</SelectItem>
                  <SelectItem value="past30d">Past 30 days</SelectItem>
                  <SelectItem value="thisMonth">This Month</SelectItem>
                  <SelectItem value="lastMonth">Last Month</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="show-visits" className="text-sm font-medium">
                  Show Visits
                </Label>
                <Switch
                  id="show-visits"
                  checked={showVisits}
                  onCheckedChange={setShowVisits}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="show-stationary" className="text-sm font-medium">
                  Show Stationary
                </Label>
                <Switch
                  id="show-stationary"
                  checked={showStationary}
                  onCheckedChange={setShowStationary}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label htmlFor="separate-trips" className="text-sm font-medium">
                  Separate Trips
                </Label>
                <Switch
                  id="separate-trips"
                  checked={separateTrips}
                  onCheckedChange={setSeparateTrips}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="desired-accuracy" className="text-sm font-medium">
                  Desired Accuracy (meters, 0 = no filter)
                </Label>
                <Input
                  id="desired-accuracy"
                  type="number"
                  min="0"
                  step="1"
                  value={desiredAccuracy}
                  onChange={(e) => setDesiredAccuracy(Number(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>

            <Button
              onClick={handleSubmit}
              className="w-full hover:bg-primary/90 hover:cursor-pointer"
              disabled={!startDateTime || !endDateTime}
            >
              Apply Filter
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default TripsFilterCard;
