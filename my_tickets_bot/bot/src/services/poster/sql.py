REGISTER_PARSER = """
INSERT INTO parser (name, url, timezone) VALUES ($1, $2, $3)
ON CONFLICT (url)
DO NOTHING 
"""

SAVE_EVENTS_FOR_PARSER = """
UPDATE parser
SET events=$2, timestamp=$3
WHERE name=$1
"""

GET_PARSERS_BY_DATETIME = """
SELECT COALESCE(array_agg(name), '{}'::text[])
FROM parser
WHERE EXTRACT(HOUR FROM $1 AT TIME ZONE parser.timezone) = 14
"""

GET_EVENTS_FOR_PARSER = """
SELECT COALESCE(events, '[]'::jsonb)
FROM parser
WHERE name = $1
"""
