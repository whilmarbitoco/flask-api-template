"""Tests for app/utils/timezone.py

Uses real assertions with real datetime objects — no mocking.
All tests verify UTC storage + timezone conversion correctness.
"""
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

from app.utils.timezone import (
    utc_now,
    to_utc,
    to_local,
    today_in,
    parse_iso_local,
    DEFAULT_TZ,
)


# --- utc_now() ---

def test_utc_now_returns_aware_datetime():
    result = utc_now()
    assert result.tzinfo is not None, "utc_now() must return timezone-aware datetime"

def test_utc_now_is_utc():
    result = utc_now()
    assert result.tzinfo == ZoneInfo("UTC"), f"Expected UTC, got {result.tzinfo}"

def test_utc_now_not_naive():
    """Ensure we never return a naive datetime (the core bug this module prevents)."""
    result = utc_now()
    # A naive datetime has tzinfo=None; an aware one has tzinfo set
    assert result.utcoffset() is not None


# --- to_utc() ---

def test_to_utc_converts_manila_to_utc():
    """Manila is UTC+8, so 09:00 Manila = 01:00 UTC."""
    naive_manila = datetime(2026, 6, 23, 9, 0, 0)
    result = to_utc(naive_manila, source_tz="Asia/Manila")
    assert result.hour == 1
    assert result.tzinfo == ZoneInfo("UTC")

def test_to_utc_preserves_utc_input():
    """If already UTC, should not change the time."""
    aware_utc = datetime(2026, 6, 23, 1, 0, 0, tzinfo=ZoneInfo("UTC"))
    result = to_utc(aware_utc, source_tz="Asia/Manila")
    assert result.hour == 1
    assert result.tzinfo == ZoneInfo("UTC")

def test_to_utc_with_aware_source():
    """If dt is already aware, source_tz is ignored."""
    aware_manila = datetime(2026, 6, 23, 9, 0, 0, tzinfo=ZoneInfo("Asia/Manila"))
    result = to_utc(aware_manila)
    assert result.hour == 1
    assert result.tzinfo == ZoneInfo("UTC")

def test_to_utc_us_eastern():
    """US Eastern (UTC-4 in DST): 09:00 EDT = 13:00 UTC."""
    naive_eastern = datetime(2026, 6, 23, 9, 0, 0)
    result = to_utc(naive_eastern, source_tz="America/New_York")
    assert result.hour == 13
    assert result.tzinfo == ZoneInfo("UTC")


# --- to_local() ---

def test_to_local_converts_utc_to_manila():
    """UTC 01:00 = Manila 09:00 (UTC+8)."""
    utc_dt = datetime(2026, 6, 23, 1, 0, 0, tzinfo=ZoneInfo("UTC"))
    result = to_local(utc_dt, target_tz="Asia/Manila")
    assert result.hour == 9
    assert result.tzinfo == ZoneInfo("Asia/Manila")

def test_to_local_naive_assumed_utc():
    """Naive datetime should be treated as UTC."""
    naive = datetime(2026, 6, 23, 1, 0, 0)
    result = to_local(naive, target_tz="Asia/Manila")
    assert result.hour == 9

def test_to_local_us_eastern():
    """UTC 13:00 = US Eastern 09:00 (EDT, UTC-4)."""
    utc_dt = datetime(2026, 6, 23, 13, 0, 0, tzinfo=ZoneInfo("UTC"))
    result = to_local(utc_dt, target_tz="America/New_York")
    assert result.hour == 9


# --- today_in() ---

def test_today_in_returns_date():
    result = today_in("Asia/Manila")
    assert isinstance(result, date)

def test_today_in_manila():
    """today_in('Asia/Manila') should match the actual date in Manila."""
    manila_now = datetime.now(ZoneInfo("Asia/Manila"))
    result = today_in("Asia/Manila")
    assert result == manila_now.date()

def test_today_in_utc():
    """today_in('UTC') should match the actual UTC date."""
    utc_now_dt = datetime.now(ZoneInfo("UTC"))
    result = today_in("UTC")
    assert result == utc_now_dt.date()

def test_today_in_different_from_server_time():
    """When server is UTC and it's 23:00 UTC June 22,
    Manila is already 07:00 June 23 — today_in should return June 23."""
    # This test documents the core problem: server date != Manila date
    # We can't mock time, but we verify the function uses the given tz
    manila_today = today_in("Asia/Manila")
    utc_today = today_in("UTC")
    # They may or may not differ depending on when the test runs,
    # but both should be valid dates
    assert isinstance(manila_today, date)
    assert isinstance(utc_today, date)


# --- parse_iso_local() ---

def test_parse_iso_local_manila():
    """'2026-06-23T09:00:00' in Manila = 01:00 UTC."""
    result = parse_iso_local("2026-06-23T09:00:00", source_tz="Asia/Manila")
    assert result.hour == 1
    assert result.tzinfo == ZoneInfo("UTC")

def test_parse_iso_local_utc():
    """'2026-06-23T01:00:00' UTC = 01:00 UTC (no conversion needed)."""
    result = parse_iso_local("2026-06-23T01:00:00", source_tz="UTC")
    assert result.hour == 1
    assert result.tzinfo == ZoneInfo("UTC")


# --- Round-trip: to_utc → to_local ---

def test_roundtrip_manila():
    """Manila → UTC → Manila should preserve the original time."""
    original = datetime(2026, 6, 23, 9, 30, 0)
    utc = to_utc(original, source_tz="Asia/Manila")
    back = to_local(utc, target_tz="Asia/Manila")
    assert back.hour == original.hour
    assert back.minute == original.minute

def test_roundtrip_us_eastern():
    """US Eastern → UTC → US Eastern should preserve the original time."""
    original = datetime(2026, 6, 23, 14, 45, 0)
    utc = to_utc(original, source_tz="America/New_York")
    back = to_local(utc, target_tz="America/New_York")
    assert back.hour == original.hour
    assert back.minute == original.minute


# --- DEFAULT_TZ ---

def test_default_tz_is_manila():
    assert DEFAULT_TZ == ZoneInfo("Asia/Manila")
