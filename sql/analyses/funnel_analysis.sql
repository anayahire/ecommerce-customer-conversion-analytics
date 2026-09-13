-- Purpose: calculate distinct-session funnel counts and prior-stage conversion.
WITH stages AS (
    SELECT 'session_start' AS stage, 1 AS step
    UNION ALL SELECT 'product_view', 2
    UNION ALL SELECT 'add_to_cart', 3
    UNION ALL SELECT 'begin_checkout', 4
    UNION ALL SELECT 'purchase', 5
),
counts AS (
    SELECT
        event_name AS stage,
        COUNT(DISTINCT session_id) AS sessions
    FROM customer_events
    GROUP BY 1
)
SELECT
    s.stage,
    COALESCE(c.sessions, 0) AS sessions,
    ROUND(
        COALESCE(c.sessions, 0) * 1.0
        / NULLIF(LAG(c.sessions) OVER (ORDER BY s.step), 0),
        4
    ) AS prior_stage_conversion
FROM stages AS s
LEFT JOIN counts AS c ON c.stage = s.stage
ORDER BY s.step;
