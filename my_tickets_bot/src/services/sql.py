"""Запросы к БД"""

SAVE_USER = """
    INSERT INTO "user" (id, username) VALUES ($1, $2)
    ON CONFLICT (id) DO UPDATE
    SET id=$1, username=$2
    RETURNING *
    """
