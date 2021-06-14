from functools import wraps

from .exceptions import AuthorizeRequired


def authorize_required(func):
    @wraps(func)
    def _validate(*args, **kwargs):
        if ((hasattr(args[0], "context") and args[0].context.account_id)
                or args[0].account_id):
            return func(*args, **kwargs)
        else:
            raise AuthorizeRequired()

    return _validate
