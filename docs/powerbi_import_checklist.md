# Power BI import checklist

All paths below are repository-relative, so the checklist works from any clone.

## Files to import

Import these eight files. `funnel_summary.csv` is listed for reconciliation only; do **not** load it into the interactive model.

| Load | File path | Rows | Model table |
|---|---|---:|---|
| 1 | `data/processed/dim_date.csv` | 365 | `dim_date` |
| 2 | `data/processed/customers.csv` | 3,000 | `customers` |
| 3 | `data/processed/customer_rfm.csv` | 3,000 | `customer_rfm` |
| 4 | `data/processed/products.csv` | 180 | `products` |
| 5 | `data/processed/marketing_campaigns.csv` | 25 | `marketing_campaigns` |
| 6 | `data/processed/orders.csv` | 8,438 | `orders` |
| 7 | `data/processed/order_items.csv` | 15,743 | `order_items` |
| 8 | `data/processed/customer_events.csv` | 57,166 | `customer_events` |
| Do not load | `data/processed/funnel_summary.csv` | 5 | Static validation output only |

## Compact build order

1. Import `dim_date`; set `date` to Date and mark it as the date table.
2. Import `customers` and `customer_rfm`; set their IDs to Text.
3. Import `products` and `marketing_campaigns`; set IDs to Text and money to Fixed decimal/currency.
4. Import `orders`; set `order_date` to Date, `order_timestamp` to Date/Time, and money to Fixed decimal/currency.
5. Import `order_items`; set money to Fixed decimal/currency.
6. Import `customer_events`; set `event_date` to Date and `event_timestamp` to Date/Time.
7. Create the relationships below, hide technical columns, then create the documented DAX measures.

## Table schemas, fields, and report roles

### `dim_date` — 365 rows

Primary key: `date`. Foreign keys: none. Use as the shared date dimension.

| Column | Power BI type | Use |
|---|---|---|
| `date` | Date | Date slicer, relationship key, chart axis |
| `year` | Whole number | Slicer/axis |
| `month` | Whole number | Sort key; hide after setting `month_name` sort |
| `month_name` | Text | Axis/slicer |
| `quarter` | Text | Axis/slicer |

### `customers` — 3,000 rows

Primary key: `customer_id`. Foreign keys: none.

| Column | Power BI type | Use |
|---|---|---|
| `customer_id` | Text | Hide; relationship and measures |
| `signup_date` | Date | Optional customer cohort slicer/visual |
| `age_group` | Text | Slicer/legend |
| `gender` | Text | Slicer/legend |
| `city` | Text | Slicer/axis/map |
| `acquisition_channel` | Text | Slicer/axis |
| `customer_status` | Text | Slicer/legend |

### `customer_rfm` — 3,000 rows

Primary key: `customer_id`. Foreign key: `customer_id → customers[customer_id]`.

| Column | Power BI type | Use |
|---|---|---|
| `customer_id` | Text | Hide; relationship key |
| `frequency` | Decimal number | Hide by default; customer-detail table only |
| `monetary` | Fixed decimal/currency | Hide by default; customer-detail table only |
| `recency_days` | Whole number | RFM distribution/tooltip |
| `r_score` | Whole number | RFM matrix/legend |
| `f_score` | Whole number | RFM matrix/legend |
| `m_score` | Whole number | RFM matrix/legend |
| `rfm_score` | Whole number | Distribution/tooltip |
| `rfm_segment` | Text | Slicer, axis, legend |

### `products` — 180 rows

Primary key: `product_id`. Foreign keys: none.

| Column | Power BI type | Use |
|---|---|---|
| `product_id` | Text | Hide; relationship key |
| `sku` | Text | Product detail/table |
| `product_name` | Text | Axis, table, Top/Bottom-N ranking |
| `category` | Text | Slicer, axis, legend |
| `subcategory` | Text | Slicer, drill-down axis |
| `brand` | Text | Slicer, axis |
| `list_price` | Fixed decimal/currency | Hide; optional tooltip |
| `unit_cost` | Fixed decimal/currency | Hide; optional tooltip |
| `active_status` | Text | Slicer |

### `marketing_campaigns` — 25 rows

Primary key: `campaign_id`. Foreign keys: none.

| Column | Power BI type | Use |
|---|---|---|
| `campaign_id` | Text | Hide; relationship key |
| `campaign_name` | Text | Axis/detail/slicer |
| `channel` | Text | Slicer, axis, legend |
| `source` | Text | Slicer/axis |
| `medium` | Text | Slicer/axis |
| `start_date` | Date | Campaign detail/tooltip |
| `end_date` | Date | Campaign detail/tooltip |
| `spend` | Fixed decimal/currency | Hide; use `Total Spend` |
| `impressions` | Whole number | Hide; use `Total Impressions` |
| `clicks` | Whole number | Hide; use `Total Clicks` |
| `conversions` | Whole number | Hide; use `Campaign Conversions` |

