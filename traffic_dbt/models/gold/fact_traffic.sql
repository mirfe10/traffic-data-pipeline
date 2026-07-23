SELECT
    id,
    created_at,
    location_name,

    latitude,
    longitude,
    road_geometry,

    traffic_congestion_percent,
    delay_seconds,
    traffic_level,

    current_speed,
    free_flow_speed,
    current_travel_time,
    free_flow_travel_time,
    road_closed

FROM {{ ref('traffic_clean') }}