# E-Commerce Customer & Conversion Analytics

An end-to-end data analytics project analyzing customer behavior, sales performance, product performance, marketing effectiveness, and conversion funnel behavior using Python, SQL, and Power BI.

## Project Overview

This project analyzes a synthetic e-commerce dataset covering the full year of 2025.

The objective is to answer key business questions:

- How is revenue changing over time?
- Which product categories and products generate the most revenue?
- Which customer segments contribute the most value?
- How many customers are repeat purchasers?
- Which marketing channels generate the best return?
- Where are customers dropping off in the conversion funnel?

## Tech Stack

- **Python** — data generation, cleaning, validation and analysis
- **Pandas / NumPy** — data manipulation and analysis
- **SQL / SQLite** — relational analysis and business queries
- **Power BI** — interactive dashboards and visualization
- **Jupyter Notebook** — exploratory analysis
- **Git / GitHub** — version control

## Dataset

The project contains six core datasets:

| Dataset | Description |
|---|---|
| customers | Customer demographics and acquisition information |
| orders | Order-level transactions |
| order_items | Individual products purchased in each order |
| products | Product catalogue and pricing |
| marketing_campaigns | Campaign spend and performance |
| customer_events | Customer funnel events |

Additional analytical tables include:

- `customer_rfm`
- `funnel_summary`
- `dim_date`

## Data Pipeline

```text
Raw Data
   ↓
Data Validation
   ↓
Python Analysis
   ↓
SQL Business Analysis
   ↓
Power BI Data Model
   ↓
Interactive Dashboard
   ↓
Business Insights
