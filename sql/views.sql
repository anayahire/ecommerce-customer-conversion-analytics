-- Completed-order revenue and active-customer trend by calendar month.
CREATE VIEW IF NOT EXISTS vw_monthly_revenue AS
SELECT
    substr(order_timestamp, 1, 7) AS order_month,
    COUNT(*) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(net_revenue), 2) AS revenue
FROM orders
WHERE order_status = 'Completed'
GROUP BY 1;

-- Product-level completed-order revenue, unit volume, and realised item margin.
CREATE VIEW IF NOT EXISTS vw_product_performance AS
SELECT
    p.category,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.item_revenue), 2) AS revenue,
    ROUND(SUM(oi.item_margin), 2) AS margin
FROM order_items AS oi
JOIN products AS p ON p.product_id = oi.product_id
JOIN orders AS o ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY 1, 2;
