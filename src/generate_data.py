"""Create deterministic, relational synthetic data for the portfolio project."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20260909
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def weighted_choice(rng, values, weights, size):
    return rng.choice(values, p=np.array(weights) / np.sum(weights), size=size)


def make_products(rng: np.random.Generator) -> pd.DataFrame:
    catalog = {
        "Electronics": [("Audio", (25, 220)), ("Wearables", (55, 350)), ("Accessories", (12, 85))],
        "Home & Kitchen": [("Cookware", (20, 150)), ("Decor", (15, 120)), ("Storage", (10, 75))],
        "Fashion": [("Apparel", (18, 110)), ("Footwear", (35, 180)), ("Accessories", (10, 65))],
        "Beauty": [("Skincare", (12, 95)), ("Makeup", (10, 70)), ("Wellness", (15, 100))],
        "Sports": [("Fitness", (20, 250)), ("Outdoor", (18, 160)), ("Athleisure", (20, 95))],
    }
    brands = ["Nova", "Harbor", "Aster", "Mosaic", "Summit", "Luma", "Cedar", "Orbit"]
    rows, product_no = [], 1
    for category, groups in catalog.items():
        for subcategory, (low, high) in groups:
            for n in range(12):
                price = round(float(rng.uniform(low, high)), 2)
                rows.append({
                    "product_id": f"P{product_no:04d}", "sku": f"{category[:3].upper()}-{product_no:05d}",
                    "product_name": f"{brands[product_no % len(brands)]} {subcategory} {n + 1}",
                    "category": category, "subcategory": subcategory,
                    "brand": brands[product_no % len(brands)], "list_price": price,
                    "unit_cost": round(price * float(rng.uniform(.32, .58)), 2),
                    "active_status": "Active" if rng.random() > .08 else "Discontinued",
                })
                product_no += 1
    return pd.DataFrame(rows)


def make_customers(rng: np.random.Generator) -> pd.DataFrame:
    n = 3000
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    signup = rng.choice(dates, size=n)
    channels = weighted_choice(rng, ["Organic Search", "Paid Search", "Social", "Email", "Referral", "Direct"],
                               [26, 18, 19, 13, 9, 15], n)
    return pd.DataFrame({
        "customer_id": [f"C{i:05d}" for i in range(1, n + 1)], "signup_date": pd.to_datetime(signup),
        "age_group": weighted_choice(rng, ["18-24", "25-34", "35-44", "45-54", "55+"], [12, 34, 28, 17, 9], n),
        "gender": weighted_choice(rng, ["Female", "Male", "Non-binary", "Prefer not to say"], [49, 46, 2, 3], n),
        "city": weighted_choice(rng, ["New York", "Los Angeles", "Chicago", "Houston", "Seattle", "Austin", "Miami", "Denver"],
                                 [19, 16, 14, 12, 10, 10, 10, 9], n),
        "acquisition_channel": channels,
        "customer_status": weighted_choice(rng, ["Active", "At Risk", "Churned"], [60, 23, 17], n),
    }).sort_values("customer_id")


def make_campaigns(rng: np.random.Generator) -> pd.DataFrame:
    profiles = [("Paid Search", "Google", "cpc", .058), ("Paid Social", "Meta", "paid_social", .029),
                ("Email", "Klaviyo", "email", .082), ("Affiliate", "Partner Network", "affiliate", .041),
                ("Display", "Google Display", "display", .012)]
    rows = []
    for i in range(1, 26):
        channel, source, medium, conversion_rate = profiles[(i - 1) % len(profiles)]
        # Overlapping campaigns run throughout the one-year analysis window.
        start = pd.Timestamp("2025-01-01") + pd.Timedelta(days=int((i - 1) * 14))
        end = min(start + pd.Timedelta(days=int(rng.integers(30, 75))), pd.Timestamp("2025-12-31"))
        impressions = int(rng.integers(35_000, 180_000))
        ctr = {"Email": .075, "Paid Search": .052, "Paid Social": .017, "Affiliate": .025, "Display": .006}[channel]
        clicks = int(impressions * rng.uniform(ctr * .78, ctr * 1.22))
        rows.append({"campaign_id": f"CMP{i:03d}", "campaign_name": f"{channel} Growth {i:02d}", "channel": channel,
                     "source": source, "medium": medium, "start_date": start, "end_date": end,
                     "spend": round(clicks * rng.uniform(.35, 2.9), 2), "impressions": impressions,
                     "clicks": clicks, "conversions": int(clicks * rng.uniform(conversion_rate * .7, conversion_rate * 1.3))})
    return pd.DataFrame(rows)


def seasonal_weights(days: pd.DatetimeIndex) -> np.ndarray:
    w = np.ones(len(days))
    w[(days.month == 11) | (days.month == 12)] *= 2.3
    w[days.month == 7] *= 1.35
    w[days.dayofweek >= 5] *= 1.15
    return w / w.sum()


def make_orders_and_items(rng, customers, products, campaigns):
    # 22% never purchase; purchasers have deliberately different repeat propensities.
    purchasers = customers.loc[rng.random(len(customers)) > .22].copy()
    behavior = weighted_choice(rng, ["one_time", "occasional", "loyal", "high_value"], [.37, .39, .19, .05], len(purchasers))
    counts = np.select([behavior == "one_time", behavior == "occasional", behavior == "loyal"],
                       [1, rng.integers(2, 5, len(purchasers)), rng.integers(5, 11, len(purchasers))], default=rng.integers(10, 18, len(purchasers)))
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    product_weights = products.list_price.to_numpy() ** -.18
    rows, item_rows, order_no, item_no = [], [], 1, 1
    for customer, count in zip(purchasers.itertuples(index=False), counts):
        eligible = dates[dates >= max(pd.Timestamp(customer.signup_date), dates.min())]
        if not len(eligible):
            continue
        order_days = rng.choice(eligible, size=int(count), replace=True, p=seasonal_weights(eligible))
        for day in order_days:
            status = weighted_choice(rng, ["Completed", "Returned", "Cancelled"], [.89, .07, .04], 1)[0]
            order_id = f"O{order_no:06d}"; order_no += 1
            n_items = int(weighted_choice(rng, [1, 2, 3, 4], [.43, .34, .17, .06], 1)[0])
            selected = rng.choice(products.index, size=n_items, replace=False, p=product_weights / product_weights.sum())
            total_gross = total_discount = total_cost = 0.0
            for idx in selected:
                product = products.loc[idx]
                quantity = int(weighted_choice(rng, [1, 2, 3], [.76, .19, .05], 1)[0])
                price = round(float(product.list_price) * rng.uniform(.92, 1.03), 2)
                discount = round(price * quantity * (rng.uniform(.03, .18) if rng.random() < .47 else 0), 2)
                revenue = round(price * quantity - discount, 2); cost = round(float(product.unit_cost) * quantity, 2)
                total_gross += price * quantity; total_discount += discount; total_cost += cost
                item_rows.append({"order_item_id": f"OI{item_no:07d}", "order_id": order_id, "product_id": product.product_id,
                                  "quantity": quantity, "unit_price": price, "discount": discount, "item_revenue": revenue,
                                  "item_cost": cost, "item_margin": round(revenue - cost, 2)})
                item_no += 1
            shipping = 0 if total_gross >= 75 else 6.99
            tax = round((total_gross - total_discount + shipping) * .0825, 2)
            net = round(total_gross - total_discount + shipping + tax, 2)
            timestamp = pd.Timestamp(day) + pd.Timedelta(hours=int(rng.integers(8, 23)), minutes=int(rng.integers(60)))
            active_campaigns = campaigns[(campaigns.start_date <= day) & (campaigns.end_date >= day)].campaign_id.to_numpy()
            campaign = rng.choice(active_campaigns) if len(active_campaigns) and rng.random() < .42 else None
            rows.append({"order_id": order_id, "customer_id": customer.customer_id, "order_timestamp": timestamp, "order_status": status,
                         "currency": "USD", "gross_sales": round(total_gross, 2), "discount": round(total_discount, 2),
                         "shipping": shipping, "tax": tax, "net_revenue": net if status != "Cancelled" else 0.0, "campaign_id": campaign})
    return pd.DataFrame(rows), pd.DataFrame(item_rows)


def make_events(rng, customers, products, orders, items, campaigns):
    rows, event_no, session_no = [], 1, 1
    channels = {"Organic Search": ("Organic Search", "google", "organic"), "Paid Search": ("Paid Search", "google", "cpc"),
                "Social": ("Social", "instagram", "social"), "Email": ("Email", "klaviyo", "email"),
                "Referral": ("Referral", "partner", "referral"), "Direct": ("Direct", "direct", "none")}
    orders_by_customer = {k: g.sort_values("order_timestamp") for k, g in orders[orders.order_status == "Completed"].groupby("customer_id")}
    products_by_order = items.groupby("order_id").product_id.apply(list).to_dict()
    # Purchasers receive a purchase journey; extra browsing sessions yield realistic drop-off.
    for customer in customers.itertuples(index=False):
        completed = orders_by_customer.get(customer.customer_id, pd.DataFrame())
        extra = int(rng.integers(1, 5) if len(completed) else rng.integers(1, 4))
        sessions = [(r.order_timestamp, r.order_id, True) for r in completed.itertuples(index=False)]
        for _ in range(extra):
            sessions.append((pd.Timestamp(rng.choice(pd.date_range(max(pd.Timestamp(customer.signup_date), pd.Timestamp("2025-01-01")), "2025-12-31"))) + pd.Timedelta(hours=int(rng.integers(8, 23))), None, False))
        for ts, order_id, purchased in sessions:
            session = f"S{session_no:07d}"; session_no += 1
            campaign = orders.loc[orders.order_id == order_id, "campaign_id"].iloc[0] if purchased else None
            channel, source, medium = channels[customer.acquisition_channel]
            if pd.notna(campaign):
                camp = campaigns.loc[campaigns.campaign_id == campaign].iloc[0]; channel, source, medium = camp.channel, camp.source, camp.medium
            product_id = rng.choice(products_by_order[order_id]) if purchased else rng.choice(products.product_id)
            stages = ["session_start", "product_view"]
            added_to_cart = purchased or rng.random() < .48
            if added_to_cart: stages.append("add_to_cart")
            if added_to_cart and (purchased or rng.random() < .53): stages.append("begin_checkout")
            if purchased: stages.append("purchase")
            for step, event in enumerate(stages):
                rows.append({"event_id": f"E{event_no:08d}", "event_timestamp": ts + pd.Timedelta(minutes=step * int(rng.integers(1, 8))),
                             "session_id": session, "customer_id": customer.customer_id, "event_name": event,
                             "product_id": product_id if event != "session_start" else None, "order_id": order_id if event == "purchase" else None,
                             "device": weighted_choice(rng, ["Mobile", "Desktop", "Tablet"], [62, 33, 5], 1)[0], "channel": channel,
                             "source": source, "medium": medium, "campaign_id": campaign})
                event_no += 1
    return pd.DataFrame(rows)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    products = make_products(rng); customers = make_customers(rng); campaigns = make_campaigns(rng)
    orders, items = make_orders_and_items(rng, customers, products, campaigns)
    events = make_events(rng, customers, products, orders, items, campaigns)
    for name, frame in {"customers": customers, "products": products, "orders": orders, "order_items": items,
                        "marketing_campaigns": campaigns, "customer_events": events}.items():
        frame.to_csv(RAW / f"{name}.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
        print(f"Wrote {name}: {len(frame):,} rows")


if __name__ == "__main__":
    main()
