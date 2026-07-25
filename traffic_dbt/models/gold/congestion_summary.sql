SELECT

    traffic_level,

    COUNT(*) AS observation_count,

    ROUND(AVG(current_speed), 2) AS avg_speed,
    ROUND(MIN(current_speed), 2) AS min_speed,
    ROUND(MAX(current_speed), 2) AS max_speed,

    ROUND(AVG(delay_seconds), 2) AS avg_delay,
    ROUND(MAX(delay_seconds), 2) AS max_delay,

    ROUND(AVG(traffic_congestion_percent), 2) AS avg_congestion,

    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(wind_speed), 2) AS avg_wind_speed,
    ROUND(AVG(rain), 2) AS avg_rain,

    SUM(CASE WHEN is_raining THEN 1 ELSE 0 END) AS rainy_observations,
    SUM(CASE WHEN road_closed THEN 1 ELSE 0 END) AS road_closure_count

FROM {{ ref('traffic_weather_analysis') }}

GROUP BY traffic_level

ORDER BY avg_congestion DESC