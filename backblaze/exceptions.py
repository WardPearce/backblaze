class AwaitingOnly(Exception):
    """Raised when a coroutine called is awaiting supported only.
    """

    pass


class BadRequest(Exception):
    """There is a problem with a passed in request parameters.
    """

    pass


class UnAuthorized(Exception):
    """The code unauthorized means that the application key is bad.
    """

    pass


class Forbidden(Exception):
    """You have a reached a storage cap limit, or account access may
    be impacted in some other way; see the human-readable message.
    """

    pass


class RequestTimeout(Exception):
    """The service timed out trying to read your request.
    This isn't raised for a HTTPX timeout, this is when backblaze times out.
    """

    pass


class TooManyRequests(Exception):
    """B2 may limit API requests on a per-account basis.
    """

    pass


class InternalError(Exception):
    """An unexpected error has occurred.
    """

    pass


class ServiceUnavailable(Exception):
    """The service is temporarily unavailable.
    """

    pass
