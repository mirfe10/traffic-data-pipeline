SELECT
    -- =========================
    -- TIME
    -- =========================
    t.event_time,
    t.created_at,
    DATE(t.event_time) AS event_date,
    EXTRACT(HOUR FROM t.event_time) AS hour,
    EXTRACT(DOW FROM t.event_time) AS day_of_week,

    CASE
        WHEN EXTRACT(HOUR FROM t.event_time) BETWEEN 7 AND 9
          OR EXTRACT(HOUR FROM t.event_time) BETWEEN 17 AND 19
        THEN TRUE
        ELSE FALSE
    END AS rush_hour,

    CASE
        WHEN EXTRACT(DOW FROM t.event_time) IN (0, 6)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend,

    -- =========================
    -- LOCATION
    -- =========================
    t.location_name,
    t.latitude,
    t.longitude,

    -- =========================
    -- TRAFFIC
    -- =========================
    t.current_speed,
    t.free_flow_speed,
    t.current_travel_time,
    t.free_flow_travel_time,
    t.delay_seconds,
    t.traffic_congestion_percent,
    t.traffic_level,
    t.road_closed,

    ROUND(
        t.current_speed::numeric /
        NULLIF(t.free_flow_speed, 0),
        2
    ) AS speed_ratio,

    CASE
        WHEN t.delay_seconds < 30 THEN 'Low'
        WHEN t.delay_seconds < 90 THEN 'Medium'
        ELSE 'High'
    END AS delay_level,

    -- =========================
    -- WEATHER
    -- =========================
    w.temperature,
    w.apparent_temperature,
    w.humidity,
    w.precipitation,
    w.rain,
    w.cloud_cover,
    w.wind_speed,
    w.weather_code,
    w.weather_description,
    w.temperature_level,
    w.humidity_level,
    w.wind_level,
    w.cloud_level,
    w.is_raining,

    CASE
        WHEN w.rain > 5 THEN 'Heavy Rain'
        WHEN w.rain > 0 THEN 'Light Rain'
        WHEN w.cloud_cover > 80 THEN 'Cloudy'
        ELSE 'Clear'
    END AS weather_severity,

    -- =========================
    -- ANALYSIS FLAGS
    -- =========================
    CASE
        WHEN w.is_raining
         AND t.traffic_congestion_percent >= 50
        THEN TRUE
        ELSE FALSE
    END AS rain_causing_congestion,

    CASE
        WHEN w.temperature >= 30
         AND t.traffic_congestion_percent >= 50
        THEN TRUE
        ELSE FALSE
    END AS hot_weather_congestion

FROM {{ ref('traffic_clean') }} t

LEFT JOIN {{ ref('weather_clean') }} w
    ON t.location_name = w.location_name
   AND t.event_time = w.event_time