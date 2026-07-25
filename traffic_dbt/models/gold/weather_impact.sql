SELECT
    weather_description,
    weather_severity,
    is_raining,

    COUNT(*) AS observation_count,

    ROUND(AVG(current_speed),2) AS avg_speed,
    ROUND(AVG(delay_seconds),2) AS avg_delay,
    ROUND(AVG(traffic_congestion_percent),2) AS avg_congestion,

    ROUND(MIN(current_speed),2) AS min_speed,
    ROUND(MAX(current_speed),2) AS max_speed,

    ROUND(AVG(temperature),2) AS avg_temperature,
    ROUND(AVG(humidity),2) AS avg_humidity,
    ROUND(AVG(wind_speed),2) AS avg_wind_speed

FROM {{ ref('traffic_weather_analysis') }}

GROUP BY
    weather_description,
    weather_severity,
    is_raining

ORDER BY avg_delay DESC