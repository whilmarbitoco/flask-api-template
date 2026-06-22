"""Timezone utilities for Flask API template.

All datetimes are stored in UTC in the database. Conversion to/from
the client's local timezone happens at the API boundary (routes/schemas).

Defaults to Asia/Manila (UTC+8) for Philippine deployments.
Override via the DEFAULT_TIMEZONE env var or per-user timezone field.
"""

from datetime import datetime, date
from zoneinfo import ZoneInfo  # Python 3.9+ stdlib — prefer over pytz

DEFAULT_TZ = ZoneInfo("Asia/Manila")


def utc_now() -> datetime:
    """Return timezone-aware UTC datetime. Use this instead of datetime.utcnow()."""
    return datetime.now(ZoneInfo("UTC"))


def to_utc(dt: datetime, source_tz: str = "Asia/Manila") -> datetime:
    """Convert a naive or aware datetime from source_tz to UTC.

    If dt is naive, it is assumed to be in source_tz.
    If dt is already aware, source_tz is ignored.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(source_tz))
    return dt.astimezone(ZoneInfo("UTC"))


def to_local(dt: datetime, target_tz: str = "Asia/Manila") -> datetime:
    """Convert a UTC datetime to target timezone for display/serialization.

    If dt is naive, it is assumed to be UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(ZoneInfo(target_tz))


def today_in(tz: str = "Asia/Manila") -> date:
    """Return today's date in the given timezone.

    Use this for cron/scheduler date comparisons instead of date.today()
    which uses the server's local time.
    """
    return datetime.now(ZoneInfo(tz)).date()


def parse_iso_local(iso_string: str, source_tz: str = "Asia/Manila") -> datetime:
    """Parse an ISO 8601 string as a local datetime and convert to UTC.

    Example: "2026-06-23T09:00:00" → UTC datetime
    """
    dt = datetime.fromisoformat(iso_string)
    return to_utc(dt, source_tz)
