# Power BI handoff guide

Load eight CSVs from `data/processed/`. Do **not** load `funnel_summary.csv`: it is a static pipeline-audit output and would not respond to report filters.

## Tables to import

| Table | Purpose | Grain | Primary key | Foreign keys |
|---|---|---|---|---|
| `dim_date` | Shared calendar. | One row per day. | `date` | — |
| `customers` | Customer profile/acquisition attributes. | One row per customer. | `customer_id` | — |
| `customer_rfm` | Current RFM scores and segment. | One row per customer. | `customer_id` | `customer_id → customers[customer_id]` |
| `products` | Product hierarchy and catalog attributes. | One row per product. | `product_id` | — |
| `marketing_campaigns` | Campaign metadata and period-level media metrics. | One row per campaign. | `campaign_id` | — |
| `orders` | Order financials and status. | One row per order. | `order_id` | `customer_id`, `campaign_id`, `order_date` |
| `order_items` | Product lines and realised margin. | One row per order line. | `order_item_id` | `order_id`, `product_id` |
| `customer_events` | Session customer-journey events. | One row per event. | `event_id` | `customer_id`, `product_id`, `campaign_id`, `event_date` |

Set IDs to Text; `orders[order_date]` and `customer_events[event_date]` to Date; timestamps to Date/Time; and money to fixed decimal/currency. Mark `dim_date[date]` as the date table and sort `month_name` by `month`.

## Relationships and star-schema map

Use active, single-direction dimension-to-fact relationships.

| From | To | Cardinality | Filter direction |
|---|---|---:|---|
| `dim_date[date]` | `orders[order_date]` | 1:* | Date → Orders |
| `dim_date[date]` | `customer_events[event_date]` | 1:* | Date → Events |
| `customers[customer_id]` | `orders[customer_id]` | 1:* | Customers → Orders |
| `customers[customer_id]` | `customer_events[customer_id]` | 1:* | Customers → Events |
| `products[product_id]` | `order_items[product_id]` | 1:* | Products → Order Items |
| `products[product_id]` | `customer_events[product_id]` | 1:* | Products → Events |
| `marketing_campaigns[campaign_id]` | `orders[campaign_id]` | 1:* | Campaigns → Orders |
| `marketing_campaigns[campaign_id]` | `customer_events[campaign_id]` | 1:* | Campaigns → Events |
| `orders[order_id]` | `order_items[order_id]` | 1:* | Orders → Order Items |
| `customer_rfm[customer_id]` | `customers[customer_id]` | 1:1 | RFM → Customers |

```text
                         customer_rfm
                              | 1:1
                              v
dim_date ──1:*──> orders ──1:*──> order_items <──*:1── products
   |                 ^  ^                                  |
   |                 |  └────*:1 marketing_campaigns ──────┤
   └──1:*──> customer_events <──*:1── customers             |
                     ^                                      |
                     └────*:1 marketing_campaigns ─────────┘
```

Do not relate `orders` directly to `customer_events`: only purchase events carry an order ID and the relationship creates ambiguous paths. Do not relate campaign start/end dates to `dim_date`; campaign spend is period-level, not daily.

`Total Revenue` is an order-header measure, so a product/category filter does not flow backward from `order_items` to `orders` in this single-direction model. Use `Product Revenue` for category/product visuals, and disable category-slicer interaction with order-header KPI cards when needed.

## Visible, hidden, dimension, and measure fields

| Table | Visible dimensions/slicers | Hide / use only in measures |
|---|---|---|
| `dim_date` | `date`, `year`, `quarter`, `month`, `month_name` | — |
| `customers` | age, gender, city, acquisition channel, status | `customer_id` |
| `customer_rfm` | segment, R/F/M scores, RFM score, recency | `customer_id`, frequency, monetary (unless showing a customer-detail table) |
| `products` | product, SKU, category, subcategory, brand, active status | `product_id`, list price, unit cost |
| `marketing_campaigns` | campaign, channel, source, medium, start/end date | `campaign_id`, spend, impressions, clicks, conversions |
| `orders` | order status, currency | IDs, timestamps/date keys, `is_completed`, all raw financial values |
| `order_items` | none; use product dimensions | all columns |
| `customer_events` | event name, device, channel, source, medium | IDs, timestamps/date keys, session ID |

## DAX measures

Create a disconnected `Measures` table and put these measures there. Format money as currency, rates as percentages, and ROAS as a decimal such as `3.48x`.

