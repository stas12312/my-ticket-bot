LIST = """
    SELECT
        name,
        url,
        jsonb_array_length(events) AS events_count,
        timezone,
        timestamp
    FROM parser
"""

GET = """
    SELECT
        name,
        url,
        jsonb_array_length(events) AS event_count,
        timezone,
        timestamp,
        events
    FROM parser
    WHERE id = $1
"""
