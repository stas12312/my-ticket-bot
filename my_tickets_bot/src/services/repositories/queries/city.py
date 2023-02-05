"""Запросы для городов"""
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

DELETE_CITY = """
    UPDATE city
    SET is_deleted = True
    WHERE
        user_id = $1
        AND id = $2
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
