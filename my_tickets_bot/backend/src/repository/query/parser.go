package query

const (
	ListParser = `
	SELECT
		id,
		name,
		url,
		COALESCE(jsonb_array_length(events), -1) AS events_count,
		timezone,
		COALESCE(timestamp, timestamp 'epoch') AS timestamp
	FROM parser
`
	GetParser = `
	SELECT
		id,
		name,
		url,
		COALESCE(jsonb_array_length(events), -1) AS event_count,
		timezone,
		COALESCE(timestamp, timestamp 'epoch') AS timestamp,
		COALESCE(events, '[]')::jsonb AS events
	FROM parser
	WHERE 
	    id = $1
`
)
