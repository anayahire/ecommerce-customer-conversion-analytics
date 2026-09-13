-- Purpose: compare acquisition channels, retaining customers with no completed orders.
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(COALESCE(SUM(o.net_revenue), 0), 2) AS revenue
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
    AND o.order_status = 'Completed'
GROUP BY 1
ORDER BY revenue DESC;