| Measure | Exact DAX | What it calculates / dependencies |
|---|---|---|
| Total Revenue | `Total Revenue = CALCULATE(SUM(orders[net_revenue]), orders[order_status] = "Completed")` | Completed-order revenue; `orders[net_revenue]`, `orders[order_status]`. |
| Total Orders | `Total Orders = CALCULATE(DISTINCTCOUNT(orders[order_id]), orders[order_status] = "Completed")` | Completed orders; `orders[order_id]`, status. |
| Total Customers | `Total Customers = DISTINCTCOUNT(customers[customer_id])` | Registered customers in current customer-filter context; `customers[customer_id]`. |
| Purchasing Customers | `Purchasing Customers = CALCULATE(DISTINCTCOUNT(orders[customer_id]), orders[order_status] = "Completed")` | Customers with a completed order; `orders[customer_id]`, status. |
| Average Order Value | `Average Order Value = DIVIDE([Total Revenue], [Total Orders])` | Revenue per completed order; prior two measures. |
| Total Units Sold | `Total Units Sold = CALCULATE(SUM(order_items[quantity]), orders[order_status] = "Completed")` | Completed-order quantity; `order_items[quantity]`, order status. |
| Total Profit Margin | `Total Profit Margin = CALCULATE(SUM(order_items[item_margin]), orders[order_status] = "Completed")` | Product-line contribution margin (excludes shipping/tax); item margin, order status. |
| Product Revenue | `Product Revenue = CALCULATE(SUM(order_items[item_revenue]), orders[order_status] = "Completed")` | Discounted product-line revenue; item revenue, order status. |
| Profit Margin % | `Profit Margin % = DIVIDE([Total Profit Margin], [Product Revenue])` | Product-line margin rate; preceding measures. |
| Revenue per Customer | `Revenue per Customer = DIVIDE([Total Revenue], [Total Customers])` | Completed revenue per registered customer; preceding measures. |
| Repeat Customers | `Repeat Customers = COUNTROWS(FILTER(VALUES(orders[customer_id]), CALCULATE(DISTINCTCOUNT(orders[order_id]), orders[order_status] = "Completed") > 1))` | Customers with >1 completed order in context; order customer, ID, status. |
| One-Time Customers | `One-Time Customers = COUNTROWS(FILTER(VALUES(orders[customer_id]), CALCULATE(DISTINCTCOUNT(orders[order_id]), orders[order_status] = "Completed") = 1))` | Customers with exactly one completed order; order customer, ID, status. |
| Non-Buyers | `Non-Buyers = COUNTROWS(FILTER(VALUES(customers[customer_id]), CALCULATE([Total Orders]) = 0))` | Registered customers without a completed order; customers and `Total Orders`. |
| Repeat Customer Rate | `Repeat Customer Rate = DIVIDE([Repeat Customers], [Purchasing Customers])` | Repeat share of purchasers; preceding measures. |
| Session Starts | `Session Starts = CALCULATE(DISTINCTCOUNT(customer_events[session_id]), customer_events[event_name] = "session_start")` | Sessions entering funnel; event session ID/name. |
| Product View Sessions | `Product View Sessions = CALCULATE(DISTINCTCOUNT(customer_events[session_id]), customer_events[event_name] = "product_view")` | Sessions reaching product view; event session ID/name. |
| Cart Sessions | `Cart Sessions = CALCULATE(DISTINCTCOUNT(customer_events[session_id]), customer_events[event_name] = "add_to_cart")` | Sessions adding to cart; event session ID/name. |
| Checkout Sessions | `Checkout Sessions = CALCULATE(DISTINCTCOUNT(customer_events[session_id]), customer_events[event_name] = "begin_checkout")` | Sessions beginning checkout; event session ID/name. |
| Purchase Sessions | `Purchase Sessions = CALCULATE(DISTINCTCOUNT(customer_events[session_id]), customer_events[event_name] = "purchase")` | Sessions purchasing; event session ID/name. |
| Conversion Rate | `Conversion Rate = DIVIDE([Purchase Sessions], [Session Starts])` | Overall session-to-purchase conversion; preceding measures. |
| Cart-to-Checkout Rate | `Cart-to-Checkout Rate = DIVIDE([Checkout Sessions], [Cart Sessions])` | Cart progression; preceding measures. |
| Checkout-to-Purchase Rate | `Checkout-to-Purchase Rate = DIVIDE([Purchase Sessions], [Checkout Sessions])` | Checkout completion; preceding measures. |
| Total Spend | `Total Spend = SUM(marketing_campaigns[spend])` | Campaign spend; `marketing_campaigns[spend]`. |
| Total Impressions | `Total Impressions = SUM(marketing_campaigns[impressions])` | Campaign reach; impressions. |
| Total Clicks | `Total Clicks = SUM(marketing_campaigns[clicks])` | Campaign clicks; clicks. |
| Campaign Conversions | `Campaign Conversions = SUM(marketing_campaigns[conversions])` | Campaign-reported conversions; conversions. |
| CTR | `CTR = DIVIDE([Total Clicks], [Total Impressions])` | Click-through rate; clicks, impressions. |
| Customer Acquisition Cost | `Customer Acquisition Cost = DIVIDE([Total Spend], [Campaign Conversions])` | Spend per campaign-reported conversion; spend, conversions. |
| Attributed Revenue | `Attributed Revenue = CALCULATE([Total Revenue], FILTER(orders, NOT ISBLANK(orders[campaign_id])))` | Completed revenue carrying a campaign ID; revenue, campaign ID. |
| ROAS | `ROAS = DIVIDE([Attributed Revenue], [Total Spend])` | Attributed revenue per spend dollar; attributed revenue, spend. |

