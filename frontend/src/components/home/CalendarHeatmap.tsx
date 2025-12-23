"use client";

import { differenceInDays, format, getDay, subDays } from "date-fns";
import { cn } from "@/lib/utils";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger
} from "@/components/ui/tooltip";

export interface CalendarHeatmapData {
  date: Date;
  count: number;
}

interface CalendarHeatmapProps {
  data: CalendarHeatmapData[];
  className?: string;
  /** Label for what each count represents (e.g., "step", "kilometer", "contribution"). Defaults to "contribution". */
  label?: string;
}

const CELL_SIZE = 12;
const CELL_GAP = 3;
const DAYS_IN_YEAR = 365;
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function getColorIntensity(count: number, maxCount: number): string {
  if (count === 0) return "bg-muted hover:bg-muted/80";

  const intensity = Math.min(count / Math.max(maxCount, 1), 1);

  if (intensity <= 0.25)
    return "bg-emerald-200 dark:bg-emerald-900 hover:bg-emerald-300 dark:hover:bg-emerald-800";
  if (intensity <= 0.5)
    return "bg-emerald-400 dark:bg-emerald-700 hover:bg-emerald-500 dark:hover:bg-emerald-600";
  if (intensity <= 0.75)
    return "bg-emerald-500 dark:bg-emerald-500 hover:bg-emerald-600 dark:hover:bg-emerald-400";
  return "bg-emerald-700 dark:bg-emerald-400 hover:bg-emerald-800 dark:hover:bg-emerald-300";
}

function generateDateRange(endDate: Date, days: number): Date[] {
  const dates: Date[] = [];
  for (let i = days - 1; i >= 0; i--) {
    dates.push(subDays(endDate, i));
  }
  return dates;
}

function groupByWeeks(dates: Date[]): Date[][] {
  const weeks: Date[][] = [];
  let currentWeek: Date[] = [];

  // Start from the first date and check what day of the week it is
  const firstDate = dates[0];
  const firstDayOfWeek = getDay(firstDate); // 0 = Sunday, 6 = Saturday

  // Add empty slots for days before the first date in the first week
  for (let i = 0; i < firstDayOfWeek; i++) {
    currentWeek.push(null as unknown as Date);
  }

  for (const date of dates) {
    const dayOfWeek = getDay(date);

    if (dayOfWeek === 0 && currentWeek.length > 0) {
      weeks.push(currentWeek);
      currentWeek = [];
    }

    currentWeek.push(date);
  }

  if (currentWeek.length > 0) {
    weeks.push(currentWeek);
  }

  return weeks;
}

function getMonthLabels(
  weeks: Date[][]
): { label: string; weekIndex: number }[] {
  const labels: { label: string; weekIndex: number }[] = [];
  let currentMonth = -1;

  weeks.forEach((week, weekIndex) => {
    // Find first valid date in the week
    const validDate = week.find((d) => d !== null);
    if (validDate) {
      const month = validDate.getMonth();
      if (month !== currentMonth) {
        // Only add label if we're at least 2 weeks into data or it's a new month
        currentMonth = month;
        labels.push({
          label: format(validDate, "MMM"),
          weekIndex
        });
      }
    }
  });

  return labels;
}

export function CalendarHeatmap({
  data,
  className,
  label = "contribution"
}: CalendarHeatmapProps) {
  const today = new Date();
  const dates = generateDateRange(today, DAYS_IN_YEAR);
  const weeks = groupByWeeks(dates);
  const monthLabels = getMonthLabels(weeks);

  // Create a map for quick lookup
  const dataMap = new Map<string, number>();
  data.forEach((item) => {
    const key = format(item.date, "yyyy-MM-dd");
    dataMap.set(key, item.count);
  });

  // Find max count for color scaling
  const maxCount = Math.max(...data.map((d) => d.count), 1);

  return (
    <div className={cn("w-full overflow-x-auto", className)}>
      <div className="inline-block min-w-max p-4">
        {/* Month labels */}
        <div
          className="flex mb-2 text-xs text-muted-foreground"
          style={{ marginLeft: 32 }}
        >
          {monthLabels.map((monthLabel, i) => (
            <div
              key={`${monthLabel.label}-${i}`}
              className="absolute"
              style={{
                left: 32 + monthLabel.weekIndex * (CELL_SIZE + CELL_GAP) + 16
              }}
            >
              {monthLabel.label}
            </div>
          ))}
        </div>

        {/* Grid container */}
        <div className="relative pt-6">
          {/* Month labels row - absolutely positioned */}
          <div
            className="absolute top-0 left-0 right-0 flex"
            style={{ marginLeft: 32 }}
          >
            {monthLabels.map((monthLabel, i) => (
              <span
                key={`${monthLabel.label}-${i}`}
                className="text-xs text-muted-foreground absolute"
                style={{
                  left: monthLabel.weekIndex * (CELL_SIZE + CELL_GAP)
                }}
              >
                {monthLabel.label}
              </span>
            ))}
          </div>

          <div className="flex">
            {/* Weekday labels */}
            <div
              className="flex flex-col mr-2 text-xs text-muted-foreground"
              style={{ gap: CELL_GAP }}
            >
              {WEEKDAYS.map((day, i) => (
                <div
                  key={day}
                  className="flex items-center justify-end"
                  style={{
                    height: CELL_SIZE,
                    visibility: i % 2 === 1 ? "visible" : "hidden"
                  }}
                >
                  {day}
                </div>
              ))}
            </div>

            {/* Heatmap grid */}
            <div className="flex" style={{ gap: CELL_GAP }}>
              {weeks.map((week, weekIndex) => (
                <div
                  key={weekIndex}
                  className="flex flex-col"
                  style={{ gap: CELL_GAP }}
                >
                  {week.map((date, dayIndex) => {
                    if (!date) {
                      return (
                        <div
                          key={`empty-${dayIndex}`}
                          style={{ width: CELL_SIZE, height: CELL_SIZE }}
                        />
                      );
                    }

                    const dateKey = format(date, "yyyy-MM-dd");
                    const count = dataMap.get(dateKey) ?? 0;
                    const colorClass = getColorIntensity(count, maxCount);
                    const isToday = differenceInDays(today, date) === 0;

                    return (
                      <Tooltip key={dateKey}>
                        <TooltipTrigger asChild>
                          <div
                            className={cn(
                              "rounded-[3px] cursor-pointer transition-colors",
                              colorClass,
                              isToday &&
                                "ring-1 ring-foreground ring-offset-1 ring-offset-background"
                            )}
                            style={{ width: CELL_SIZE, height: CELL_SIZE }}
                          />
                        </TooltipTrigger>
                        <TooltipContent side="top" sideOffset={5}>
                          <p className="font-medium">
                            {count} {label}
                            {count !== 1 ? "s" : ""} on{" "}
                            {format(date, "MMM d, yyyy")}
                          </p>
                        </TooltipContent>
                      </Tooltip>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex items-center justify-end mt-4 gap-2 text-xs text-muted-foreground">
            <span>Less</span>
            <div className="flex gap-1">
              <div
                className="rounded-[3px] bg-muted"
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
              <div
                className="rounded-[3px] bg-emerald-200 dark:bg-emerald-900"
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
              <div
                className="rounded-[3px] bg-emerald-400 dark:bg-emerald-700"
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
              <div
                className="rounded-[3px] bg-emerald-500 dark:bg-emerald-500"
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
              <div
                className="rounded-[3px] bg-emerald-700 dark:bg-emerald-400"
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
            </div>
            <span>More</span>
          </div>
        </div>
      </div>
    </div>
  );
}
