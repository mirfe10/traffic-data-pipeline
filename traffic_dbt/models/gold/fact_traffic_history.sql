SELECT
    id,
    created_at,
    location_name,
    current_speed,
    free_flow_speed,
    traffic_congestion_percent,
    delay_seconds,
    traffic_level,
    road_closed
FROM {{ ref('traffic_clean') }}