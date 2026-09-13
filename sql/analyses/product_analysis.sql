-- Purpose: rank the 20 highest-revenue products using completed order lines.
SELECT
    p.category,
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.item_revenue), 2) AS revenue,
    ROUND(SUM(oi.item_margin), 2) AS margin
FROM order_items AS oi
JOIN orders AS o USING (order_id)
JOIN products AS p USING (product_id)
WHERE o.order_status = 'Completed'
GROUP BY 1, 2
ORDER BY revenue DESC
LIMIT 20;
