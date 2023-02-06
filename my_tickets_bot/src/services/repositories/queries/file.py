SAVE_FILE = """
    INSERT 
    INTO file (ticket_id, location) VALUES ($1, $2)
    RETURNING
        id AS file_id,
        ticket_id AS ticket_id,
        location AS file_location
"""
