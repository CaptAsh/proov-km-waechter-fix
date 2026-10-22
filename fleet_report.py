# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float | None:
    """Return wear percentage for a car, or None if no last-service reading exists."""
    if "last_service_km" not in car:
        return None
    return wear_percent(car["odometer"] - car["last_service_km"], SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[dict]) -> dict:
    """Summarise the fleet: total count, cars due for service, and average wear."""
    due = 0
    wear_values: list[float] = []
    for car in fleet:
        w = car_wear(car)
        if w is not None:
            wear_values.append(w)
        if needs_service(car):
            due += 1
    average = sum(wear_values) / len(wear_values) if wear_values else 0.0
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list[dict]) -> None:
    """Print the nightly fleet report and flush the log."""
    settings = load_settings()
    log(settings.get("report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = sum(car["odometer"] for car in fleet)
    # The partner garage in England wants the distance in miles (since 2015).
    print(f"Fleet distance: {fleet_utils.format_number(fleet_utils.km_to_miles(total_km))} miles")
    flush_log(settings.get("log_file", "km_wachter.log"))
