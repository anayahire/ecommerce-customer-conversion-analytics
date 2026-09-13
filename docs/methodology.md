# Methodology

The project uses a fixed-seed synthetic generator, not external data. The generator creates uneven customer propensities, seasonal demand peaks in November and December, campaign-specific traffic efficiency, repeat purchasing, non-purchasers, returns, cancellations, and session-level funnel drop-off.

Completed orders are used for revenue, RFM, and product performance. Cancelled orders have zero net revenue; returned orders remain available for operational analysis but are excluded from completed-sales metrics. RFM is calculated as of 2026-01-01: recency is days since the last completed order, frequency is completed-order count, and monetary value is completed net revenue. Scores are quintiles among buyers.

Run validation before processing. It checks required columns, unique primary keys, foreign keys, funnel values, financial arithmetic, positive quantities, cancellation treatment, completed purchase events, and analysis-year coverage.
