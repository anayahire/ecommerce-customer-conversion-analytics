"""Produce Power BI-ready facts, dimensions, and analytical summaries."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from rfm import build_rfm

ROOT = Path(__file__).resolve().parents[1]
INTERIM, PROCESSED = ROOT / "data" / "interim", ROOT / "data" / "processed"


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    frames = {p.stem: pd.read_csv(p) for p in INTERIM.glob("*.csv")}
    orders = frames["orders"]; orders["order_timestamp"] = pd.to_datetime(orders["order_timestamp"])
    events = frames["customer_events"]; events["event_timestamp"] = pd.to_datetime(events["event_timestamp"])
    orders["order_date"] = orders.order_timestamp.dt.date
    orders["order_month"] = orders.order_timestamp.dt.to_period("M").astype(str)
    orders["is_completed"] = (orders.order_status == "Completed").astype(int)
    events["event_date"] = events.event_timestamp.dt.date
    for name in ["customers", "products", "marketing_campaigns", "order_items"]: frames[name].to_csv(PROCESSED / f"{name}.csv", index=False)
    orders.to_csv(PROCESSED / "orders.csv", index=False); events.to_csv(PROCESSED / "customer_events.csv", index=False)
    rfm = build_rfm(orders, frames["customers"]); rfm.to_csv(PROCESSED / "customer_rfm.csv", index=False)
    stages = ["session_start", "product_view", "add_to_cart", "begin_checkout", "purchase"]
    funnel = events[events.event_name.isin(stages)].groupby("event_name").session_id.nunique().reindex(stages).reset_index(name="sessions")
    funnel["prior_sessions"] = funnel.sessions.shift(1); funnel["stage_conversion_rate"] = (funnel.sessions / funnel.prior_sessions).fillna(1).round(4)
    funnel.to_csv(PROCESSED / "funnel_summary.csv", index=False)
    dates = pd.date_range(orders.order_timestamp.min().normalize(), orders.order_timestamp.max().normalize(), freq="D")
    dim_date = pd.DataFrame({"date": dates}); dim_date["year"] = dates.year; dim_date["month"] = dates.month; dim_date["month_name"] = dates.strftime("%b"); dim_date["quarter"] = "Q" + dates.quarter.astype(str)
    dim_date.to_csv(PROCESSED / "dim_date.csv", index=False)
    print(f"Created processed tables, including {len(rfm):,} RFM records and {len(funnel)} funnel stages.")


if __name__ == "__main__": main()
