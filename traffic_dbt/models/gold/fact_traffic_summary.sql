SELECT
    location_name,

    COUNT(*) AS record_count,

    ROUND(AVG(current_speed), 2) AS avg_current_speed,

    ROUND(AVG(free_flow_speed), 2) AS avg_free_flow_speed,

    ROUND(AVG(traffic_congestion_percent), 2)
        AS avg_traffic_congestion_percent,

    ROUND(AVG(delay_seconds), 2)
        AS avg_delay_seconds,

    MAX(created_at) AS last_update,

    CASE
        WHEN AVG(traffic_congestion_percent) < 20 THEN 'Akıcı'
        WHEN AVG(traffic_congestion_percent) < 50 THEN 'Orta'
        WHEN AVG(traffic_congestion_percent) < 75 THEN 'Yoğun'
        ELSE 'Çok Yoğun'
    END AS overall_traffic_level

FROM {{ ref('traffic_clean') }}

GROUP BY location_name