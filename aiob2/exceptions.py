class InvalidAuthorization(Exception):
    """
    When calling b2_authorize_account, this means that there was
    something wrong with the applicationKeyId or with the
    application key that was provided. The code unauthorized
    means that the application key is bad. The code unsupported
    means that the application key is only valid in a later version of
    the API.

    When uploading data using b2_upload_file or b2_upload_part,
    this can mean a variety of things. Try calling b2_get_upload_url or
    b2_get_upload_part_url again to get a new upload target and
    auth token. That call will either work or provide a meaningful
    error code.

    For all other API calls, the code returned tells you what to do. The
    code unauthorized means that the auth token is valid, but does
    not allow you to make this call with these parameters. When the
    code is either bad_auth_token or expired_auth_token you should
    call b2_authorize_account again to get a new auth token.
    """
    pass


class NoSuchFile(Exception):
    pass


class InvalidPartNumber(Exception):
    pass


class BadRequest(Exception):
    """
    There is a problem with a passed in request
    parameters - the JSON error structure returned will contain an
    error code of bad_request and a human-readable error message
    describing the problem.
    """
    pass


class Forbidden(Exception):
    """
    You have a reached a storage cap limit, or account
    access may be impacted in some other way;
    see the human-readable message.
    """
    pass


class RequestTimeout(Exception):
    """ The service timed out trying to read your request. """
    pass


class TooManyRequests(Exception):
    """ B2 may limit API requests on a per-account basis. """
    pass


class InternalError(Exception):
    """ An unexpected error has occurred. """
    pass


class ServiceUnavailable(Exception):
    """
    The service is temporarily unavailable.
    The human-readable message identifies the nature of the issue,
    in general we recommend retrying with an exponential backoff
    between retries in response to this error.
    """
    pass


class UndefinedError(Exception):
    """
    API has given an error what aiob2 doesn't understand.
    """
    pass
