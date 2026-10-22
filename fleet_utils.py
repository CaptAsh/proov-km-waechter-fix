# fleet_utils.py
# Utility helpers for the nightly fleet report.

KM_PER_MILE: float = 1.609344


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km / KM_PER_MILE


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"
