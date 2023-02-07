SAVE_FILE = """
    INSERT 
    INTO file (ticket_id, location, bot_file_id) VALUES ($1, $2, $3)
    RETURNING
        id AS file_id,
        ticket_id AS ticket_id,
        bot_file_id AS bot_file_id,
        location AS file_location
"""
