package query

const GetEventQuery string = `
    SELECT
        event.id AS id,
        event.name AS name,
        event.link AS link,
        event.time AT TIME ZONE city.timezone AS time,
        event.end_time AT TIME ZONE city.timezone AS end_time,
        event.created_at AT TIME ZONE city.timezone AS created_at,
        event."UUID" AS uuid,
        event.user_id AS user_id,
        
        city.id AS city_id,
        city.name AS city_name,
        city.timezone AS city_timezone,
        
        location.id AS location_id,
        location.name AS location_name,
        location.address AS location_address,
        location.url AS location_url
        
    FROM event
    JOIN location ON location.id = event.location_id
    JOIN city ON city.id = location.city_id
    WHERE 
        event."UUID" = $1
`
