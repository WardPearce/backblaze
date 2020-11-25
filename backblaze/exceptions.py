class BackblazeException(Exception):
    """Base backblaze exception.
    """

    def __init__(self, msg="Backblaze Expection", *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class AwaitingOnly(BackblazeException):
    """Raised when a coroutine called is awaiting supported only.
    """

    def __init__(self, msg="This coroutine is only for awaiting",
                 *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class BadRequest(BackblazeException):
    """There is a problem with a passed in request parameters.
    """

    def __init__(self, msg="Bad request made", *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class UnAuthorized(BackblazeException):
    """The code unauthorized means that the application key is bad.
    """

    def __init__(self, msg="UnAuthorized request", *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class Forbidden(BackblazeException):
    """You have a reached a storage cap limit, or account access may
    be impacted in some other way; see the human-readable message.
    """

    def __init__(self,
                 msg="Forbidden, storage cap limit or account access impact",
                 *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class RequestTimeout(BackblazeException):
    """The service timed out trying to read your request.
    This isn't raised for a HTTPX timeout, this is when backblaze times out.
    """

    def __init__(self, msg="Backblaze timed out", *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class TooManyRequests(BackblazeException):
    """B2 may limit API requests on a per-account basis.
    """

    def __init__(self, msg="Backblaze rate limiting", *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class InternalError(BackblazeException):
    """An unexpected error has occurred.
    """

    def __init__(self, msg="Backblaze internal error",
                 *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class ServiceUnavailable(BackblazeException):
    """The service is temporarily unavailable.
    """

    def __init__(self, msg="The service is temporarily unavailable",
                 *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class AuthorizeRequired(BackblazeException):
    """Blocking.authorize or Awaiting.authorize hasn't been called
    before running a function what requires it.
    """

    def __init__(self, msg="Authorize hasn't been called",
                 *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)
