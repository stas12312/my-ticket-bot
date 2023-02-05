"""Запросы к БД"""

SAVE_USER = """
    INSERT 
    INTO "user" (id, username) VALUES ($1, $2)
    ON CONFLICT (id) DO UPDATE
    SET id=$1, username=$2
    RETURNING *
    """

GET_USER_CITIES = """
    SELECT *
    FROM city
    WHERE 
        user_id = $1
        AND is_deleted IS DISTINCT FROM TRUE
"""

CREATE_CITY = """
    INSERT 
    INTO city (user_id, name, timezone) VALUES ($1, $2, $3)
    RETURNING *
"""
GET_CITY = """
    SELECT *
    FROM city
    WHERE 
        user_id = $1
        AND id = $2
"""

GET_CITY_BY_NAME = """
    SELECT *
    FROM city
    WHERE
        user_id = $1
        AND city.name = $2
    
"""

DELETE_CITY = """
    UPDATE city
    SET is_deleted = True
    WHERE
        user_id = $1
        AND id = $2
"""

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
