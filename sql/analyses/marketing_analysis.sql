-- Purpose: compare campaign delivery cost and completed-order attributed revenue.
SELECT
    m.campaign_name,
    m.channel,
    m.spend,
    m.impressions,
    m.clicks,
    m.conversions,
    ROUND(m.spend * 1.0 / NULLIF(m.clicks, 0), 2) AS cost_per_click,
    ROUND(COALESCE(SUM(o.net_revenue), 0), 2) AS attributed_revenue
FROM marketing_campaigns AS m
LEFT JOIN orders AS o
    ON m.campaign_id = o.campaign_id
    AND o.order_status = 'Completed'
GROUP BY m.campaign_id
ORDER BY attributed_revenue DESC;
