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
    FROM "city"
    WHERE 
        "user_id" = $1
        AND "is_deleted" IS DISTINCT FROM TRUE
"""

CREATE_CITY = """
    INSERT 
    INTO city (user_id, name, timezone) VALUES ($1, $2, $3)
    RETURNING *
"""
GET_CITY = """
    SELECT *
    FROM "city"
    WHERE 
        "user_id" = $1
        AND "id" = $2
"""

DELETE_CITY = """
    UPDATE "city"
    SET "is_deleted" = True
    WHERE
        "user_id" = $1
        AND "id" = $2
"""
