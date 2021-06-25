def migrate(cr, version):
    """Update blocked reasons with dummy reasons since 
    we're making this field a required field if the location is blocked."""
    cr.execute(
        """
        UPDATE stock_location
        SET u_blocked_reason = 'Location is blocked'
        WHERE u_blocked IS True and u_blocked_reason IS Null;
    """
    )
