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

- **Python** — data generation, cleaning, validation, and analysis
- **Pandas / NumPy** — data manipulation and analysis
- **SQL / SQLite** — relational analysis and business queries
- **Power BI** — interactive dashboards and visualization
- **Jupyter Notebook** — exploratory data analysis
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

- customer_rfm
- funnel_summary
- dim_date

## Data Pipeline

**Raw Data**

↓  

**Data Validation**

↓

**Python Analysis**

↓

**SQL Business Analysis**

↓

**Power BI Data Model**

↓

**Interactive Dashboard**

↓

**Business Insights**

## Power BI Dashboard

The Power BI dashboard provides an interactive view of revenue, customer behavior, product performance, marketing effectiveness, and conversion funnel performance.
### Interactive Power BI Report

[📊 Download the Power BI Dashboard (.pbix)](powerbi/ecommerce_customer_conversion_analytics.pbix)

> The downloadable Power BI report contains 5 interactive pages covering Executive Overview, Customer & RFM, Product Performance, Marketing Performance, and Conversion Funnel analysis.

### Executive Overview

![Executive Overview](https://raw.githubusercontent.com/anayahire/ecommerce-customer-conversion-analytics/main/powerbi/screenshots/executive_overview.jpeg)

### Customer & RFM Analysis

![Customer & RFM Analysis](https://raw.githubusercontent.com/anayahire/ecommerce-customer-conversion-analytics/main/powerbi/screenshots/customer_rfm.jpeg)

### Product Performance

![Product Performance](https://raw.githubusercontent.com/anayahire/ecommerce-customer-conversion-analytics/main/powerbi/screenshots/product_performance.jpeg)

### Marketing Performance

![Marketing Performance](https://raw.githubusercontent.com/anayahire/ecommerce-customer-conversion-analytics/main/powerbi/screenshots/marketing_performance.jpeg)

### Conversion Funnel

![Conversion Funnel](https://raw.githubusercontent.com/anayahire/ecommerce-customer-conversion-analytics/main/powerbi/screenshots/conversion_funnel.jpeg)

## Key Business Insights

- Generated **$1.31M** in completed-order revenue across **7,547 completed orders**.
- Average order value was approximately **$174**.
- **November and December contributed 44.81% of annual revenue**, with December being the strongest month.
- **Electronics** was the highest-revenue product category at approximately **$344K**.
- **60.96% of purchasing customers were repeat customers**.
- The **Champions RFM segment** contributed approximately **51% of total revenue**.
- The largest conversion loss occurred between **product view and add-to-cart**.
- Overall marketing **ROAS was 3.48x**.
- **Paid Search** had the lowest channel ROAS at approximately **1.30x**.
- **Email** had the lowest customer acquisition cost at approximately **$13.98**.

## Analysis Areas

### Customer Analytics

- Customer segmentation using RFM analysis
- Repeat vs one-time customer analysis
- Customer value and purchasing behavior
- Recency, frequency, and monetary analysis

### Product Analytics

- Revenue by product category
- Top-performing products
- Units sold by category
- Product-level performance analysis

### Marketing Analytics

- Campaign spend analysis
- Attributed revenue
- ROAS by marketing channel
- Customer acquisition cost
- Marketing spend vs attributed revenue

### Conversion Funnel

- Session-to-purchase conversion
- Funnel stage analysis
- Drop-off identification
- Conversion performance by marketing channel

## Project Structure

- **data/**
  - raw/
  - interim/
  - processed/

- **docs/**
  - business_insights.md
  - dashboard_guide.md
  - data_dictionary.md
  - methodology.md
  - powerbi_import_checklist.md

- **notebooks/**
  - 01_data_audit.ipynb
  - 02_eda.ipynb
  - 03_rfm_segmentation.ipynb
  - 04_funnel_analysis.ipynb

- **powerbi/screenshots/**
  - executive_overview.jpeg
  - customer_rfm.jpeg
  - product_performance.jpeg
  - marketing_performance.jpeg
  - conversion_funnel.jpeg

- **sql/**
  - analyses/
  - schema.sql
  - views.sql

- **src/**
  - cleaning.py
  - feature_engineering.py
  - generate_data.py
  - ingestion.py
  - quality_checks.py
  - rfm.py

- **tests/**
  - test_quality.py

- .gitignore
- README.md
- requirements.txt

## Validation

The project includes data quality and reproducibility checks covering:

- Missing values
- Duplicate records
- Referential integrity
- Valid foreign-key relationships
- Order and transaction consistency
- RFM calculation validation
- Funnel analysis validation
- Automated quality tests
- Reproducibility checks

## Reproducibility

The dataset is synthetically generated with a fixed random seed to ensure reproducible results.

The project can be reproduced by installing the required Python dependencies and running the data generation, validation, analysis, and notebook workflows provided in the repository.

## Limitations

- The dataset is synthetic and does not represent real customer behavior.
- Monetary values are represented in USD.
- Revenue includes shipping and tax components.
- Marketing attribution is based on the available campaign attribution fields.
- The Power BI dashboard is documented through screenshots and model/import instructions.

## Author

**Anaya Hire** — Author  
**Anjali Sinha** — Co-author


Data Analytics | Python | SQL | Power BI
