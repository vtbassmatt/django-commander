from functools import wraps

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest, HttpResponseForbidden


try:
    COMMANDER_KEY = settings.COMMANDER_KEY
except AttributeError as exc:
    raise ImproperlyConfigured('Make sure to set a secure COMMANDER_KEY in your settings') from exc

# don't allow the default key in production
# TODO: switch this to the checks framework:
# https://docs.djangoproject.com/en/2.1/topics/checks/
if COMMANDER_KEY == 's00pers3cret!':
    if settings.DEBUG:
        import warnings
        warnings.warn('You can\'t use the example COMMANDER_KEY. Change it to something else before deploying to production.')
        pass # raise a warning
    else:
        raise ImproperlyConfigured('You can\'t use the example COMMANDER_KEY; change it to something else')


def protect_with_key(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if COMMANDER_KEY is None:
            return HttpResponseForbidden('Commander is disabled')
        if 'key' not in request.GET:
            return HttpResponseBadRequest('Make sure to include the ?key in your querystring')
        if request.GET['key'] != COMMANDER_KEY:
            return HttpResponseForbidden('Incorrect key')
        return view(request, *args, **kwargs)
    return wrapper
