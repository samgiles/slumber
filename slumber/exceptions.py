class SlumberClientError(Exception):
    """
    Called when the server tells us there was a client error (4xx).
    """
    

class SlumberServerError(Exception):
    """
    Called when the server tells us there was a server error (5xx).
    """