# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Runs every morning. Never cleaned up.

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car):
    if "last_service_km" not in car:
        return None
    return wear_percent(car["odometer"] - car["last_service_km"], SERVICE_INTERVAL_KM)


def fleet_summary(fleet):
    due = 0
    wear_values = []
    for car in fleet:
        w = car_wear(car)
        if w is not None:
            wear_values.append(w)
        if needs_service(car):
            due += 1
    average = sum(wear_values) / len(wear_values) if wear_values else 0.0
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet):
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print("Fleet: %d cars" % s["count"])
    print("Due for service: %d" % s["due"])
    print("Average wear: %.1f%%" % s["average_wear"])
    total_km = 0
    for car in fleet:
        total_km = total_km + car["odometer"]
    # Die Partnerwerkstatt in England will die Distanz in Meilen (seit 2015).
    # (The partner garage in England wants the distance in miles, since 2015.)
    print("Fleet distance: %s miles" % fleet_utils.format_number(fleet_utils.km_to_miles(total_km)))
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