## Dashboard pages

For all pages, use clean titles, a tooltip with the relevant supporting measure, and only the slicers named below.

### 1. Executive Overview

| Visual | Data fields / measures | Slicers | Business question |
|---|---|---|---|
| KPI cards | Total Revenue, Total Orders, Average Order Value, Total Profit Margin, Profit Margin % | Date, category, campaign channel, city | How is the business performing? |
| Line chart | `dim_date[date]`, Total Revenue | Date, category, channel | How is revenue trending? |
| Column chart | month, Total Orders | Year, category | When does order demand peak? |
| Bar chart | product category, Product Revenue | Date, brand | Which categories lead revenue? |
| Bar chart | campaign channel, Attributed Revenue | Campaign/source/medium | Which paid channels produce attributed revenue? |
| Top-N bar/table | product name; Product Revenue, Units, Margin; Top 10 | Category, date | Which products lead sales and profit? |

### 2. Customer & RFM

| Visual | Data fields / measures | Slicers | Business question |
|---|---|---|---|
| Donut/bar | RFM segment, Total Customers | City, acquisition channel, age group | How is the customer base segmented? |
| Clustered column | RFM segment; Total Customers and Total Revenue | City, channel | Which segments are largest and most valuable? |
| Matrix | R score × F score; Total Customers, Total Revenue; M-score filter | Segment | Where do customers sit in RFM space? |
| Cards or clustered bars | Repeat Customers, One-Time Customers, Non-Buyers | City, acquisition channel | How many repeat, one-time, and non-buying customers exist? |
| Bar chart | acquisition channel; Total Customers, Purchasing Customers, Revenue per Customer | Segment, city | Which sources acquire valuable customers? |

### 3. Product Performance

| Visual | Data fields / measures | Slicers | Business question |
|---|---|---|---|
| KPI cards | Product Revenue, Total Units Sold, Total Profit Margin, Profit Margin % | Date, category, brand | How is the portfolio performing? |
| Bar chart | category; Product Revenue and Total Profit Margin | Date, brand | Which categories lead or lag? |
| Top-N bar | product name; Product Revenue; Top 10 | Category, date | Which ten products are strongest? |
| Bottom-N bar | product name; Product Revenue; Bottom 10 | Category, date | Which products may need review? |
| Combo/small multiples | month; Product Revenue and Units; small multiple category | Year, brand | How does category performance change over time? |

### 4. Marketing Performance

| Visual | Data fields / measures | Slicers | Business question |
|---|---|---|---|
| KPI cards | Total Spend, Impressions, Clicks, Campaign Conversions, CTR, CAC, ROAS | Channel, campaign, source, medium | Is campaign investment efficient? |
| Combo chart | channel; Total Spend and Attributed Revenue | Campaign, source | Which channels balance cost and return? |
| Matrix | channel; Impressions, Clicks, CTR, Conversions, CAC, ROAS | Campaign, medium | How do channel efficiency metrics compare? |
| Scatter | campaign name; X=CAC, Y=ROAS, Size=Spend, Legend=channel | Channel, source | Which campaigns are scalable? |
| Bar chart | campaign channel; Attributed Revenue | Campaign, source, medium | Which paid channels drive revenue? |

Campaign spend is period-level: do not use the daily report-date slicer for spend/ROAS until daily spend allocation is added.

### 5. Conversion Funnel

| Visual | Data fields / measures | Slicers | Business question |
|---|---|---|---|
| Funnel or stacked bar | event name and distinct session count, or the five funnel measures | Date, device, event channel, source, medium | Where do visitors leave the journey? |
| KPI cards | Conversion Rate, Cart-to-Checkout Rate, Checkout-to-Purchase Rate | Date, device, channel | What are key conversion rates? |
| Clustered bar | device; Conversion Rate and Purchase Sessions | Date, channel | Which devices convert best? |
| Clustered bar | event channel; Conversion Rate and Purchase Sessions | Date, device, source | Which traffic channels convert best? |
| Matrix | device × event name; distinct session count | Date, channel | How does stage progression vary by device? |

For a native funnel using five individual measures, create a small disconnected stage table in Power BI only; do not connect it to the model.
