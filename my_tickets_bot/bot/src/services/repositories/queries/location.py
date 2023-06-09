"""Запросы для мест"""
LIST = """
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
        AND location.is_deleted IS DISTINCT FROM TRUE
        -- Не отображаем места для удаленных городов
        AND city.is_deleted IS DISTINCT FROM TRUE 
            
"""

GET_LOCATION = """
    SELECT
        location.id AS id,
        location.name AS name,
        location.address AS address,
        location.url AS url,
        
        city.id AS city_id,
        city.name AS city_name
    FROM location
    JOIN city ON city.id = location.city_id
    WHERE
        city.user_id = $1
        AND location.id = $2
"""

GET_BY_NAME = """
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

SAVE = """
    INSERT
    INTO location (city_id, name, address, url) VALUES ($1, $2, $3, $4)
    RETURNING *
"""

UPDATE = """
    UPDATE location
    SET
        name = $3,
        address = $4,
        url = $5
    WHERE
        id = $1
        AND city_id = $2
    RETURNING *
"""

DELETE = """
    UPDATE location
    SET is_deleted = True
    WHERE
        -- Проверка, что пользователю доступно место
        (SELECT city.user_id FROM city WHERE city.id = location.city_id) = $1
        AND location.id = $2
"""