### `orders` — 8,438 rows

Primary key: `order_id`. Foreign keys: `customer_id → customers`, optional `campaign_id → marketing_campaigns`, `order_date → dim_date`.

| Column | Power BI type | Use |
|---|---|---|
| `order_id` | Text | Hide; relationship and measures |
| `customer_id` | Text | Hide; relationship and measures |
| `order_timestamp` | Date/Time | Hide; optional order-detail tooltip |
| `order_status` | Text | Slicer/legend |
| `currency` | Text | Hide; all generated values are USD |
| `gross_sales` | Fixed decimal/currency | Hide; raw financial field |
| `discount` | Fixed decimal/currency | Hide; raw financial field |
| `shipping` | Fixed decimal/currency | Hide; raw financial field |
| `tax` | Fixed decimal/currency | Hide; raw financial field |
| `net_revenue` | Fixed decimal/currency | Hide; use `Total Revenue` |
| `campaign_id` | Text | Hide; relationship key |
| `order_date` | Date | Hide; date relationship key |
| `order_month` | Text | Hide; use `dim_date` fields |
| `is_completed` | Whole number | Hide; use order-status-aware measures |

### `order_items` — 15,743 rows

Primary key: `order_item_id`. Foreign keys: `order_id → orders`, `product_id → products`.

| Column | Power BI type | Use |
|---|---|---|
| `order_item_id` | Text | Hide; key |
| `order_id` | Text | Hide; relationship key |
| `product_id` | Text | Hide; relationship key |
| `quantity` | Whole number | Hide; use `Total Units Sold` |
| `unit_price` | Fixed decimal/currency | Hide; raw detail |
| `discount` | Fixed decimal/currency | Hide; raw detail |
| `item_revenue` | Fixed decimal/currency | Hide; use `Product Revenue` |
| `item_cost` | Fixed decimal/currency | Hide; raw detail |
| `item_margin` | Fixed decimal/currency | Hide; use `Total Profit Margin` |

### `customer_events` — 57,166 rows

Primary key: `event_id`. Foreign keys: `customer_id → customers`, optional `product_id → products`, optional `campaign_id → marketing_campaigns`, `event_date → dim_date`; `order_id` is informational only and is deliberately not related.

| Column | Power BI type | Use |
|---|---|---|
| `event_id` | Text | Hide; key |
| `event_timestamp` | Date/Time | Hide; event-detail tooltip |
| `session_id` | Text | Hide; DAX distinct session measures |
| `customer_id` | Text | Hide; relationship key |
| `event_name` | Text | Axis, legend, funnel visual |
| `product_id` | Text | Hide; relationship key |
| `order_id` | Text | Hide; informational purchase-event reference |
| `device` | Text | Slicer, axis, legend |
| `channel` | Text | Slicer, axis, legend |
| `source` | Text | Slicer, axis |
| `medium` | Text | Slicer, axis |
| `campaign_id` | Text | Hide; relationship key |
| `event_date` | Date | Hide; date relationship key |

### `funnel_summary` — 5 rows, do not import

Primary key: `event_name`. It has no model relationships. Its columns are `event_name` (Text), `sessions` (Whole number), `prior_sessions` (Decimal number; blank at the first stage), and `stage_conversion_rate` (Decimal number/Percentage). Keep it only as a reconciliation reference.

## Exact relationship setup

Create these active relationships, all with **single** cross-filter direction:

```text
dim_date[date] (1) → orders[order_date] (*)
dim_date[date] (1) → customer_events[event_date] (*)
customers[customer_id] (1) → orders[customer_id] (*)
customers[customer_id] (1) → customer_events[customer_id] (*)
products[product_id] (1) → order_items[product_id] (*)
products[product_id] (1) → customer_events[product_id] (*)
marketing_campaigns[campaign_id] (1) → orders[campaign_id] (*)
marketing_campaigns[campaign_id] (1) → customer_events[campaign_id] (*)
orders[order_id] (1) → order_items[order_id] (*)
customer_rfm[customer_id] (1) → customers[customer_id] (1)
```

## Expected reconciliation KPIs

These values use completed orders, except where noted. Currency is USD.

