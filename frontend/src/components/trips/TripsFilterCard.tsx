import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ChevronDown, ChevronUp } from "lucide-react";

interface TripsFilterCardProps {
  onSubmit?: (startDateTime: string, endDateTime: string) => void;
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

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(startDateTime, endDateTime);
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
