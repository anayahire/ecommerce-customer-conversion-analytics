"""Build the local SQLite database from validated raw data."""
from __future__ import annotations
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    database = ROOT / "data" / "ecommerce_analytics.sqlite"
    if database.exists(): database.unlink()
    connection = sqlite3.connect(database); connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript((ROOT / "sql" / "schema.sql").read_text())
    for table in ["customers", "products", "marketing_campaigns", "orders", "order_items", "customer_events"]:
        frame = pd.read_csv(ROOT / "data" / "raw" / f"{table}.csv")
        frame.where(pd.notna(frame), None).to_sql(table, connection, if_exists="append", index=False)
    connection.executescript((ROOT / "sql" / "views.sql").read_text())
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    if violations: raise RuntimeError(f"Foreign-key failures: {violations}")
    print(f"Created {database.name} with {connection.execute('SELECT COUNT(*) FROM orders').fetchone()[0]:,} orders.")
    connection.close()


if __name__ == "__main__": main()
