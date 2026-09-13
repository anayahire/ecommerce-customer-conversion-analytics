-- SQLite warehouse schema for the generated e-commerce analytics data.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    signup_date TEXT NOT NULL,
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    city TEXT NOT NULL,
    acquisition_channel TEXT NOT NULL,
    customer_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    brand TEXT NOT NULL,
    list_price REAL NOT NULL,
    unit_cost REAL NOT NULL,
    active_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marketing_campaigns (
    campaign_id TEXT PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    channel TEXT NOT NULL,
    source TEXT NOT NULL,
    medium TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    spend REAL NOT NULL,
    impressions INTEGER NOT NULL,
    clicks INTEGER NOT NULL,
    conversions INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    order_timestamp TEXT NOT NULL,
    order_status TEXT NOT NULL,
    currency TEXT NOT NULL,
    gross_sales REAL NOT NULL,
    discount REAL NOT NULL,
    shipping REAL NOT NULL,
    tax REAL NOT NULL,
    net_revenue REAL NOT NULL,
    campaign_id TEXT REFERENCES marketing_campaigns(campaign_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    product_id TEXT NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL,
    discount REAL NOT NULL,
    item_revenue REAL NOT NULL,
    item_cost REAL NOT NULL,
    item_margin REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_events (
    event_id TEXT PRIMARY KEY,
    event_timestamp TEXT NOT NULL,
    session_id TEXT NOT NULL,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    event_name TEXT NOT NULL CHECK (event_name IN (
        'session_start', 'product_view', 'add_to_cart', 'begin_checkout', 'purchase'
    )),
    product_id TEXT REFERENCES products(product_id),
    order_id TEXT REFERENCES orders(order_id),
    device TEXT NOT NULL,
    channel TEXT NOT NULL,
    source TEXT NOT NULL,
    medium TEXT NOT NULL,
    campaign_id TEXT REFERENCES marketing_campaigns(campaign_id)
);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_events_session ON customer_events(session_id);
