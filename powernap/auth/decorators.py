from flask import abort, current_app
from flask_login import current_user

from powernap.exceptions import PermissionError, UnauthorizedError


def require_public(func, public=False):
    def _formatter(*args, **kwargs):
        if not public and not current_user.is_admin:
            abort(503 if current_app.config["DEBUG"] else 404)
        return func(*args, **kwargs)
    return _formatter


def require_permissions(self, func, permissions=None):
    """Same as :meth:`require` except not a decorator."""
    def _formatter(*args, **kwargs):
        if permissions and not current_user.is_admin:
            if not current_user.has_permission(permissions):
                raise PermissionError(description={'permissions': permissions})
        return func(*args, **kwargs)
    return _formatter


def require_login(func, login=True):
    """Decorate func requires login or raises error.

    Raises :class:`core.api.exceptions.UnauthorizedError`
    """
    def _formatter(*args, **kwargs):
        if login and not current_user.is_authenticated():
            raise UnauthorizedError
        return func(*args, **kwargs)
    return _formatter
