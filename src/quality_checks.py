"""Validate raw and processed data before it is used for analysis."""
from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REQUIRED = {
    "customers": ["customer_id", "signup_date", "age_group", "gender", "city", "acquisition_channel", "customer_status"],
    "products": ["product_id", "sku", "product_name", "category", "subcategory", "brand", "list_price", "unit_cost", "active_status"],
    "orders": ["order_id", "customer_id", "order_timestamp", "order_status", "currency", "gross_sales", "discount", "shipping", "tax", "net_revenue", "campaign_id"],
    "order_items": ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount", "item_revenue", "item_cost", "item_margin"],
    "marketing_campaigns": ["campaign_id", "campaign_name", "channel", "source", "medium", "start_date", "end_date", "spend", "impressions", "clicks", "conversions"],
    "customer_events": ["event_id", "event_timestamp", "session_id", "customer_id", "event_name", "product_id", "order_id", "device", "channel", "source", "medium", "campaign_id"],
}


def load_raw() -> dict[str, pd.DataFrame]:
    date_columns = {
        "customers": ["signup_date"], "orders": ["order_timestamp"],
        "marketing_campaigns": ["start_date", "end_date"], "customer_events": ["event_timestamp"],
    }
    return {name: pd.read_csv(RAW / f"{name}.csv", parse_dates=date_columns.get(name, [])) for name in REQUIRED}


def validate(frames: dict[str, pd.DataFrame]) -> list[str]:
    issues = []
    for name, columns in REQUIRED.items():
        frame = frames[name]
        missing = set(columns) - set(frame.columns)
        if missing: issues.append(f"{name}: missing columns {sorted(missing)}")
        key = columns[0]
        if frame[key].isna().any() or frame[key].duplicated().any(): issues.append(f"{name}: {key} must be unique and non-null")
    customers, products, orders, items, campaigns, events = (frames[k] for k in REQUIRED)
    checks = [
        (set(orders.customer_id) <= set(customers.customer_id), "orders.customer_id has orphan records"),
        (set(items.order_id) <= set(orders.order_id), "order_items.order_id has orphan records"),
        (set(items.product_id) <= set(products.product_id), "order_items.product_id has orphan records"),
        (set(events.customer_id) <= set(customers.customer_id), "customer_events.customer_id has orphan records"),
        (set(events.product_id.dropna()) <= set(products.product_id), "customer_events.product_id has orphan records"),
        (set(events.order_id.dropna()) <= set(orders.order_id), "customer_events.order_id has orphan records"),
        (set(orders.campaign_id.dropna()) <= set(campaigns.campaign_id), "orders.campaign_id has orphan records"),
        (set(events.campaign_id.dropna()) <= set(campaigns.campaign_id), "customer_events.campaign_id has orphan records"),
    ]
    issues.extend(message for ok, message in checks if not ok)
    expected_stages = {"session_start", "product_view", "add_to_cart", "begin_checkout", "purchase"}
    if set(events.event_name.unique()) != expected_stages: issues.append("Funnel stages must match the required five stages")
    for prior, current in zip(["session_start", "product_view", "add_to_cart", "begin_checkout"], ["product_view", "add_to_cart", "begin_checkout", "purchase"]):
        prior_sessions = set(events.loc[events.event_name == prior, "session_id"])
        current_sessions = set(events.loc[events.event_name == current, "session_id"])
        if not current_sessions <= prior_sessions: issues.append(f"Funnel sessions reach {current} without {prior}")
    if (products.unit_cost > products.list_price).any(): issues.append("Product cost exceeds list price")
    if (items.item_margin.round(2) != (items.item_revenue - items.item_cost).round(2)).any(): issues.append("Invalid item margin calculation")
    if (orders.net_revenue < 0).any() or (items.quantity <= 0).any(): issues.append("Negative revenue or non-positive quantity")
    order_totals = items.assign(line_gross=items.quantity * items.unit_price).groupby("order_id").agg(item_gross_sales=("line_gross", "sum"), item_discount=("discount", "sum"))
    reconciled = orders.set_index("order_id").join(order_totals)
    if not (reconciled.gross_sales.round(2) == reconciled.item_gross_sales.round(2)).all(): issues.append("Order gross sales do not reconcile to order items")
    if not (reconciled.discount.round(2) == reconciled.item_discount.round(2)).all(): issues.append("Order discounts do not reconcile to order items")
    cancelled = orders[orders.order_status == "Cancelled"]
    if not (cancelled.net_revenue == 0).all(): issues.append("Cancelled orders must have zero net revenue")
    purchase_orders = set(events.loc[events.event_name == "purchase", "order_id"].dropna())
    completed_orders = set(orders.loc[orders.order_status == "Completed", "order_id"])
    if not purchase_orders <= completed_orders: issues.append("Purchase events must reference completed orders")
    purchase_events = events.loc[events.event_name == "purchase", ["order_id", "product_id"]].dropna()
    valid_purchase_items = set(map(tuple, items[["order_id", "product_id"]].to_numpy()))
    if not set(map(tuple, purchase_events.to_numpy())) <= valid_purchase_items: issues.append("Purchase event products do not match order items")
    if (campaigns.end_date < campaigns.start_date).any(): issues.append("Campaign end dates precede start dates")
    if (campaigns.spend < 0).any() or (campaigns.clicks > campaigns.impressions).any() or (campaigns.conversions > campaigns.clicks).any(): issues.append("Invalid campaign performance metrics")
    completed_counts = orders.loc[orders.order_status == "Completed"].groupby("customer_id").order_id.nunique()
    if not (len(completed_counts) < len(customers) and (completed_counts == 1).any() and (completed_counts > 1).any()): issues.append("Customer purchase behavior lacks non-buyers, one-time buyers, or repeat buyers")
    if orders.order_timestamp.min() > pd.Timestamp("2025-01-31") or orders.order_timestamp.max() < pd.Timestamp("2025-12-01"): issues.append("Order dates do not span the analysis year")
    return issues


def main() -> None:
    frames = load_raw(); issues = validate(frames)
    for name, frame in frames.items(): print(f"{name}: {len(frame):,} rows")
    if issues:
        print("VALIDATION FAILED:", *issues, sep="\n- "); sys.exit(1)
    print("VALIDATION PASSED: schemas, keys, foreign keys, funnel stages, and business rules are valid.")


if __name__ == "__main__": main()
