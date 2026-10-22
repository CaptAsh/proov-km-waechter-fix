# What I checked, and what the agent got wrong

## What the agent got wrong
IBM Bob did most of the work well, but I caught several mistakes by reading its answers and diffs instead of trusting them:

- In its first summary it called Vossberg Mobility a "car-rental company". TASK.md says it runs a fleet of sports cars.
- It suggested replacing `== True` with `is True`. The correct modern style is to drop the comparison completely: `if needs_service(car):`.
- It explained `split("=")` wrongly ("only splits on the first ="). It actually splits on every "=", and the old code then threw away everything after the second one. The fix is `split("=", 1)`.
- Its first test for the missing reading said in a comment that the car is left out of the average, but the test never checked that. I asked Bob to strengthen it, and now it asserts the exact average.
- It told me analyze.py was mine to write alone, but TASK.md step 9 says to do it with Bob. Only NOTES.md is mine.
- In its first review it missed that `format_percent` was dead code and that the report printed the average with `%d`, which would cut 59.7% down to 59%.

## What I checked before I accepted its work
- I read every diff before committing, and checked that `SERVICE_INTERVAL_KM = 15000` and `WARN_AT_PERCENT = 80` (and settings.cfg) were never changed.
- I ran pytest and `python verify.py` after each step instead of trusting "done". The car at 14,900 of 15,000 km now shows 99.3% and is flagged; a car with no last-service reading is not flagged and is left out of the average.
- Before Bob deleted dead code, I made it search the repo first. I made sure `get_int` stayed, because verify.py uses it.
- I saw that unknown keys in settings.cfg are still silently ignored. I left that on purpose, because changing how the config behaves was outside the scope of this task.
- I committed in small steps so each change could be reviewed on its own.

## What the data actually said
I compared the 26 cars that broke down with the 94 that did not, column by column:

| Column | Broke down | Kept going |
|---|---|---|
| km_since_service | 11,678 km | 7,261 km |
| avg_daily_km | 160 km/day | 131 km/day |
| load_factor | 0.60 | 0.51 |
| odometer_km | 53,448 km | 53,302 km |
| age_years | 5.9 | 5.9 |

The factors that predict a breakdown are km since the last service, how hard the car is driven each day, and how heavily it is loaded. Total mileage and age, the "obvious" answers, are almost identical in both groups, so they do not predict anything here. The risk score in analyze.py therefore uses only the three columns that separate the groups.

The score is a simple ranking, not a perfect predictor: of the 26 highest-scored cars, 13 actually broke down. It is useful for deciding which cars to inspect first, alongside the 80% rule, not instead of it.