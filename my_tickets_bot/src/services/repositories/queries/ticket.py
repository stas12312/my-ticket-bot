SAVE_TICKET = """
    INSERT
    INTO ticket (event_id, comment) VALUES ($1, $2)
    RETURNING 
        id AS ticket_id
"""

GET_TICKETS_FOR_EVENT = """
    SELECT
        ticket.id AS ticket_id,
        ticket.created_at AS created_at,
        
        file.id AS file_id,
        file.location AS file_location
        
    FROM ticket
    JOIN event ON event.id = ticket.event_id
    JOIN file ON file.ticket_id = ticket.id
    WHERE
        event.user_id = $1
        AND event.id = $2
"""
