const CalendarHeatmapSkeleton = () => {
  return (
    <div className="flex gap-1 animate-pulse">
      {/* Generate 52 weeks (columns) */}
      {Array.from({ length: 52 }).map((_, weekIndex) => (
        <div key={weekIndex} className="flex flex-col gap-1">
          {/* Generate 7 days (rows) for each week */}
          {Array.from({ length: 7 }).map((_, dayIndex) => (
            <div
              key={dayIndex}
              className="w-[10px] h-[10px] rounded-sm bg-gradient-to-r from-zinc-200 via-zinc-300 to-zinc-200 dark:from-zinc-800 dark:via-zinc-700 dark:to-zinc-800 animate-shimmer"
              style={{
                animationDelay: `${(weekIndex * 7 + dayIndex) * 2}ms`,
              }}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default CalendarHeatmapSkeleton;

