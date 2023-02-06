"""Запросы для мест"""
GET_LOCATIONS = """
    SELECT
        location.id AS id,
        location.name AS name,
        
        location.address AS address,
        city.id AS city_id,
        city.name AS city_name
    FROM location
    JOIN city ON city.id = location.city_id
    WHERE
        city.user_id = $1
        -- Опциональный фильтр по городу
        AND CASE
                WHEN $2::bigint IS NOT NULL THEN location.city_id = $2::bigint
                ELSE TRUE
            END 
            
"""

GET_PLACE = """
    SELECT
        location.id AS id,
        location.name AS name,
        location.address AS address,
        
        city.id AS city_id,
        city.name AS city_name
    FROM location
    JOIN city ON city.id = location.city_id
    WHERE
        city.user_id = $1
        AND location.id = $2
"""

GET_PLACE_BY_NAME = """
    SELECT
        location.id AS id,
        location.name AS name,
        location.address AS address,
        city.id AS city_id,
        city.name AS city_name
    FROM location
    JOIN city  ON city.id = location.city_id
    WHERE
        city.user_id = $1
        AND location.name = $2
"""

SAVE_PLACE = """
    INSERT
    INTO location (city_id, name, address) VALUES ($1, $2, $3)
    RETURNING *
"""

DELETE_PLACE = """
    UPDATE location
    SET is_deleted = True
    WHERE
        (SELECT city.user_id FROM city WHERE city.id = location.city_id) = $1 -- Проверка, что пользователю доступно место
        AND location.id = $2
"""
