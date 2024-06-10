from functools import wraps
import logging

logger = logging.getLogger(__name__)


def deprecated_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        logger.warn(f"{view_func.__name__} is deprecated")
        response = view_func(request, *args, **kwargs)
        response["Warning"] = '299 - "Deprecated API"'
        return response

    return _wrapped_view
