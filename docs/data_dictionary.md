# Data dictionary

All IDs are stable text keys. Currency is USD. Raw tables are generated under `data/raw/`; processed tables add analytical fields for reporting. Monetary values are rounded to two decimals. `net_revenue` is gross sales less discount plus shipping and tax; product-line revenue and margin do not include shipping or tax.

## `customers`

**Purpose:** customer profile and acquisition attributes. **Grain:** one row per registered customer. **Primary key:** `customer_id`. **Foreign keys:** none.

| Column | Meaning |
|---|---|
| `customer_id` | Unique customer identifier. |
| `signup_date` | Date the customer registered. |
| `age_group`, `gender`, `city` | Customer demographic and geographic reporting attributes. |
| `acquisition_channel` | Original channel through which the customer was acquired. |
| `customer_status` | Synthetic current customer status: Active, At Risk, or Churned. |

## `products`

**Purpose:** product catalog and hierarchy. **Grain:** one row per product. **Primary key:** `product_id`. **Foreign keys:** none.

| Column | Meaning |
|---|---|
| `product_id` | Unique product identifier. |
| `sku` | Business-facing stock keeping unit. |
| `product_name`, `brand` | Product reporting labels. |
| `category`, `subcategory` | Product hierarchy used for performance analysis. |
| `list_price` | Catalog selling price before order-level pricing/discount effects. |
| `unit_cost` | Synthetic unit cost used in margin calculation. |
| `active_status` | Active or Discontinued catalog status. |

## `marketing_campaigns`

**Purpose:** campaign metadata and period-level media performance. **Grain:** one row per campaign. **Primary key:** `campaign_id`. **Foreign keys:** none.

| Column | Meaning |
|---|---|
| `campaign_id` | Unique campaign identifier. |
| `campaign_name` | Campaign reporting label. |
| `channel`, `source`, `medium` | Marketing attribution hierarchy. |
| `start_date`, `end_date` | Campaign active dates. |
| `spend` | Period-level media cost. |
| `impressions`, `clicks`, `conversions` | Campaign-reported performance metrics. |

## `orders`

**Purpose:** order-level commercial and fulfilment record. **Grain:** one row per order. **Primary key:** `order_id`. **Foreign keys:** `customer_id → customers`; optional `campaign_id → marketing_campaigns`; processed `order_date → dim_date`.

| Column | Meaning |
|---|---|
| `order_id` | Unique order identifier. |
| `customer_id` | Customer placing the order. |
| `order_timestamp` | Order Date/Time. |
| `order_status` | Completed, Returned, or Cancelled. Revenue measures use Completed orders only. |
| `currency` | Transaction currency; all generated records are USD. |
| `gross_sales` | Sum of pre-discount line revenue. |
| `discount` | Sum of order-line discounts. |
| `shipping`, `tax` | Order-level shipping and tax charges. |
| `net_revenue` | Gross sales less discount plus shipping and tax; zero for cancelled orders. |
| `campaign_id` | Optional campaign associated with the order. |
| `order_date`, `order_month`, `is_completed` | Processed reporting fields: date key, YYYY-MM month, and completed-order flag. |

## `order_items`

**Purpose:** product-level order detail and realised item margin. **Grain:** one row per product line in an order. **Primary key:** `order_item_id`. **Foreign keys:** `order_id → orders`; `product_id → products`.

| Column | Meaning |
|---|---|
| `order_item_id` | Unique order-line identifier. |
| `order_id`, `product_id` | Parent order and product keys. |
| `quantity` | Units purchased on the line. |
| `unit_price` | Realised unit price before line discount. |
| `discount` | Discount applied to the line. |
| `item_revenue` | `unit_price × quantity − discount`. |
| `item_cost` | Unit cost multiplied by quantity. |
| `item_margin` | `item_revenue − item_cost`; product-line contribution margin. |

## `customer_events`

**Purpose:** session-level behavioural event stream for funnel analysis. **Grain:** one row per customer event. **Primary key:** `event_id`. **Foreign keys:** `customer_id → customers`; optional `product_id → products`; optional `campaign_id → marketing_campaigns`; processed `event_date → dim_date`. `order_id` is populated for purchase events but is intentionally not modelled as a Power BI relationship.

| Column | Meaning |
|---|---|
| `event_id` | Unique event identifier. |
| `event_timestamp` | Event Date/Time. |
| `session_id` | Session identifier used for distinct-session funnel measures. |
| `customer_id` | Customer generating the event. |
| `event_name` | One of `session_start`, `product_view`, `add_to_cart`, `begin_checkout`, or `purchase`. |
| `product_id` | Relevant viewed/purchased product when applicable. |
| `order_id` | Completed order referenced by a purchase event. |
| `device` | Mobile, Desktop, or Tablet. |
| `channel`, `source`, `medium` | Event-level traffic attribution. |
| `campaign_id` | Optional marketing campaign attribution. |
| `event_date` | Processed date key for reporting. |

## `customer_rfm`

**Purpose:** current-state customer value segmentation. **Grain:** one row per customer. **Primary key and foreign key:** `customer_id → customers[customer_id]`.

| Column | Meaning |
|---|---|
| `customer_id` | Customer key. |
| `frequency` | Number of completed orders. |
| `monetary` | Sum of completed-order net revenue. |
| `recency_days` | Days from the latest completed order to 2026-01-01; non-buyers are assigned 999. |
| `r_score`, `f_score`, `m_score` | Quintile scores; higher is better. |
| `rfm_score` | Sum of the three component scores. |
| `rfm_segment` | Champions, Loyal High Value, New Customers, At Risk, Hibernating, or Needs Activation. |

## `dim_date`

**Purpose:** shared reporting calendar. **Grain:** one row per day in 2025. **Primary key:** `date`. **Foreign keys:** none; it is referenced by processed order and event date fields.

| Column | Meaning |
|---|---|
| `date` | Calendar date and relationship key. |
| `year` | Calendar year. |
| `month` | Month number, used to sort `month_name`. |
| `month_name` | Abbreviated month label. |
| `quarter` | Calendar quarter label. |

## Supporting output: `funnel_summary`

**Purpose:** static pipeline reconciliation output, not a reporting-model fact. **Grain:** one row per funnel stage. **Primary key:** `event_name`.

| Column | Meaning |
|---|---|
| `event_name` | Funnel stage. |
| `sessions` | Distinct sessions reaching the stage. |
| `prior_sessions` | Distinct sessions at the preceding stage. |
| `stage_conversion_rate` | Sessions divided by preceding-stage sessions. |
