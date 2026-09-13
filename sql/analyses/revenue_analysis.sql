-- Purpose: track completed-order revenue, volume, and average order value by month.
SELECT
    substr(order_timestamp, 1, 7) AS month,
    COUNT(*) AS orders,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(AVG(net_revenue), 2) AS average_order_value
FROM orders
WHERE order_status = 'Completed'
GROUP BY 1
ORDER BY 1;
