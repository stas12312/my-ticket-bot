LIST = """
    SELECT
        name,
        url,
        jsonb_array_length(events) AS events_count,
        timezone,
        timestamp
    FROM parser
"""