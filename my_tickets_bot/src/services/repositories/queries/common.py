"""Общие запросы"""

GET_USER_STATISTIC = """
    WITH user_event AS (
        SELECT
            event.id,
            event.time,
            date_part('year', event.time)::int AS year
        FROM event
        WHERE
            event.user_id = $1
    ),
    statistic AS (
        -- Статистика по прошедшим мероприятиям в разрезе года
        SELECT
            COUNT(*) AS count,
            year,
            TRUE AS is_past
        FROM
            user_event
        WHERE 
            time < $2
        GROUP BY 
            year
    
        UNION ALL
        -- Количество планируемых мероприятий в разрезе года
        SELECT
            COUNT(*) AS count,
            year,
            FALSE AS is_part
        FROM
            user_event
        WHERE
            time >= $2
        GROUP BY 
            year
    )   
    SELECT *
    FROM statistic
    ORDER BY year
"""

GET_EVENTS_FOR_DATE = """
    SELECT 
        COALESCE(array_agg(event.id), '{}'::bigint[])
    FROM 
        event
    JOIN location ON location.id = event.location_id
    JOIN city ON city.id = location.city_id
    WHERE
        city.user_id = $1
        AND event.time AT TIME ZONE city.timezone BETWEEN $2 AND $2 + interval '1 day'
"""