| KPI | Expected value |
|---|---:|
| Total Revenue | $1,313,406.42 |
| Total Orders | 7,547 |
| Total Customers | 3,000 |
| Purchasing Customers | 2,231 |
| Average Order Value | $174.03 |
| Total Units Sold | 17,977 |
| Product Revenue | $1,197,616.02 |
| Total Profit Margin | $619,680.02 |
| Profit Margin % | 51.74% |
| Revenue per Customer | $437.80 |
| Repeat Customers | 1,360 |
| One-Time Customers | 871 |
| Non-Buyers | 769 |
| Repeat Customer Rate | 60.96% |
| Session Starts | 14,629 |
| Product View Sessions | 14,629 |
| Cart Sessions | 11,004 |
| Checkout Sessions | 9,357 |
| Purchase Sessions | 7,547 |
| Conversion Rate | 51.59% |
| Cart-to-Checkout Rate | 85.03% |
| Checkout-to-Purchase Rate | 80.66% |
| Total Spend | $158,045.74 |
| Total Impressions | 2,607,462 |
| Total Clicks | 92,472 |
| Campaign Conversions | 5,899 |
| CTR | 3.55% |
| Customer Acquisition Cost | $26.79 |
| Attributed Revenue | $549,462.29 |
| ROAS | 3.48x |

## Report-build matrix

| Page | Visual | Chart type | Axis | Values | Legend | Slicer |
|---|---|---|---|---|---|---|
| Executive Overview | Headline performance | Cards | — | Total Revenue; Total Orders; AOV; Total Profit Margin; Profit Margin % | — | Date, city, campaign channel |
| Executive Overview | Revenue trend | Line | `dim_date[date]` | Total Revenue | — | Date, channel |
| Executive Overview | Orders trend | Column | `dim_date[month_name]` | Total Orders | — | Year, category |
| Executive Overview | Revenue by category | Bar | `products[category]` | Product Revenue | — | Date, brand |
| Executive Overview | Revenue by paid channel | Bar | `marketing_campaigns[channel]` | Attributed Revenue | — | Campaign, source |
| Executive Overview | Top products | Bar/table, Top 10 | `products[product_name]` | Product Revenue; Total Units Sold; Total Profit Margin | Category | Category, date |
| Customer & RFM | Segment mix | Donut/bar | `customer_rfm[rfm_segment]` | Total Customers | — | City, acquisition channel |
| Customer & RFM | Segment value | Clustered column | RFM segment | Total Customers; Total Revenue | — | City, channel |
| Customer & RFM | Score distribution | Matrix | R score × F score | Total Customers; Total Revenue | M score | Segment |
| Customer & RFM | Buyer mix | Cards/clustered bars | Customer type | Repeat Customers; One-Time Customers; Non-Buyers | — | City, acquisition channel |
| Customer & RFM | Acquisition quality | Bar | `customers[acquisition_channel]` | Total Customers; Purchasing Customers; Revenue per Customer | — | Segment, city |
| Product Performance | Portfolio KPIs | Cards | — | Product Revenue; Units; Margin; Margin % | — | Date, category, brand |
| Product Performance | Category performance | Bar | `products[category]` | Product Revenue; Total Profit Margin | — | Date, brand |
| Product Performance | Top 10 | Bar, Top 10 | Product name | Product Revenue | Category | Category, date |
| Product Performance | Bottom 10 | Bar, Bottom 10 | Product name | Product Revenue | Category | Category, date |
| Product Performance | Category trend | Combo/small multiples | Month | Product Revenue; Total Units Sold | Category | Year, brand |
| Marketing Performance | Marketing KPIs | Cards | — | Spend; Impressions; Clicks; Conversions; CTR; CAC; ROAS | — | Channel, campaign |
| Marketing Performance | Spend vs revenue | Combo | Campaign channel | Total Spend; Attributed Revenue | — | Campaign, source |
| Marketing Performance | Channel efficiency | Matrix | Channel | Impressions; Clicks; CTR; Conversions; CAC; ROAS | — | Campaign, medium |
| Marketing Performance | Campaign portfolio | Scatter | CAC | ROAS; Total Spend (size) | Channel | Channel, source |
| Marketing Performance | Attributed revenue | Bar | Channel | Attributed Revenue | — | Campaign, source |
| Conversion Funnel | Journey progression | Funnel/stacked bar | Event name | Distinct session count | — | Date, device, channel |
| Conversion Funnel | Funnel rates | Cards | — | Conversion Rate; Cart-to-Checkout; Checkout-to-Purchase | — | Date, device, channel |
| Conversion Funnel | Device conversion | Clustered bar | Device | Conversion Rate; Purchase Sessions | — | Date, channel |
| Conversion Funnel | Channel conversion | Clustered bar | Event channel | Conversion Rate; Purchase Sessions | — | Date, device, source |
| Conversion Funnel | Device stage detail | Matrix | Device | Distinct session count | Event name | Date, channel |

Build **Executive Overview** first. It validates the date, customer, campaign, order, and product portions of the model before the more specialised pages are added.
