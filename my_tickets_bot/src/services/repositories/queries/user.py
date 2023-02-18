"""Запросы для пользователей"""

SAVE_USER = """
    INSERT 
    INTO "user" (id, username, first_name, last_name) VALUES ($1, $2, $3, $4)
    ON CONFLICT (id) DO UPDATE
    SET id=$1, username=$2, first_name=$3, last_name=$4
    RETURNING *
    """
