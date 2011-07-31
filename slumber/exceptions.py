class SlumberBaseException(Exception):
    """
    All Slumber exceptions inherit from this exception.
    """


class SlumberHttpBaseException(SlumberBaseException):
    """
    All Slumber HTTP Exceptions inherit from this exception.
    """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        super(SlumberHttpBaseException, self).__init__(*args)


class SlumberHttpClientError(SlumberHttpBaseException):
    """
    Called when the server tells us there was a client error (4xx).
    """


class SlumberHttpServerError(SlumberHttpBaseException):
    """
    Called when the server tells us there was a server error (5xx).
    """
