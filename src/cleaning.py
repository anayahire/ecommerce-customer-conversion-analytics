"""Clean raw CSVs without changing their business meaning."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, INTERIM = ROOT / "data" / "raw", ROOT / "data" / "interim"
DATE_COLUMNS = {"customers": ["signup_date"], "orders": ["order_timestamp"], "marketing_campaigns": ["start_date", "end_date"], "customer_events": ["event_timestamp"]}


def main() -> None:
    INTERIM.mkdir(parents=True, exist_ok=True)
    for path in RAW.glob("*.csv"):
        frame = pd.read_csv(path)
        for col in DATE_COLUMNS.get(path.stem, []): frame[col] = pd.to_datetime(frame[col])
        # String IDs are preserved; only nullable foreign keys are represented as blank cells in CSV.
        frame.to_csv(INTERIM / path.name, index=False, date_format="%Y-%m-%d %H:%M:%S")
        print(f"Cleaned {path.name}: {len(frame):,} rows")


if __name__ == "__main__": main()
