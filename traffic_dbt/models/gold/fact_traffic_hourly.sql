SELECT
    DATE_TRUNC('hour', created_at) AS hour,
    location_name,

    ROUND(AVG(current_speed),2) AS avg_current_speed,

    ROUND(AVG(delay_seconds),2) AS avg_delay_seconds,

    ROUND(AVG(traffic_congestion_percent),2)
        AS avg_traffic_congestion_percent,

    COUNT(*) AS record_count

FROM {{ ref('traffic_clean') }}

GROUP BY
    DATE_TRUNC('hour', created_at),
    location_name