# tasks.py

import logging
from datetime import date as date_type, datetime, timedelta, time as dt_time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from celery import shared_task
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import DailyActivitySummary, Location, UserSettings, Visit

log = logging.getLogger(__name__)


@shared_task
def compute_daily_activity_summary(start_date=None, end_date=None):
    """
    Pre-compute daily location and visit counts grouped by the user's home
    timezone.

    If ``start_date`` / ``end_date`` are provided (ISO-format strings or
    ``datetime.date`` objects) only that range is processed.  Otherwise the
    past 365 days are used.

    Dates that are missing from DailyActivitySummary OR that have
    ``partial=True`` are (re-)computed.  Yesterday is always recomputed to
    correct any summary that was written mid-day.  The record for today is
    always written with ``partial=True``; all other records are written with
    ``partial=False``.
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

    today_in_tz = datetime.now(tz=user_tz).date()

    # Resolve date range
    if start_date is None:
        resolved_start = today_in_tz - timedelta(days=365)
    elif isinstance(start_date, str):
        resolved_start = date_type.fromisoformat(start_date)
    else:
        resolved_start = start_date

    if end_date is None:
        resolved_end = today_in_tz
    elif isinstance(end_date, str):
        resolved_end = date_type.fromisoformat(end_date)
    else:
        resolved_end = end_date

    # Collect every date in the window
    all_dates: set = set()
    current = resolved_start
    while current <= resolved_end:
        all_dates.add(current)
        current += timedelta(days=1)

    # Find which dates already have a non-partial summary
    existing_summaries = DailyActivitySummary.objects.filter(
        timezone=timezone_str,
        date__gte=resolved_start,
        date__lte=resolved_end,
    ).values("date", "partial")

    existing_dates = set()
    partial_dates = set()
    for s in existing_summaries:
        existing_dates.add(s["date"])
        if s["partial"]:
            partial_dates.add(s["date"])

    missing_dates = all_dates - existing_dates

    # Always recompute yesterday to fix any mid-day partial that wasn't flagged
    yesterday_in_tz = today_in_tz - timedelta(days=1)
    dates_to_compute = missing_dates | partial_dates
    if yesterday_in_tz in all_dates:
        dates_to_compute.add(yesterday_in_tz)

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
                "partial": target_date == today_in_tz,
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
