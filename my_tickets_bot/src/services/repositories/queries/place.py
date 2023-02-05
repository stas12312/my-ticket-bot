"""Запросы для мест"""
GET_PLACES = """
    SELECT
        P.id AS id,
        P.name AS name,
        P.address AS address,
        C.id AS city_id,
        C.name AS city_name
    FROM place P
    JOIN city C ON C.id = P.city_id
    WHERE
        C.user_id = $1
        -- Опциональный фильтр по городу
        AND CASE
                WHEN $2::bigint IS NOT NULL THEN P.city_id = $2::bigint
            END 
"""

GET_PLACE = """
    SELECT
        P.id AS id,
        P.name AS name,
        P.address AS address,
        C.id AS city_id,
        C.name AS city_name
    FROM place P
    JOIN city C ON C.id = P.city_id
    WHERE
        C.user_id = $1
        AND P.id = $2
"""

GET_PLACE_BY_NAME = """
    SELECT
        P.id AS id,
        P.name AS name,
        P.address AS address,
        C.id AS city_id,
        C.name AS city_name
    FROM place P
    JOIN city C ON C.id = P.city_id
    WHERE
        C.user_id = $1
        AND P.name = $2
"""

SAVE_PLACE = """
    INSERT
    INTO place (city_id, name, address) VALUES ($1, $2, $3)
    RETURNING *
"""

DELETE_PLACE = """
    UPDATE place P
    SET is_deleted = True
    WHERE
        (SELECT C.user_id FROM city C WHERE C.id = P.city_id) = $1 -- Проверка, что пользователю доступно место
        AND P.id = $2
"""
