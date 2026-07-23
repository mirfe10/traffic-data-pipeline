WITH traffic_base AS (

    SELECT
        id,
        created_at,
        location_name,
        latitude,
        longitude,
        road_geometry,

        ROUND(
            (
                1 -
                current_speed::numeric /
                NULLIF(free_flow_speed, 0)
            ) * 100,
            1
        ) AS traffic_congestion_percent,

        current_travel_time - free_flow_travel_time
            AS delay_seconds,

        current_speed,
        free_flow_speed,

        current_travel_time,
        free_flow_travel_time,
        road_closed

    FROM bronze.traffic_raw

    WHERE
        current_speed >= 0
        AND free_flow_speed > 0
        AND confidence >= 0.70

)

SELECT
    id,
    created_at,
    location_name,
    latitude,
    longitude,
    road_geometry,

    traffic_congestion_percent,
    delay_seconds,

    CASE
        WHEN traffic_congestion_percent < 20 THEN 'Akıcı'
        WHEN traffic_congestion_percent < 50 THEN 'Orta'
        WHEN traffic_congestion_percent < 75 THEN 'Yoğun'
        ELSE 'Çok Yoğun'
    END AS traffic_level,

    current_speed,
    free_flow_speed,
    current_travel_time,
    free_flow_travel_time,
    road_closed

FROM traffic_base