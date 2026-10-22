# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how much of the service interval has been used, as a percentage."""
    return km_since_service / interval * 100


def needs_service(car: dict) -> bool:
    """Return True if the car has used at least WARN_AT_PERCENT of its service interval."""
    if "last_service_km" not in car:
        return False
    km_since = car["odometer"] - car["last_service_km"]
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list:
    """Flag all cars due for service, print a notice for each, and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
