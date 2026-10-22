# analyze.py
# Summary: km_since_service, avg_daily_km, and load_factor predict breakdown (+61%, +22%, +19%
# above the non-breakdown group mean). Total mileage (odometer_km) and age_years show <1%
# difference between groups — they look predictive but the data says otherwise.

import pandas as pd


# Columns that clearly separate broke_down=1 from broke_down=0:
RISK_COLS = ["km_since_service", "avg_daily_km", "load_factor"]

# Dropped columns and why:
#   odometer_km  — mean difference between groups is only +0.3%; pure noise.
#   age_years    — mean difference is -0.2%; older cars are NOT more likely to break down here.


def compare_groups(df: pd.DataFrame) -> None:
    """Print mean of each numeric column for the two breakdown groups side by side."""
    numeric = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
    g = df.groupby("broke_down")[numeric].mean()
    diff_pct = ((g.loc[1] - g.loc[0]) / g.loc[0] * 100)

    print("=== Group means (broke_down=0 vs 1) ===")
    header = f"{'column':<22}  {'no breakdown':>14}  {'broke down':>12}  {'diff %':>8}"
    print(header)
    print("-" * len(header))
    for col in numeric:
        marker = "  <-- kept" if col in RISK_COLS else "  (dropped)"
        print(
            f"{col:<22}  {g.loc[0, col]:>14.2f}  {g.loc[1, col]:>12.2f}"
            f"  {diff_pct[col]:>+7.1f}%{marker}"
        )
    print()


def min_max_scale(series: pd.Series) -> pd.Series:
    """Scale a series to [0, 1] using min-max normalisation."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


def build_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a 0-100 risk score for each car.

    Each kept column is min-max scaled to [0, 1]; the three scaled values are
    averaged and multiplied by 100 to give a single score.
    """
    scaled = pd.DataFrame(index=df.index)
    for col in RISK_COLS:
        scaled[col] = min_max_scale(df[col])
    df = df.copy()
    df["risk_score"] = (scaled.mean(axis=1) * 100).round(1)
    return df


def print_ranking(df: pd.DataFrame) -> None:
    """Print all cars ranked by risk score, highest first."""
    ranked = df.sort_values("risk_score", ascending=False).reset_index(drop=True)
    print("=== Cars ranked by breakdown risk (highest first) ===")
    header = f"{'rank':>4}  {'car_id':<12}  {'risk':>6}  {'km_since_svc':>14}  {'avg_daily_km':>13}  {'load':>6}  {'broke_down':>10}"
    print(header)
    print("-" * len(header))
    for i, row in ranked.iterrows():
        print(
            f"{i + 1:>4}  {row['car_id']:<12}  {row['risk_score']:>6.1f}"
            f"  {row['km_since_service']:>14.0f}  {row['avg_daily_km']:>13.0f}"
            f"  {row['load_factor']:>6.2f}  {'YES' if row['broke_down'] else 'no':>10}"
        )
    print()


def main() -> None:
    """Load fleet history, compare groups, build risk scores, print ranking."""
    df = pd.read_csv("fleet_history.csv")
    print(f"Loaded {len(df)} cars ({df['broke_down'].sum()} later broke down)\n")
    compare_groups(df)
    df = build_risk_scores(df)
    print_ranking(df)


if __name__ == "__main__":
    main()
