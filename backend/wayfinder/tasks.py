# tasks.py

import logging
from datetime import datetime, timedelta, time as dt_time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from celery import shared_task
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import DailyActivitySummary, Location, UserSettings, Visit

log = logging.getLogger(__name__)


@shared_task
def compute_daily_activity_summary():
    """
    Pre-compute daily location and visit counts grouped by the user's home
    timezone.  Only dates that are not yet in DailyActivitySummary are
    computed; today (in the user's timezone) is always recomputed so that
    data arriving throughout the day is captured on the next beat run.
    """

    # Determine the timezone to use
    try:
        user_settings = UserSettings.objects.first()
        timezone_str = user_settings.home_timezone if user_settings else "UTC"
    except Exception:
        timezone_str = "UTC"

    try:
        user_tz = ZoneInfo(timezone_str)
    except ZoneInfoNotFoundError:
        log.warning("Invalid timezone '%s', falling back to UTC", timezone_str)
        timezone_str = "UTC"
        user_tz = ZoneInfo("UTC")

    log.info("Computing daily activity summary for timezone: %s", timezone_str)

    # Date range: past 365 days in the user's timezone
    today_in_tz = datetime.now(tz=user_tz).date()
    start_date = today_in_tz - timedelta(days=365)

    # Collect every date in the window
    all_dates: set = set()
    current = start_date
    while current <= today_in_tz:
        all_dates.add(current)
        current += timedelta(days=1)

    # Find which dates already have a summary
    existing_dates = set(
        DailyActivitySummary.objects.filter(
            timezone=timezone_str,
            date__gte=start_date,
            date__lte=today_in_tz,
        ).values_list("date", flat=True)
    )

    # Always recompute today and yesterday: today captures intraday updates, yesterday
    # corrects any partial summary that was computed mid-day (e.g. by the bootstrap trigger).
    yesterday_in_tz = today_in_tz - timedelta(days=1)
    dates_to_compute = (all_dates - existing_dates) | {today_in_tz, yesterday_in_tz}

    log.info("Dates to compute: %d", len(dates_to_compute))

    if not dates_to_compute:
        return

    # Build a timezone-aware datetime range that covers all target dates
    min_date = min(dates_to_compute)
    max_date = max(dates_to_compute)
    min_dt = datetime.combine(min_date, dt_time.min, tzinfo=user_tz)
    max_dt = datetime.combine(max_date, dt_time.max, tzinfo=user_tz)

    # Aggregate location counts grouped by date in the user's timezone
    location_counts = (
        Location.objects.filter(time__gte=min_dt, time__lte=max_dt)
        .annotate(date=TruncDate("time", tzinfo=user_tz))
        .values("date")
        .annotate(count=Count("id"))
    )
    location_dict = {item["date"]: item["count"] for item in location_counts}

    # Aggregate visit counts grouped by date in the user's timezone
    visit_counts = (
        Visit.objects.filter(time__gte=min_dt, time__lte=max_dt)
        .annotate(date=TruncDate("time", tzinfo=user_tz))
        .values("date")
        .annotate(count=Count("id"))
    )
    visit_dict = {item["date"]: item["count"] for item in visit_counts}

    created_count = 0
    updated_count = 0
    for target_date in dates_to_compute:
        _, created = DailyActivitySummary.objects.update_or_create(
            date=target_date,
            timezone=timezone_str,
            defaults={
                "location_count": location_dict.get(target_date, 0),
                "visit_count": visit_dict.get(target_date, 0),
            },
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    log.info(
        "Daily activity summary: created %d, updated %d",
        created_count,
        updated_count,
    )
