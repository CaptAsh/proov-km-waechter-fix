# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_does_not_crash_on_missing_reading():
    # VOS-7788 has no last_service_km: fleet_summary must not crash, and the average
    # must reflect only VOS-4471 (14900 km of 15000 → 99.33…%), not VOS-7788.
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},
    ]
    result = fleet_summary(fleet)
    assert result["count"] == 2
    expected_avg = 14900 / 15000 * 100   # only VOS-4471 contributes
    assert abs(result["average_wear"] - expected_avg) < 0.01
