"""Запросы к таблице event"""

SAVE_EVENT = """
    INSERT
    INTO event (user_id, name, time, link, location_id) VALUES ($1, $2, $3, $4, $5)
    RETURNING 
        id AS event_id
"""

GET_EVENTS = """
    SELECT
        event.id AS event_id,
        event.name AS event_name,
        event.link AS event_link,
        event.time AT TIME ZONE city.timezone AS event_time,
        event.created_at AT TIME ZONE city.timezone AS event_created_at,
        
        city.id AS city_id,
        city.name AS city_name,
        
        location.id AS location_id,
        location.name AS location_name,
        location.address AS location_address
        
    FROM event
    JOIN location ON location.id = event.location_id
    JOIN city ON city.id = location.city_id
    WHERE
        event.user_id = $1
        -- Опциональный фильтр по идентификатору
        AND CASE 
                WHEN $2::bigint IS NOT NULL THEN event.id = $2::bigint
                ELSE TRUE
        END
"""

DELETE_EVENT = """
    DELETE FROM event
    WHERE
        event.user_id = $1
        AND event.id = $2
"""
