SAVE_FILE = """
    INSERT 
    INTO file (location, type) VALUES ($1, $2)
    RETURNING *
"""
