SELECT
    id,
    DATE_TRUNC('minute', created_at) AS event_time,
    created_at,
    location_name,
    latitude,
    longitude,

    ROUND(temperature::numeric, 1) AS temperature,
    ROUND(apparent_temperature::numeric, 1) AS apparent_temperature,

    humidity,

    ROUND(precipitation::numeric, 2) AS precipitation,
    ROUND(rain::numeric, 2) AS rain,

    cloud_cover,

    ROUND(wind_speed::numeric, 1) AS wind_speed,

    weather_code,

    CASE
        WHEN temperature < 10 THEN 'Cold'
        WHEN temperature < 20 THEN 'Cool'
        WHEN temperature < 30 THEN 'Warm'
        ELSE 'Hot'
    END AS temperature_level,

    CASE
        WHEN humidity < 40 THEN 'Low'
        WHEN humidity < 70 THEN 'Medium'
        ELSE 'High'
    END AS humidity_level,

    CASE
        WHEN wind_speed < 10 THEN 'Light'
        WHEN wind_speed < 25 THEN 'Moderate'
        ELSE 'Strong'
    END AS wind_level,

    CASE
        WHEN rain > 0 THEN TRUE
        ELSE FALSE
    END AS is_raining,

    CASE
        WHEN cloud_cover < 25 THEN 'Clear'
        WHEN cloud_cover < 60 THEN 'Partly Cloudy'
        ELSE 'Cloudy'
    END AS cloud_level,

    CASE
        WHEN weather_code = 0 THEN 'Clear Sky'
        WHEN weather_code IN (1,2,3) THEN 'Cloudy'
        WHEN weather_code IN (45,48) THEN 'Fog'
        WHEN weather_code IN (51,53,55,56,57) THEN 'Drizzle'
        WHEN weather_code IN (61,63,65,66,67) THEN 'Rain'
        WHEN weather_code IN (71,73,75,77) THEN 'Snow'
        WHEN weather_code IN (80,81,82) THEN 'Rain Showers'
        WHEN weather_code IN (95,96,99) THEN 'Thunderstorm'
        ELSE 'Unknown'
    END AS weather_description

FROM bronze.weather_raw

WHERE
    temperature IS NOT NULL
    AND humidity IS NOT NULL
    AND wind_speed IS NOT NULL