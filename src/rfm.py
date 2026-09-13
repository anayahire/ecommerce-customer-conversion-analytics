"""RFM scoring functions shared by notebooks and the processing pipeline."""
from __future__ import annotations
import pandas as pd


def build_rfm(orders: pd.DataFrame, customers: pd.DataFrame, as_of_date: str = "2026-01-01") -> pd.DataFrame:
    completed = orders.loc[orders["order_status"] == "Completed"].copy()
    completed["order_timestamp"] = pd.to_datetime(completed["order_timestamp"])
    summary = completed.groupby("customer_id").agg(last_order=("order_timestamp", "max"), frequency=("order_id", "nunique"), monetary=("net_revenue", "sum")).reset_index()
    result = customers[["customer_id"]].merge(summary, on="customer_id", how="left")
    result["recency_days"] = (pd.Timestamp(as_of_date) - result["last_order"]).dt.days
    result[["frequency", "monetary"]] = result[["frequency", "monetary"]].fillna(0)
    result["recency_days"] = result["recency_days"].fillna(999).astype(int)
    # Higher score is better; non-buyers remain explicitly identifiable.
    buyers = result["frequency"] > 0
    result["r_score"] = 1; result["f_score"] = 1; result["m_score"] = 1
    # Recent, frequent, and high-spend customers each receive higher scores.
    recency_ranks = result.loc[buyers, "recency_days"].rank(method="first", ascending=True)
    result.loc[buyers, "r_score"] = pd.qcut(recency_ranks, 5, labels=[5, 4, 3, 2, 1]).astype(int).to_numpy()
    for column, score in [("frequency", "f_score"), ("monetary", "m_score")]:
        ranks = result.loc[buyers, column].rank(method="first", ascending=True)
        result.loc[buyers, score] = pd.qcut(ranks, 5, labels=[1, 2, 3, 4, 5]).astype(int).to_numpy()
    result["rfm_score"] = result[["r_score", "f_score", "m_score"]].sum(axis=1)
    result["rfm_segment"] = "Needs Activation"
    result.loc[buyers & (result.f_score >= 4) & (result.m_score >= 4), "rfm_segment"] = "Loyal High Value"
    # Apply the narrower Champions rule after Loyal High Value so it takes precedence.
    result.loc[buyers & (result.r_score >= 4) & (result.f_score >= 4), "rfm_segment"] = "Champions"
    result.loc[buyers & (result.r_score >= 4) & (result.f_score <= 2), "rfm_segment"] = "New Customers"
    result.loc[buyers & (result.r_score <= 2) & (result.f_score >= 3), "rfm_segment"] = "At Risk"
    result.loc[buyers & (result.r_score <= 2) & (result.f_score <= 2), "rfm_segment"] = "Hibernating"
    return result.drop(columns="last_order")
