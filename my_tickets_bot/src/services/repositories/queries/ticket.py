SAVE_TICKET = """
    INSERT
    INTO ticket (user_id, place_id, event_time, event_name, file_id, event_link) VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING *
"""

GET_TICKETS = """
    SELECT 
        T.id as ticket_id,
        T.event_name as event_name,
        T.event_time as event_time,
        T.event_link as event_link,
        T.created_at as created_at,
        T.user_id as user_id,
        P.name as place_name,
        P.address as place_address,
        P.id as place_id,
        C.id as city_id,
        C.name as city_name,
        C.timezone as timezone_name,
        F.id as file_id,
        F.location as file_location
    FROM ticket T
    JOIN place P ON P.id = T.id
    JOIN city C ON C.id = P.city_id
    JOIN file F ON F.id = T.file_id
    WHERE
        T.user_id = $1
    ORDER BY T.event_time
"""
