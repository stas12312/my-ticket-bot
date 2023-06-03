LIST = """
    SELECT
        id,
        name,
        url,
        jsonb_array_length(events) AS events_count,
        timezone,
        timestamp
    FROM parser
"""

GET = """
    SELECT
        id,
        name,
        url,
        jsonb_array_length(events) AS event_count,
        timezone,
        timestamp,
        events
    FROM parser
    WHERE id = $1
"""

GET_SUPPORTER_LOCATIONS = """
    SELECT
        parser.id as parser_id,
        location.id as location_id,
        location.name
    FROM location
    JOIN city ON city.id = location.city_id
    JOIN parser ON parser.url ILIKE '%' || location.url
    WHERE city.user_id = $1
"""

LIST_PARSER_EVENTS = """
    SELECT
    event ->> 'url' AS url,
    event ->> 'name' AS name,
    event ->> 'datetime' AS datetime
    FROM 
        parser,
        jsonb_array_elements(events) as event
    WHERE id = $1
    LIMIT $2 OFFSET $3
"""

COUNT_PARSER_EVENTS = """
    SELECT COUNT(*)
        FROM 
        parser,
        jsonb_array_elements(events) as event
    WHERE id = $1
"""